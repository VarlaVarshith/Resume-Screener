# ResumeIQ – AI Resume Analyzer

## Overview

ResumeIQ is an AI-powered resume screening system that analyzes resumes and matches them with relevant job roles using machine learning and skill-based evaluation.

The system helps recruiters and job seekers understand how well a resume aligns with a specific role and provides actionable suggestions for improvement.

---

## Features

* Upload resume in PDF format
* Automatic job role prediction using machine learning
* Skill extraction and matching with job categories
* Resume scoring based on skill relevance
* Selection chance prediction (High, Moderate, Low)
* Identification of missing skills
* Personalized improvement suggestions
* Learning resource recommendations
* Interactive user interface built with Streamlit

---

## Tech Stack

* Frontend: Streamlit
* Backend: Python
* Machine Learning: Scikit-learn
* Natural Language Processing: SpaCy
* PDF Processing: pdfplumber

---

## Project Structure

Resume-Screener/
│── app.py
│── model.pkl
│── encoder.pkl
│── category_skills.pkl
│── requirements.txt
│── README.md

---

## Installation and Setup

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

## How It Works

1. Extracts text from the uploaded resume
2. Cleans and processes the extracted text
3. Predicts the job category using a trained machine learning model
4. Matches extracted skills with predefined job requirements
5. Calculates a resume score based on skill overlap
6. Provides insights, suggestions, and improvement strategies

---

## Future Enhancements

* Resume and job description matching
* Multiple resume comparison and ranking
* Downloadable analysis reports
* Deployment on cloud platforms

---

## Author

Varla Varshith

---

## License

This project is for educational and demonstration purposes.
