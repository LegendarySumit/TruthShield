"""
Improved Fake News Detection Model Training
Uses larger dataset, better features, and ensemble model for higher accuracy.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
import joblib
import os
import re
import string

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer.pkl")


def clean_text(text):
    """Advanced text preprocessing."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', ' URL ', text, flags=re.MULTILINE)
    text = re.sub(r'@\w+', ' MENTION ', text)
    text = re.sub(r'#\w+', ' HASHTAG ', text)
    # Count exclamation/question marks before removing (these are strong fake signals)
    excl_count = text.count('!')
    caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = ' '.join(text.split())
    # Append engineered features as pseudo-words
    if excl_count >= 3:
        text += ' MANY_EXCLAMATIONS'
    if caps_ratio > 0.3:
        text += ' HIGH_CAPS_RATIO'
    return text


def load_all_data():
    """Load and combine all available datasets."""
    all_dfs = []

    # 1. Enhanced Dataset v2 (our generated one)
    v2_path = os.path.join(BASE_DIR, "Enhanced_Dataset_v2.csv")
    if os.path.exists(v2_path):
        df = pd.read_csv(v2_path)
        if 'text' in df.columns and 'label' in df.columns:
            print(f"  Loaded Enhanced_Dataset_v2.csv: {len(df)} rows")
            all_dfs.append(df[['text', 'label']])

    # 2. Original Enhanced Dataset
    orig_path = os.path.join(BASE_DIR, "Enhanced_Dataset.csv")
    if os.path.exists(orig_path):
        df = pd.read_csv(orig_path)
        if 'text' in df.columns and 'label' in df.columns:
            print(f"  Loaded Enhanced_Dataset.csv: {len(df)} rows")
            all_dfs.append(df[['text', 'label']])

    # 3. Fake.csv + True.csv (legacy format)
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
    final = final[final['text'].str.strip().str.len() > 10]  # Remove very short texts
    final = final.drop_duplicates(subset=['text'])
    return final


def train_model():
    print("=" * 60)
    print("  IMPROVED MODEL TRAINING v2")
    print("=" * 60)

    # --- 1. Load Data ---
    print("\n[1/5] Loading datasets...")
    df = load_all_data()
    if df is None:
        return

    print(f"\n  Total samples: {len(df)}")
    print(f"  Real (0): {len(df[df['label']==0])}")
    print(f"  Fake (1): {len(df[df['label']==1])}")

    # --- 2. Preprocess ---
    print("\n[2/5] Preprocessing text...")
    df['text'] = df['text'].apply(clean_text)
    df = df[df['text'].str.len() > 5]

    X = df['text']
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"  Train: {len(X_train)}, Test: {len(X_test)}")

    # --- 3. Vectorize with improved TF-IDF ---
    print("\n[3/5] Building TF-IDF features...")
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_df=0.85,          # More lenient — don't remove too many common words
        min_df=2,
        ngram_range=(1, 3),   # Unigrams + bigrams + trigrams for better context
        max_features=15000,   # More features for better discrimination
        sublinear_tf=True,    # Apply sublinear TF scaling (1 + log(tf))
    )

    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    print(f"  Features: {X_train_tfidf.shape[1]}")

    # --- 4. Train Ensemble Model ---
    print("\n[4/5] Training ensemble model...")

    # Individual models
    lr = LogisticRegression(max_iter=2000, class_weight='balanced', C=1.0, solver='lbfgs')
    svc = CalibratedClassifierCV(LinearSVC(class_weight='balanced', max_iter=3000, C=0.5))
    rf = RandomForestClassifier(n_estimators=200, class_weight='balanced', max_depth=None, random_state=42, n_jobs=-1)

    # Soft voting ensemble
    ensemble = VotingClassifier(
        estimators=[('lr', lr), ('svc', svc), ('rf', rf)],
        voting='soft',
        weights=[2, 2, 1]  # LR and SVC often better for text
    )

    print("  Training LogisticRegression + LinearSVC + RandomForest ensemble...")
    ensemble.fit(X_train_tfidf, y_train)
    print("  Training complete!")

    # --- 5. Evaluate ---
    print("\n[5/5] Evaluating...")
    y_pred = ensemble.predict(X_test_tfidf)
    y_pred_proba = ensemble.predict_proba(X_test_tfidf)

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
    print(classification_report(y_test, y_pred, target_names=['Real News', 'Fake News']))

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"Confusion Matrix:")
    print(f"  True Negatives (Real→Real): {cm[0][0]}")
    print(f"  False Positives (Real→Fake): {cm[0][1]}")
    print(f"  False Negatives (Fake→Real): {cm[1][0]}")
    print(f"  True Positives (Fake→Fake): {cm[1][1]}")

    # Cross-validation
    print(f"\nRunning 5-fold cross-validation on full dataset...")
    X_all_tfidf = vectorizer.transform(X)
    cv_scores = cross_val_score(
        LogisticRegression(max_iter=2000, class_weight='balanced', C=1.0),
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

    # --- 7. Quick sanity checks ---
    print(f"\n{'=' * 60}")
    print("  SANITY CHECKS")
    print(f"{'=' * 60}")
    test_texts = [
        "BREAKING: Government caught putting mind control drugs in tap water!!! They don't want you to know! Share NOW!!!",
        "The Federal Reserve raised interest rates by 0.25% on Wednesday, citing persistent inflation concerns.",
        "You won't BELIEVE what scientists found in vaccines! Big Pharma is HIDING this! Watch before it gets deleted!",
        "NASA announced the successful launch of the Artemis III mission from Kennedy Space Center on Monday.",
        "EXPOSED: The Deep State has been rigging elections for decades! Millions of fake ballots confirmed!",
        "City officials in Austin approved a $45 million plan to renovate the downtown transit hub.",
    ]

    for text in test_texts:
        cleaned = clean_text(text)
        vec = vectorizer.transform([cleaned])
        pred = ensemble.predict(vec)[0]
        prob = ensemble.predict_proba(vec)[0]
        label = "FAKE" if pred == 1 else "REAL"
        conf = max(prob) * 100
        snippet = text[:80] + "..." if len(text) > 80 else text
        print(f"  [{label} {conf:.0f}%] {snippet}")

    print(f"\n{'=' * 60}")
    print("  TRAINING COMPLETE!")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    train_model()
