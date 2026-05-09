# MindMate

MindMate is an emotion-aware student companion chatbot that detects emotions from text and responds with supportive, context-aware guidance for both mental well-being and academic productivity.

This upgraded version adds a Streamlit UI, richer emotion detection, confidence scoring, chat analytics, study suggestions, mental health tips, and optional voice features.

It uses Natural Language Processing (NLP) and machine learning to classify emotions and provide personalized recommendations for students.

---

## Resume-ready highlights

- Streamlit web app with chat view and dashboard
- 8 supported emotions:
  - happy
  - sad
  - stressed
  - anxious
  - angry
  - lonely
  - motivated
  - tired
- Emotion confidence display for every prediction
- Improved NLP model using hybrid TF-IDF + keyword-aware classification
- Hybrid classification with ML + emotion-keyword features
- Emotion tracking charts and session chat history
- Personalized study suggestions and wellness recommendations
- Optional voice input and text-to-speech support
- Stored model metrics for portfolio-ready accuracy reporting

---

## Project Structure

```text
MindMate/
│── data/
│   └── emotion_dataset.csv
│── model/
│   └── emotion_pipeline.joblib
│── src/
│   ├── app.py
│   ├── chatbot.py
│   ├── config.py
│   ├── text_utils.py
│   └── train.py
│── requirements.txt
│── README.md
```

---

## Features

### Basic Features Included

1. Emotion accuracy display
2. More emotions
3. Better responses
4. Chat history
5. Emotion tracking
6. Study suggestions
7. Mental health tips
8. Web app with Streamlit
9. Voice input
10. Text-to-speech
11. Dashboard
12. Better model

---

## Model Upgrade

The original Naive Bayes approach is replaced with a stronger hybrid classification pipeline:

- Text normalization
- Word and character TF-IDF features
- Emotion-keyword feature extraction
- Calibrated Linear SVM plus keyword-aware probability blending
- Lightweight text augmentation for the bundled training set
- 5-fold cross-validation for a more credible accuracy estimate
- Held-out test split for additional evaluation

This setup is more resume-friendly than a basic classifier and crosses the 85% benchmark on the bundled project dataset.

---

## Latest Local Metrics

From `model/metrics.json` after running:

```bash
python -m src.train
```

### Metrics

- Cross-validation accuracy: 99.4%
- Held-out test accuracy: 100.0%
- Macro F1: 99.4%
- Base dataset size: 144 examples
- Augmented training size: 834 examples

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Run Training

```bash
python -m src.train
```

This saves:

- `model/emotion_pipeline.joblib`
- `model/metrics.json`

---

## Run the App

```bash
streamlit run src/app.py
```

---

## Notes on Voice Features

- Voice input uses `st.audio_input` in Streamlit
- Speech transcription may require internet access when using Google recognizer
- Text-to-speech uses `pyttsx3` when available

---

## Suggested Resume / Interview Talking Points

- Built an emotion-aware student support chatbot using NLP and machine learning
- Improved text classification using TF-IDF, keyword features, and a calibrated Linear SVM with cross-validation
- Developed a Streamlit dashboard for real-time emotion analytics and chat history
- Added personalized academic and mental wellness recommendations based on predicted emotion
- Integrated optional voice input and text-to-speech for a more accessible conversational experience