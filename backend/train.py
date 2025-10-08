
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, classification_report
import joblib
import os
import re
import string

# --- Configuration ---
# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer.pkl")

# Try to use the real dataset first, fallback to sample data
DATASET_FILES = [
    os.path.join(BASE_DIR, "WELFake_Dataset.csv"),
    os.path.join(BASE_DIR, "Enhanced_Dataset.csv"),
    # Fallback to old data if needed
    (os.path.join(BASE_DIR, "Fake.csv"), os.path.join(BASE_DIR, "True.csv"))
]

def clean_text(text):
    """
    Advanced text preprocessing for better model accuracy
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove mentions and hashtags
    text = re.sub(r'@\w+|#\w+', '', text)
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def train_model():
    """
    Trains a fake news detection model with improved preprocessing.
    """
    print("=" * 60)
    print("🚀 Starting Advanced Model Training")
    print("=" * 60)

    # --- 1. Load Data ---
    df = None
    dataset_used = None
    
    # Try each dataset source
    for source in DATASET_FILES:
        try:
            if isinstance(source, tuple):
                # Old format with separate files
                print(f"\n📂 Trying legacy dataset format...")
                df_fake = pd.read_csv(source[0])
                df_true = pd.read_csv(source[1])
                
                df_fake["label"] = 1  # 1 for fake news
                df_true["label"] = 0  # 0 for real news
                
                df = pd.concat([df_fake, df_true], ignore_index=True)
                dataset_used = "Legacy (Fake.csv + True.csv)"
            else:
                # New format with single file
                print(f"\n📂 Loading dataset: {os.path.basename(source)}")
                df = pd.read_csv(source)
                dataset_used = os.path.basename(source)
            
            # Check if required columns exist
            if 'text' not in df.columns and 'label' not in df.columns:
                print(f"⚠️  Dataset has wrong format (missing 'text' or 'label' columns)")
                print(f"    Available columns: {df.columns.tolist()}")
                continue
            
            print(f"✅ Successfully loaded {len(df)} articles")
            break
            
        except FileNotFoundError:
            continue
        except Exception as e:
            print(f"⚠️  Error loading: {e}")
            continue
    
    if df is None:
        print("\n❌ ERROR: No dataset found!")
        print("Please run download_dataset.py first")
        return

    # --- 2. Advanced Preprocessing ---
    print(f"\n🔧 Preprocessing with dataset: {dataset_used}")
    
    # Shuffle the dataset
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    # Handle missing values
    df["text"] = df["text"].fillna("")
    
    # Apply advanced text cleaning
    print("📝 Applying text cleaning (URLs, punctuation, lowercase)...")
    df["text"] = df["text"].apply(clean_text)

    # --- 3. Feature Engineering (Enhanced TF-IDF) ---
    print("\n🧮 Creating TF-IDF features with optimized parameters...")
    X = df["text"]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Enhanced TF-IDF with better parameters
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_df=0.7,           # Ignore terms that appear in >70% of documents
        min_df=2,             # Ignore terms that appear in <2 documents
        ngram_range=(1, 2),   # Use unigrams and bigrams for better context
        max_features=5000     # Limit to top 5000 features
    )
    
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    print(f"   ✓ Training samples: {len(X_train)}")
    print(f"   ✓ Testing samples: {len(X_test)}")
    print(f"   ✓ Features extracted: {X_train_tfidf.shape[1]}")

    # --- 4. Model Training ---
    print("\n🤖 Training Logistic Regression model...")
    model = LogisticRegression(
        max_iter=1000,
        class_weight='balanced',  # Handle class imbalance
        C=1.0,                    # Regularization strength
        solver='lbfgs'
    )
    model.fit(X_train_tfidf, y_train)
    print("   ✓ Model training complete!")

    # --- 5. Comprehensive Evaluation ---
    print("\n📊 Evaluating model performance...")
    y_pred = model.predict(X_test_tfidf)
    y_pred_proba = model.predict_proba(X_test_tfidf)
    
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print(f"\n{'=' * 60}")
    print(f"📈 MODEL PERFORMANCE METRICS")
    print(f"{'=' * 60}")
    print(f"✓ Accuracy:  {accuracy * 100:.2f}%")
    print(f"✓ F1 Score:  {f1:.4f}")
    print(f"✓ Dataset:   {dataset_used}")
    print(f"✓ Samples:   {len(df)} total ({len(X_train)} train, {len(X_test)} test)")
    print(f"{'=' * 60}\n")
    
    # Detailed classification report
    print("📋 Detailed Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Real News', 'Fake News']))

    # --- 6. Save Model and Vectorizer ---
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    print(f"\n💾 Saving model to: {MODEL_PATH}")
    joblib.dump(model, MODEL_PATH)

    print(f"💾 Saving vectorizer to: {VECTORIZER_PATH}")
    joblib.dump(vectorizer, VECTORIZER_PATH)

    print(f"\n{'=' * 60}")
    print("✅ TRAINING COMPLETE!")
    print(f"{'=' * 60}")
    print(f"📦 Model files saved successfully")
    print(f"🎯 Ready to make predictions with {accuracy * 100:.2f}% accuracy!")
    print(f"{'=' * 60}\n")

if __name__ == "__main__":
    train_model()
