# 🏋️ AI Real-Time Gym Coach

An AI-powered fitness coaching platform that combines Computer Vision, Pose Estimation, Generative AI, and Voice Feedback to provide real-time exercise analysis and personalized workout guidance.

## 🚀 Features

### Real-Time Exercise Tracking

* Live webcam-based workout monitoring
* MediaPipe pose estimation
* Real-time body landmark detection
* Automated repetition counting

### Supported Exercises

* Squats
* Push-ups
* Lunges
* Shoulder Press
* Biceps Curls

### Form Analysis & Feedback

* Joint angle calculations
* Exercise-specific biomechanics analysis
* Posture correction detection
* Real-time form assessment

### AI Coaching

* Personalized workout feedback using Groq LLM
* Context-aware coaching recommendations
* Dynamic exercise guidance
* Natural language fitness coaching

### Voice Assistance

* Text-to-Speech workout guidance
* Real-time corrective cues
* Set completion announcements
* Workout completion feedback

### Progress Tracking

* Set and rep monitoring
* Workout session management
* Exercise history storage
* Performance analytics dashboard

---

## 🛠️ Tech Stack

### AI & Machine Learning

* MediaPipe
* Computer Vision
* Pose Estimation
* Generative AI (Groq LLM)

### Backend

* Python
* SQLite

### Frontend

* Streamlit
* Streamlit WebRTC

### Data Processing

* NumPy
* Pandas
* OpenCV

### AI Services

* Groq API
* Text-to-Speech

---

## 📂 Project Structure

```text
AI-Real-Time-Gym-Coach/
│
├── core/
├── detectors/
├── ml_models/
├── services/
│   ├── auth/
│   ├── coaching/
│   ├── config/
│   ├── persistence/
│   ├── state/
│   ├── tracking/
│   ├── ui/
│   └── vision/
│
├── static/
├── .streamlit/
├── main.py
└── requirements.txt
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/Xama9696/AI-Real-Time-Gym-Coach.git
cd AI-Real-Time-Gym-Coach
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

Windows:

```bash
.venv\Scripts\activate
```

Linux / macOS:

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

### Run Application

```bash
streamlit run main.py
```

---

## 🎯 Key Capabilities

* Real-time pose tracking
* Automated rep counting
* Exercise-specific form correction
* AI-generated coaching feedback
* Voice-based workout assistance
* Session and progress tracking
* Multi-exercise support

---

## 📸 Demo

Add screenshots and demo videos here.

---

## 🔮 Future Improvements

* Exercise recommendation engine
* Personalized workout plans
* Multi-user analytics
* Mobile deployment
* Advanced exercise detection
* Wearable device integration

---

## 👨‍💻 Author

**Zaman Asif**

AI/ML Enthusiast | Computer Vision | Generative AI | Applied Machine Learning

LinkedIn: Add your LinkedIn URL
GitHub: https://github.com/Xama9696
