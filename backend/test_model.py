"""
Test the trained model with various examples
"""

import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, 'models/model.pkl'))
vectorizer = joblib.load(os.path.join(BASE_DIR, 'models/vectorizer.pkl'))

# Test cases
test_cases = [
    # Should be detected as FAKE
    ("Government admits to microchipping population through vaccines. Share before deleted!", "FAKE"),
    ("Scientists discover cure for all diseases using simple herb. Doctors hate this!", "FAKE"),
    ("Breaking: Moon landing was faked in Hollywood studio. Evidence revealed!", "FAKE"),
    ("Drink this before bed and lose 50 pounds in one week without exercise!", "FAKE"),
    
    # Should be detected as REAL
    ("Congress passes infrastructure bill after months of negotiations. Legislation allocates funding.", "REAL"),
    ("Stock market closes mixed as investors react to earnings reports. Tech sector gains.", "REAL"),
    ("Federal Reserve raises interest rates by 0.25 percentage points to control inflation.", "REAL"),
    ("Study published in medical journal shows benefits of regular exercise over five years.", "REAL"),
    
    # Edge cases - potentially ambiguous
    ("President announces new policy on climate change. Critics question effectiveness.", "REAL"),
    ("Shocking revelation about celebrity. Sources confirm tragedy.", "FAKE"),
]

print("=" * 80)
print("🧪 TESTING MODEL PREDICTIONS")
print("=" * 80)

correct = 0
total = len(test_cases)

for text, expected in test_cases:
    # Make prediction
    prediction = model.predict(vectorizer.transform([text]))[0]
    confidence = max(model.predict_proba(vectorizer.transform([text]))[0]) * 100
    predicted_label = "FAKE" if prediction == 1 else "REAL"
    
    # Check if correct
    is_correct = predicted_label == expected
    correct += is_correct
    
    # Display result
    status = "✅" if is_correct else "❌"
    print(f"\n{status} Text: {text[:60]}...")
    print(f"   Expected: {expected} | Predicted: {predicted_label} | Confidence: {confidence:.1f}%")

print("\n" + "=" * 80)
print(f"📊 ACCURACY: {correct}/{total} ({correct/total*100:.1f}%)")
print("=" * 80)
