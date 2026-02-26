
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import google.generativeai as genai
from dotenv import load_dotenv

# --- Configuration ---
# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY not found in environment variables.")
else:
    genai.configure(api_key=GEMINI_API_KEY)

# --- App Initialization ---
app = FastAPI(
    title="Fake News Detector API",
    description="An API to detect fake news using Gemini AI.",
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

# --- Pydantic Models ---
class NewsArticle(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    explanation: str

# --- API Endpoints ---
@app.get("/", tags=["Health Check"])
def read_root():
    """Root endpoint for health checks."""
    return {"status": "API is running"}

@app.post("/predict", response_model=PredictionResponse, tags=["AI Analysis"])
async def predict(article: NewsArticle):
    """Predicts if a news article is real or fake using Gemini AI."""
    if not article.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API key is not configured.")

    # Check cache first
    if article.text in cache:
        return cache[article.text]

    try:
        # Initialize the model
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Create the prompt
        prompt = f"""
        You are an expert fact-checker and journalist. Analyze the following news article text and determine if it is likely "Real" or "Fake" news.
        
        Article Text:
        \"\"\"{article.text}\"\"\"
        
        Provide your analysis in the following JSON format exactly, with no markdown formatting or extra text:
        {{
            "prediction": "Real" or "Fake",
            "confidence": a float between 0.0 and 1.0 representing your confidence,
            "explanation": "A brief explanation of why you made this prediction, pointing out specific linguistic markers, lack of sources, sensationalism, or factual consistency."
        }}
        """

        # Generate response
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean up potential markdown formatting from the response
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
            
        response_text = response_text.strip()
        
        # Parse JSON
        result = json.loads(response_text)
        
        # Validate and format the result
        prediction_text = result.get("prediction", "Fake")
        if prediction_text not in ["Real", "Fake"]:
            prediction_text = "Fake"
            
        confidence = float(result.get("confidence", 0.5))
        explanation = result.get("explanation", "No explanation provided.")

        # Create response
        prediction_response = PredictionResponse(
            prediction=prediction_text,
            confidence=confidence,
            explanation=explanation
        )

        # Store in cache
        if len(cache) > 100: # Simple cache eviction
            cache.pop(next(iter(cache)))
        cache[article.text] = prediction_response

        return prediction_response

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse AI response.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
