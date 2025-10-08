
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import os

# --- Configuration ---
# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer.pkl")

# --- App Initialization ---
app = FastAPI(
    title="Fake News Detector API",
    description="An API to detect fake news using a machine learning model.",
    version="1.0.0"
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
) 

# --- In-memory Cache ---
cache = {}

# --- Load Model and Vectorizer ---
def load_model():
    """Loads the model and vectorizer from disk if they exist."""
    if not (os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH)):
        print("WARNING: Model or vectorizer not found. Running in dummy mode.")
        return None, None
    
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    return model, vectorizer

model, vectorizer = load_model()

# --- Pydantic Models ---
class NewsArticle(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    explanation: str

# --- Helper Functions ---
def generate_explanation(prediction: str, confidence: float) -> str:
    """Generates a simple explanation for the prediction."""
    if prediction == "Real":
        if confidence > 0.9:
            return "The model is highly confident that this is a real news article based on its textual content and structure."
        else:
            return "The model predicts this is a real news article, but with some uncertainty. It shares some characteristics with both real and fake news."
    else: # Fake
        if confidence > 0.9:
            return "The model is highly confident that this is a fake news article. It likely contains language patterns commonly found in fabricated stories."
        else:
            return "The model predicts this is a fake news article, but with some uncertainty. It's advisable to cross-reference with other sources."

# --- API Endpoints ---
@app.get("/", tags=["Health Check"])
def read_root():
    """Root endpoint for health checks."""
    return {"status": "API is running"}

@app.post("/predict", response_model=PredictionResponse, tags=["Machine Learning"])
def predict(article: NewsArticle):
    """Predicts if a news article is real or fake."""
    if not article.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    # If model is not loaded, return a dummy response
    if model is None or vectorizer is None:
        return PredictionResponse(
            prediction="Real",
            confidence=0.99,
            explanation="This is a dummy response. Please train a real model for actual predictions."
        )

    # Check cache first
    if article.text in cache:
        return cache[article.text]

    try:
        # TF-IDF Transformation
        text_vector = vectorizer.transform([article.text])

        # Prediction
        prediction_proba = model.predict_proba(text_vector)[0]
        prediction_label = np.argmax(prediction_proba)

        confidence = float(prediction_proba[prediction_label])
        prediction_text = "Real" if prediction_label == 0 else "Fake"

        # Generate Explanation
        explanation = generate_explanation(prediction_text, confidence)

        # Create response
        response = PredictionResponse(
            prediction=prediction_text,
            confidence=confidence,
            explanation=explanation
        )

        # Store in cache
        if len(cache) > 100: # Simple cache eviction
            cache.pop(next(iter(cache)))
        cache[article.text] = response

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
