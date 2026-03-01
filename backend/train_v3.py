"""
Universal Fact-Check Model Training v3
=======================================
Trains an ensemble model on diverse claim types: news, health, science,
history, tech, social media, urban legends, finance, and more.

Uses improved TF-IDF features + ensemble (LR + SVC + RF) with comprehensive
sanity checks across all claim categories.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
import joblib
import os
import re

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer.pkl")


def clean_text(text):
    """Advanced text preprocessing with style feature engineering."""
    if not isinstance(text, str):
        return ""
    
    original = text
    
    # Count stylistic signals BEFORE lowering
    excl_count = text.count('!')
    question_count = text.count('?')
    caps_words = len([w for w in text.split() if w.isupper() and len(w) > 2])
    caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
    has_all_caps_phrases = bool(re.search(r'\b[A-Z]{3,}\b.*\b[A-Z]{3,}\b', text))
    
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', ' URL ', text, flags=re.MULTILINE)
    text = re.sub(r'@\w+', ' MENTION ', text)
    text = re.sub(r'#\w+', ' HASHTAG ', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = ' '.join(text.split())
    
    # Append engineered pseudo-features as tokens
    # These help the model detect sensationalism
    if excl_count >= 2:
        text += ' FEAT_MANY_EXCLAMATIONS'
    if excl_count >= 5:
        text += ' FEAT_EXTREME_EXCLAMATIONS'
    if caps_ratio > 0.15:
        text += ' FEAT_HIGH_CAPS'
    if caps_ratio > 0.30:
        text += ' FEAT_EXTREME_CAPS'
    if caps_words >= 3:
        text += ' FEAT_MANY_CAPS_WORDS'
    if has_all_caps_phrases:
        text += ' FEAT_CAPS_PHRASES'
    if question_count >= 2:
        text += ' FEAT_MANY_QUESTIONS'
    if excl_count + question_count >= 4:
        text += ' FEAT_HEAVY_PUNCTUATION'
    
    # Detect urgency patterns
    urgency_words = ['breaking', 'urgent', 'alert', 'warning', 'exposed', 'leaked', 'banned', 'shocking', 'bombshell']
    urgency_count = sum(1 for w in urgency_words if w in text)
    if urgency_count >= 2:
        text += ' FEAT_HIGH_URGENCY'
    
    # Detect vague sourcing
    vague_sources = ['they don', 'they won', 'they are hiding', 'they don\'t want', 'doctors hate', 'doctors won', 'wake up', 'open your eyes', 'sheeple']
    if any(vs in text for vs in vague_sources):
        text += ' FEAT_VAGUE_SOURCE'
    
    return text


def load_all_data():
    """Load and combine all available datasets."""
    all_dfs = []

    # 1. Enhanced Dataset v3 (our comprehensive one)
    v3_path = os.path.join(BASE_DIR, "Enhanced_Dataset_v3.csv")
    if os.path.exists(v3_path):
        df = pd.read_csv(v3_path)
        if 'text' in df.columns and 'label' in df.columns:
            print(f"  Loaded Enhanced_Dataset_v3.csv: {len(df)} rows")
            all_dfs.append(df[['text', 'label']])

    # 2. Enhanced Dataset v2 (previous version)
    v2_path = os.path.join(BASE_DIR, "Enhanced_Dataset_v2.csv")
    if os.path.exists(v2_path):
        df = pd.read_csv(v2_path)
        if 'text' in df.columns and 'label' in df.columns:
            print(f"  Loaded Enhanced_Dataset_v2.csv: {len(df)} rows")
            all_dfs.append(df[['text', 'label']])

    # 3. Original Enhanced Dataset
    orig_path = os.path.join(BASE_DIR, "Enhanced_Dataset.csv")
    if os.path.exists(orig_path):
        df = pd.read_csv(orig_path)
        if 'text' in df.columns and 'label' in df.columns:
            print(f"  Loaded Enhanced_Dataset.csv: {len(df)} rows")
            all_dfs.append(df[['text', 'label']])

    # 4. Fake.csv + True.csv (legacy)
    fake_path = os.path.join(BASE_DIR, "Fake.csv")
    true_path = os.path.join(BASE_DIR, "True.csv")
    if os.path.exists(fake_path) and os.path.exists(true_path):
        try:
            df_fake = pd.read_csv(fake_path)
            df_true = pd.read_csv(true_path)
            if 'text' in df_fake.columns and 'text' in df_true.columns:
                df_fake['label'] = 1
                df_true['label'] = 0
                combined = pd.concat([df_fake[['text', 'label']], df_true[['text', 'label']]])
                print(f"  Loaded Fake.csv + True.csv: {len(combined)} rows")
                all_dfs.append(combined)
        except Exception as e:
            print(f"  Skipping Fake/True.csv: {e}")

    if not all_dfs:
        print("ERROR: No datasets found!")
        return None

    final = pd.concat(all_dfs, ignore_index=True)
    final = final.dropna(subset=['text'])
    final = final[final['text'].str.strip().str.len() > 10]
    final = final.drop_duplicates(subset=['text'])
    return final


def train_model():
    print("=" * 60)
    print("  UNIVERSAL FACT-CHECK MODEL TRAINING v3")
    print("=" * 60)

    # --- 1. Load Data ---
    print("\n[1/5] Loading datasets...")
    df = load_all_data()
    if df is None:
        return

    print(f"\n  Total unique samples: {len(df)}")
    print(f"  Real (0): {len(df[df['label']==0])}")
    print(f"  Fake (1): {len(df[df['label']==1])}")

    # --- 2. Preprocess ---
    print("\n[2/5] Preprocessing text...")
    df['text'] = df['text'].apply(clean_text)
    df = df[df['text'].str.len() > 5]

    X = df['text']
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.15, random_state=42, stratify=y
    )
    print(f"  Train: {len(X_train)}, Test: {len(X_test)}")

    # --- 3. Vectorize with improved TF-IDF ---
    print("\n[3/5] Building TF-IDF features...")
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_df=0.90,
        min_df=2,
        ngram_range=(1, 2),   # Bigrams only (trigrams add size with little gain)
        max_features=10000,    # Lean feature set — fast inference
        sublinear_tf=True,
        strip_accents='unicode',
    )

    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    print(f"  Features: {X_train_tfidf.shape[1]}")

    # --- 4. Train Ensemble Model ---
    print("\n[4/5] Training ensemble model...")

    lr = LogisticRegression(max_iter=3000, class_weight='balanced', C=1.0, solver='lbfgs')
    svc = CalibratedClassifierCV(LinearSVC(class_weight='balanced', max_iter=5000, C=0.5))
    rf = RandomForestClassifier(n_estimators=50, class_weight='balanced', max_depth=20, random_state=42, n_jobs=-1)

    ensemble = VotingClassifier(
        estimators=[('lr', lr), ('svc', svc), ('rf', rf)],
        voting='soft',
        weights=[2, 2, 1]
    )

    print("  Training LogisticRegression + LinearSVC + RandomForest ensemble...")
    ensemble.fit(X_train_tfidf, y_train)
    print("  Training complete!")

    # --- 5. Evaluate ---
    print("\n[5/5] Evaluating...")
    y_pred = ensemble.predict(X_test_tfidf)

    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print(f"\n{'=' * 60}")
    print(f"  MODEL PERFORMANCE")
    print(f"{'=' * 60}")
    print(f"  Accuracy:  {accuracy * 100:.2f}%")
    print(f"  F1 Score:  {f1:.4f}")
    print(f"  Samples:   {len(df)} total ({len(X_train)} train, {len(X_test)} test)")
    print(f"{'=' * 60}\n")

    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Real/Credible', 'Fake/Non-Credible']))

    cm = confusion_matrix(y_test, y_pred)
    print(f"Confusion Matrix:")
    print(f"  True Negatives  (Real→Real): {cm[0][0]}")
    print(f"  False Positives (Real→Fake): {cm[0][1]}")
    print(f"  False Negatives (Fake→Real): {cm[1][0]}")
    print(f"  True Positives  (Fake→Fake): {cm[1][1]}")

    # Cross-validation
    print(f"\nRunning 5-fold cross-validation...")
    X_all_tfidf = vectorizer.transform(X)
    cv_scores = cross_val_score(
        LogisticRegression(max_iter=3000, class_weight='balanced', C=1.0),
        X_all_tfidf, y, cv=5, scoring='f1'
    )
    print(f"  CV F1 scores: {[f'{s:.4f}' for s in cv_scores]}")
    print(f"  Mean CV F1: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

    # --- 6. Save ---
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(ensemble, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    print(f"\n  Model saved to {MODEL_PATH}")
    print(f"  Vectorizer saved to {VECTORIZER_PATH}")

    # --- 7. Comprehensive Sanity Checks ---
    print(f"\n{'=' * 60}")
    print("  COMPREHENSIVE SANITY CHECKS")
    print(f"{'=' * 60}")

    test_cases = [
        # === SHOULD BE DETECTED AS FAKE ===
        ("FAKE", "Conspiracy",      "BREAKING: Government caught putting mind control drugs in tap water!!! They don't want you to know! Share NOW!!!"),
        ("FAKE", "Health misinfo",   "Drinking bleach in small quantities CURES cancer! Doctors are HIDING this from you! Big Pharma is FURIOUS!"),
        ("FAKE", "Clickbait",        "You won't BELIEVE what scientists found in vaccines! Big Pharma is HIDING this! Watch before it gets DELETED!"),
        ("FAKE", "Flat Earth",       "PROOF that the Earth is flat! NASA has been faking space photos for decades! The truth is finally out!!!"),
        ("FAKE", "Election fraud",   "EXPOSED: Massive voter fraud scheme during the last election. Millions of fake ballots confirmed by inside source!"),
        ("FAKE", "Financial scam",   "Mom of 3 discovers loophole that makes $5,000 per day from her phone! Banks HATE this trick!"),
        ("FAKE", "Urban legend",     "CONFIRMED: Bigfoot was captured alive by the military! Multiple witnesses verified! Why isn't media covering this??"),
        ("FAKE", "WhatsApp forward", "FORWARD THIS TO EVERYONE!! Starting tomorrow all messages monitored by government! Send to 10 people NOW!"),
        ("FAKE", "Celebrity death",  "RIP Keanu Reeves! Mysterious circumstances! The official story doesn't add up! SHARE before they delete this!"),
        ("FAKE", "Science denial",   "EXPOSED: Climate change is the biggest scientific fraud in history! Follow the MONEY! The evidence is UNDENIABLE!"),
        ("FAKE", "Fake history",     "HIDDEN TRUTH: The pyramids were built by aliens using antigravity technology! Your history books LIED to you!"),
        ("FAKE", "Tech scare",       "LEAKED: Your phone is recording ALL conversations even when turned off! Apple just ADMITTED it! Delete everything NOW!"),
        ("FAKE", "Anti-vax",         "Vaccines contain magnetic nanoparticles — try putting a magnet on your arm! mRNA permanently alters your DNA!!!"),
        ("FAKE", "5G conspiracy",    "WARNING: 5G towers are being activated to control your thoughts!! This is being CENSORED! Repost on every platform!"),
        ("FAKE", "Food scare",       "The bread you eat every day is DESTROYING your brain! Made from recycled plastic! A scientist was FIRED for revealing this!"),
        ("FAKE", "Crypto scam",      "Elon Musk just endorsed TruthCoin! Invest now before it goes to the MOON! A 19-year-old made $50,000 in 3 days!"),
        ("FAKE", "NWO claim",        "NEW WORLD ORDER: The UN just dissolved all national borders! Secret meeting of billionaires controlling population! NOT A DRILL!"),
        ("FAKE", "Miracle cure",     "This one weird trick reverses aging by 20 years! Doctors HATE it! Number 7 will SHOCK you!"),
        ("FAKE", "General misinfo",  "FACT THEY HIDE: The cure for cancer has existed for decades! Curing it isn't profitable! Wake up people!!!"),
        ("FAKE", "Short fake",       "BREAKING: All hospitals going on emergency lockdown! Share with EVERYONE before they censor this!!!"),

        # === SHOULD BE DETECTED AS REAL ===
        ("REAL", "News economy",     "The Federal Reserve raised interest rates by 0.25% on Wednesday, citing persistent inflation concerns. Economists largely supported the decision."),
        ("REAL", "News science",     "NASA announced the successful launch of the Artemis III mission from Kennedy Space Center on Monday."),
        ("REAL", "News politics",    "The Senate voted 67-33 to approve the Infrastructure Investment Act, which would allocate funding for bridge and road repairs."),
        ("REAL", "Health fact",      "The CDC recommends that adults get at least 150 minutes of moderate-intensity exercise per week to reduce cardiovascular risk."),
        ("REAL", "Science study",    "Researchers at MIT published a study in Nature showing that a new compound may slow the progression of Alzheimer's disease."),
        ("REAL", "General fact",     "Water boils at 100 degrees Celsius at standard atmospheric pressure, a physical constant established through thermodynamic research."),
        ("REAL", "History",          "The signing of the Treaty of Versailles occurred in 1919, resulting in significant geopolitical changes."),
        ("REAL", "Climate fact",     "According to NOAA, global CO2 concentrations reached 421 parts per million in 2024, continuing an upward trend."),
        ("REAL", "Tech neutral",     "According to a report by Gartner, global AI spending exceeded $150 billion in 2025."),
        ("REAL", "Education",        "City officials in Austin approved a $45 million plan to renovate the downtown transit hub. Construction begins in March."),
        ("REAL", "Expert opinion",   "Experts at Stanford noted that AI has potential to improve healthcare. While early results are encouraging, ethical challenges remain."),
        ("REAL", "Short fact",       "The Earth revolves around the Sun, completing one orbit approximately every 365.25 days."),
        ("REAL", "DNA fact",         "DNA carries the genetic instructions for all known living organisms. The Human Genome Project completed mapping in 2003."),
        ("REAL", "Medical trial",    "The FDA approved a new monoclonal antibody treatment for rheumatoid arthritis after Phase III trials showed significant improvement."),
        ("REAL", "Environment",      "Renewable energy sources accounted for 35% of electricity generation in Germany in 2025, according to NOAA."),
        ("REAL", "Archaeology",      "Archaeological evidence from Göbekli Tepe confirms that advanced engineering was used in ancient construction, dating back approximately 10,000 years."),
        ("REAL", "Vaccine fact",     "Vaccines work by training the immune system to recognize and fight pathogens. The CDC and WHO recommend vaccination based on clinical trial data."),
        ("REAL", "Space fact",       "The International Space Station orbits the Earth approximately every 90 minutes at an altitude of about 400 kilometers."),
        ("REAL", "Nutrition",        "A systematic review in JAMA examined 83 studies and found that moderate coffee consumption is not associated with increased cardiovascular risk."),
        ("REAL", "Short fact 2",     "The human heart beats approximately 100,000 times per day. This rate varies based on age, fitness level, and activity."),
    ]

    correct = 0
    total = len(test_cases)
    misses = []

    for expected, category, text in test_cases:
        cleaned = clean_text(text)
        vec = vectorizer.transform([cleaned])
        pred = ensemble.predict(vec)[0]
        prob = ensemble.predict_proba(vec)[0]
        label = "FAKE" if pred == 1 else "REAL"
        conf = max(prob) * 100
        is_correct = label == expected

        if is_correct:
            correct += 1
            status = "OK"
        else:
            status = "MISS"
            misses.append((expected, category, label, conf, text[:60]))

        snippet = text[:65] + "..." if len(text) > 65 else text
        print(f"  [{status}] Expected={expected} Got={label} ({conf:.0f}%) [{category}] {snippet}")

    print(f"\n{'=' * 60}")
    print(f"  SANITY CHECK RESULTS: {correct}/{total} correct ({correct/total*100:.1f}%)")
    if misses:
        print(f"\n  MISSES:")
        for exp, cat, got, conf, snip in misses:
            print(f"    Expected {exp}, Got {got} ({conf:.0f}%) [{cat}] {snip}...")
    print(f"{'=' * 60}")
    print("  TRAINING COMPLETE!")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    train_model()
