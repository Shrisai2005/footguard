# backend/main.py

from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import torch
import torchvision.transforms as transforms
from PIL import Image
import io
import re
import google.generativeai as genai
import os
from dotenv import load_dotenv
# Database imports
from database import SessionLocal, engine
import models
import schemas

# =====================================
# CREATE DATABASE TABLES
# =====================================

models.Base.metadata.create_all(bind=engine)

# =====================================
# GEMINI CONFIG
# =====================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=GEMINI_API_KEY)

model_ai = genai.GenerativeModel("models/gemini-2.5-flash-lite")

# =====================================
# FASTAPI APP
# =====================================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================
# DATABASE SESSION
# =====================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =====================================
# LOAD TRAINED MODEL
# =====================================

model = torch.hub.load(
    "pytorch/vision:v0.10.0",
    "mobilenet_v2",
    pretrained=False
)

model.classifier[1] = torch.nn.Linear(
    model.last_channel,
    4
)

model.load_state_dict(
    torch.load("model.pth", map_location="cpu")
)

model.eval()

# =====================================
# CLASS LABELS
# =====================================

classes = [
    "normal",
    "stage1",
    "stage2",
    "stage3"
]

# =====================================
# IMAGE TRANSFORM
# =====================================

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# =====================================
# HOME ROUTE
# =====================================

@app.get("/")
def home():
    return {
        "message": "FootGuard AI Backend Running"
    }

# =====================================
# IMAGE PREDICTION + SAVE TO DATABASE
# =====================================

@app.post("/predict-image")
async def predict_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    contents = await file.read()

    image = Image.open(
        io.BytesIO(contents)
    ).convert("RGB")

    image = transform(image).unsqueeze(0)

    # AI Prediction
    with torch.no_grad():
        outputs = model(image)
        probs = torch.softmax(outputs, dim=1)

        confidence, predicted = torch.max(
            probs,
            1
        )

    label = classes[predicted.item()]

    severity = (
        "Severe"
        if label == "stage3"
        else "Moderate"
    )

    # =====================================
    # GEMINI PROMPT
    # =====================================

    prompt = f"""
You are an expert medical assistant.

A diabetic patient has {label} diabetic foot ulcer.

Explain clearly using:
1. Disease Explanation
2. Symptoms
3. Causes
4. Severity Level
5. Treatment
6. Prevention
7. When to See Doctor

IMPORTANT RULES:
- Do NOT use quotation marks
- Do NOT use markdown symbols like ** or ###
- Keep language simple and patient-friendly
- Make it visually clean and structured
- Use bullet points where possible
"""

    try:
        response = model_ai.generate_content(prompt)
        text = response.text

        # Clean text
        text = re.sub(r"\\*\\*", "", text)
        text = re.sub(r"\\*", "", text)
        text = re.sub(r"###", "", text)
        text = re.sub(r"---", "", text)
        text = re.sub(r"\\d+\\.\\s*", "", text)
        text = re.sub(r"\\n\\s*\\n+", "\\n\\n", text)

        text = text.strip()

    except Exception as e:
        print("Gemini Error:", str(e))

        # Fallback explanation
        text = f"""
Disease Explanation:
Detected {label} diabetic foot ulcer.

Severity:
{severity}

Treatment:
Please consult a doctor immediately and maintain proper foot care.

Prevention:
Daily foot checks, hygiene, blood sugar control.

Doctor Visit:
Recommended immediately for proper treatment.
"""

    # =====================================
    # SAVE TO DATABASE
    # =====================================

    new_record = models.PatientRecord(
        patient_name="Default Patient",
        age=25,
        stage=label,
        severity=severity,
        confidence=float(confidence.item()),
        ai_explanation=text
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return {
        "id": new_record.id,
        "ulcer_detected": label != "normal",
        "stage": label,
        "severity": severity,
        "confidence": float(confidence.item()),
        "ai_explanation": text
    }

# =====================================
# GET ALL PATIENT HISTORY
# =====================================

@app.get("/patients")
def get_all_patients(
    db: Session = Depends(get_db)
):
    patients = db.query(
        models.PatientRecord
    ).all()

    return patients 