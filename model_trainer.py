import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib

# Curated dataset for student mental state and study intent
# X: text statements, y_mood: mood label, y_intent: intent label

data = [
    # GREETING
    ("hello", "neutral", "greeting"),
    ("hi", "neutral", "greeting"),
    ("hey", "neutral", "greeting"),
    ("good morning", "neutral", "greeting"),
    ("good afternoon", "neutral", "greeting"),
    ("hello mindmate", "neutral", "greeting"),
    ("hey there", "neutral", "greeting"),
    ("hi bot", "neutral", "greeting"),
    
    # EXAM STRESS
    ("i'm stressed about exams", "stressed", "stress_exam"),
    ("stressed about exams", "stressed", "stress_exam"),
    ("i am so stressed about finals", "stressed", "stress_exam"),
    ("worried about my test", "stressed", "stress_exam"),
    ("exam stress is driving me crazy", "stressed", "stress_exam"),
    ("too much exam pressure", "stressed", "stress_exam"),
    ("anxious about tests", "stressed", "stress_exam"),
    ("i have a big exam coming up and i am panicking", "stressed", "stress_exam"),
    ("i'm terrified of my exams", "stressed", "stress_exam"),
    ("the exam schedule is stress inducing", "stressed", "stress_exam"),
    
    # FOCUS ISSUES
    ("i can't focus today", "distracted", "focus_help"),
    ("can't focus today", "distracted", "focus_help"),
    ("i cannot concentrate", "distracted", "focus_help"),
    ("distracted by my phone", "distracted", "focus_help"),
    ("my mind keeps wandering", "distracted", "focus_help"),
    ("i'm procrastinating so much", "distracted", "focus_help"),
    ("hard to pay attention to studying", "distracted", "focus_help"),
    ("i keep losing focus", "distracted", "focus_help"),
    ("i want to study but i keep scrolling social media", "distracted", "focus_help"),
    ("my attention span is zero right now", "distracted", "focus_help"),
    
    # ACED TEST / SUCCESS
    ("i aced my test!", "happy", "biology_test"),
    ("aced my biology test!", "happy", "biology_test"),
    ("i did so well in my exam", "happy", "biology_test"),
    ("passed my chemistry test with an a", "happy", "biology_test"),
    ("i scored top marks", "happy", "biology_test"),
    ("aced my finals!", "happy", "biology_test"),
    ("got a great grade on the exam", "happy", "biology_test"),
    ("i am so proud of my test results", "happy", "biology_test"),
    ("i passed!", "happy", "biology_test"),
    ("exam went amazingly well", "happy", "biology_test"),
    
    # OVERWHELMED
    ("i feel overwhelmed", "overwhelmed", "overwhelmed"),
    ("feel overwhelmed", "overwhelmed", "overwhelmed"),
    ("there is too much work to do", "overwhelmed", "overwhelmed"),
    ("i can't handle all this homework", "overwhelmed", "overwhelmed"),
    ("drowning in assignments", "overwhelmed", "overwhelmed"),
    ("i am burning out", "overwhelmed", "overwhelmed"),
    ("so much stuff to learn, i want to cry", "overwhelmed", "overwhelmed"),
    ("too many things on my plate", "overwhelmed", "overwhelmed"),
    ("i'm under a mountain of pressure", "overwhelmed", "overwhelmed"),
    ("it's all too much for me", "overwhelmed", "overwhelmed"),
    
    # CONFUSED ABOUT TOPIC
    ("i don't understand this topic", "anxious", "confused_topic"),
    ("don't understand this topic", "anxious", "confused_topic"),
    ("this subject makes no sense", "anxious", "confused_topic"),
    ("i am confused by math", "anxious", "confused_topic"),
    ("stuck on this physics problem", "anxious", "confused_topic"),
    ("i don't get this biology concept", "anxious", "confused_topic"),
    ("this textbook explanation is confusing", "anxious", "confused_topic"),
    ("i am failing to grasp these ideas", "anxious", "confused_topic"),
    ("can't solve this algebra equation", "anxious", "confused_topic"),
    ("chemistry is too hard, i don't understand it", "anxious", "confused_topic"),
    
    # GOODBYE
    ("bye", "neutral", "goodbye"),
    ("goodbye", "neutral", "goodbye"),
    ("see you later", "neutral", "goodbye"),
    ("thanks for the help, bye", "neutral", "goodbye"),
    ("i'll go study now, bye", "neutral", "goodbye"),
    ("talk to you later", "neutral", "goodbye"),
    ("have a good day", "neutral", "goodbye"),
    
    # GENERAL / STUDY TALK
    ("what is the study planner?", "neutral", "general"),
    ("can you help me organize?", "neutral", "general"),
    ("let's write down a study schedule", "neutral", "general"),
    ("tell me a tip", "neutral", "general"),
    ("i'm going to library", "neutral", "general"),
    ("today i will study for 4 hours", "neutral", "general"),
    ("what is my current mood?", "neutral", "general"),
    ("how are you?", "neutral", "general"),
    ("who are you?", "neutral", "general"),
]

def train_and_save():
    X = [item[0] for item in data]
    y_mood = [item[1] for item in data]
    y_intent = [item[2] for item in data]
    
    # We will build pipelines for mood and intent.
    # We use a TfidfVectorizer with word and character n-grams to handle small spelling errors and variations.
    vectorizer_mood = TfidfVectorizer(ngram_range=(1, 2), lowercase=True, stop_words='english', min_df=1)
    classifier_mood = LogisticRegression(C=2.0, max_iter=1000, class_weight='balanced')
    
    vectorizer_intent = TfidfVectorizer(ngram_range=(1, 2), lowercase=True, stop_words='english', min_df=1)
    classifier_intent = LogisticRegression(C=2.0, max_iter=1000, class_weight='balanced')
    
    # Train mood pipeline
    mood_pipeline = Pipeline([
        ('vectorizer', vectorizer_mood),
        ('clf', classifier_mood)
    ])
    mood_pipeline.fit(X, y_mood)
    print("Mood classifier trained successfully.")
    
    # Train intent pipeline
    intent_pipeline = Pipeline([
        ('vectorizer', vectorizer_intent),
        ('clf', classifier_intent)
    ])
    intent_pipeline.fit(X, y_intent)
    print("Intent classifier trained successfully.")
    
    # Save the pipeline models and metadata
    model_data = {
        "mood_pipeline": mood_pipeline,
        "intent_pipeline": intent_pipeline
    }
    
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mindmate_model.joblib")
    joblib.dump(model_data, model_path)
    print(f"Models saved successfully to {model_path}")

if __name__ == "__main__":
    train_and_save()
