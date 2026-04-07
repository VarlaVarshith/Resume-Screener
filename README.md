# ⚡ ResumeIQ – AI Resume Analyzer

## 📌 Overview

ResumeIQ is an AI-powered Resume Screening System that analyzes resumes and matches them with job roles using Machine Learning and skill-based evaluation.

It helps recruiters and job seekers understand how well a resume fits a specific role and provides actionable improvement suggestions.

---

## 🚀 Features

* 📄 Upload resume (PDF format)
* 🧠 Automatic job role prediction using ML
* 🎯 Skill matching with job categories
* 📊 Resume scoring system
* 📉 Selection chance prediction (High / Moderate / Low)
* ⚠️ Missing skills detection
* 💡 Personalized improvement tips
* 📚 Learning resource recommendations
* 🎨 Modern UI built with Streamlit

---

## 🛠️ Tech Stack

* **Frontend/UI:** Streamlit
* **Backend:** Python
* **Machine Learning:** Scikit-learn
* **NLP:** SpaCy
* **PDF Processing:** pdfplumber

---

## 📂 Project Structure

Resume-Screener/
│── app.py
│── model.pkl
│── encoder.pkl
│── category_skills.pkl
│── requirements.txt
│── README.md

---

## ▶️ How to Run

### 1. Clone the repository

git clone https://github.com/VarlaVarshith/Resume-Screener.git
cd Resume-Screener

### 2. Install dependencies

pip install -r requirements.txt

### 3. Install SpaCy model

python -m spacy download en_core_web_sm

### 4. Run the application

streamlit run app.py

---

## 📊 How it Works

1. Extracts text from uploaded PDF resume
2. Cleans and processes the text
3. Predicts job category using Machine Learning model
4. Matches skills with predefined job requirements
5. Calculates a resume score
6. Provides improvement suggestions and career insights

---

## 🎯 Future Enhancements

* 🔍 Resume vs Job Description matching
* 📂 Multiple resume ranking system
* 📄 Downloadable report generation
* 🌐 Deployment on cloud platforms

---

## 👨‍💻 Author

**Varla Varshith**

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
