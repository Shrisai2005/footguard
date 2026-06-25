# 🦶 FootGuard - AI Powered Diabetic Foot Ulcer Stage Detection System

FootGuard is an AI-powered healthcare application designed for the early detection and stage classification of Diabetic Foot Ulcers (DFU). The system combines Deep Learning, Computer Vision, FastAPI, React, and Gemini AI to help patients and healthcare professionals identify ulcer severity and receive AI-generated medical guidance.

---

## 📌 Project Overview

Diabetic Foot Ulcers are one of the leading complications of diabetes and can result in severe infections or amputations if left untreated.

FootGuard analyzes an uploaded foot image using a trained MobileNetV2 deep learning model and predicts the ulcer stage. It then generates patient-friendly explanations, treatment suggestions, prevention tips, and medical guidance using Google's Gemini AI.

---

## ✨ Features

- 🔍 AI-based diabetic foot ulcer detection
- 📊 Stage Classification
  - Normal
  - Stage 1
  - Stage 2
  - Stage 3
- 📈 Confidence score for each prediction
- 🤖 AI-generated medical explanation using Gemini AI
- 💾 Patient history stored in database
- ⚡ FastAPI backend for prediction APIs
- 🎨 React frontend with image upload interface
- 📱 Simple and user-friendly interface

---

## 🏗️ System Architecture

```
User
   │
   ▼
React Frontend
   │
   ▼
FastAPI Backend
   │
   ├── Image Preprocessing
   │
   ├── MobileNetV2 Model
   │
   ├── Stage Prediction
   │
   ├── Gemini AI Explanation
   │
   └── Database Storage
   │
   ▼
Prediction Results
```

---

## 🛠️ Tech Stack

### Frontend

- React.js
- HTML
- CSS
- JavaScript

### Backend

- FastAPI
- Python
- SQLAlchemy

### AI & Machine Learning

- PyTorch
- TorchVision
- MobileNetV2
- Google Gemini AI

### Database

- SQLite

---

## 📂 Project Structure

```
footguard_ai_project/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── train_model.py
│   ├── model.pth
│   └── requirements.txt
│
├── frontend/
│   ├── package.json
│   ├── public/
│   └── src/
│
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/Shrisai2005/footguard.git
```

---

### Backend Setup

```bash
cd backend

pip install -r requirements.txt
```

Create a `.env` file:

```
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

Run the backend:

```bash
uvicorn main:app --reload
```

---

### Frontend Setup

```bash
cd frontend

npm install

npm start
```

---

## 📷 Screenshots

Add screenshots of:

- Home Page
- Image Upload
- Prediction Result
- AI Explanation
- Patient History

---

## 🤖 AI Prediction Output

The backend returns:

```json
{
  "ulcer_detected": true,
  "stage": "stage2",
  "severity": "Moderate",
  "confidence": 0.96,
  "ai_explanation": "..."
}
```

---

## 🔮 Future Enhancements

- IoT Smart Insole Integration
- Thermal Image Analysis
- Multiple Image Support
- Doctor Dashboard
- Patient Login & Authentication
- Cloud Deployment
- Mobile Application
- PDF Medical Report Generation

---

## 👨‍💻 Author

**Shrisai Aski**

B.Tech – Electronics and Communication Engineering

GitHub: https://github.com/Shrisai2005

LinkedIn: https://linkedin.com/in/shrisai-aski-21940828a

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.