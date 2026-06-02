import os
import uuid
from flask import Flask, request, jsonify, send_from_directory, session
import database
import joblib

app = Flask(__name__, static_folder="static", static_url_path="")
app.secret_key = "mindmate_super_secret_session_key"

# Path to the trained NLP model
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mindmate_model.joblib")

# Load model pipeline
nlp_model = None
def load_model():
    global nlp_model
    if os.path.exists(MODEL_PATH):
        try:
            nlp_model = joblib.load(MODEL_PATH)
            print("NLP model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            nlp_model = None
    else:
        print("Model file not found. Running with rule-based fallback until trained.")
        nlp_model = None

# Fallback NLP logic if model is not loaded yet
def fallback_nlp(text):
    text_lower = text.lower()
    # Simple rule-based intent/mood detection
    if any(k in text_lower for k in ["hello", "hi", "hey", "morning", "afternoon"]):
        return "neutral", "greeting"
    elif any(k in text_lower for k in ["stressed", "stress", "anxious", "exam", "test", "finals", "grade"]):
        if any(k in text_lower for k in ["aced", "win", "won", "passed", "great", "excellent", "a"]):
            return "happy", "biology_test"
        return "stressed", "stress_exam"
    elif any(k in text_lower for k in ["focus", "concentrate", "distract", "phone", "scroll", "procrastinate"]):
        return "distracted", "focus_help"
    elif any(k in text_lower for k in ["aced", "passed", "did well", "got an a", "perfect score"]):
        return "happy", "biology_test"
    elif any(k in text_lower for k in ["overwhelmed", "drowning", "too much", "burnout", "plate"]):
        return "overwhelmed", "overwhelmed"
    elif any(k in text_lower for k in ["don't understand", "confused", "stuck", "don't get", "makes no sense"]):
        return "anxious", "confused_topic"
    elif any(k in text_lower for k in ["bye", "goodbye", "later", "thanks"]):
        return "neutral", "goodbye"
    
    return "neutral", "general"

# Empathetic response generation based on intent and mood
def generate_bot_response(text, mood, intent, first_name="there"):
    responses = {
        "greeting": [
            f"Hello {first_name}! I'm MindMate, your emotion-aware study companion. How are you feeling today?",
            f"Hi {first_name}! I'm here to support you through your study sessions and help manage any stress. What's on your mind?"
        ],
        "stress_exam": [
            f"I hear you, {first_name}. Exam stress can be incredibly heavy. Remember that exams measure your knowledge of a specific topic at a single point in time, not your intelligence or value. Let's take a slow breath. I can help you break down your study topics, or we can plan a study session together. What would help you most right now?",
            "Exam season is tough, but you are tougher. Let's make a plan to conquer this step-by-step. What subject is causing you the most stress right now?"
        ],
        "focus_help": [
            "It's completely normal to struggle with focus. Sometimes our brains are just tired or overstimulated. Let's try the Pomodoro technique: study for 25 minutes, then take a 5-minute break. I can help you set a timer, or we can write down your primary study goal for the hour. Want to try that?",
            "Focus comes and goes. Let's start with just one small task to get you going. Tell me one small thing you'd like to get done in the next 15 minutes."
        ],
        "biology_test": [
            "Congratulations! 🎉 Acing your test is amazing news! Your hard work is paying off, and you should be so proud of yourself. Let's log this positive mood to your tracker. What subject are we tackling next, or are you taking a well-deserved break?",
            "Wow, great job! You absolutely crushed it. Taking a moment to celebrate these wins is so important. How are you planning to reward yourself?"
        ],
        "overwhelmed": [
            "I'm really sorry you're feeling overwhelmed. When there's too much on your plate, everything feels impossible. Let's do a 'brain dump': tell me everything you need to do, and we can organize it step-by-step. We can start with just the absolute highest priority item. How does that sound?",
            "Take a deep breath. When you're overwhelmed, the best step is a small step. Let's look at your study planner and just check off one tiny task. We'll handle this together."
        ],
        "confused_topic": [
            "Failing to understand a topic is frustrating, and it's easy to feel anxious. But confusion is actually the first step of learning! Let's break it down. What specific part is confusing? We can figure out how to approach it or structure a revision guide.",
            "We can absolutely figure this out. Sometimes explaining it to someone else (or a bot!) helps. Tell me what you know about the topic so far, and we can fill in the blanks."
        ],
        "goodbye": [
            "Goodbye! Good luck with your studying. Remember to take regular breaks, and I'll be here whenever you need a chat.",
            "Take care! You've got this. See you soon!"
        ],
        "general": [
            "I understand. Studying and academic life have their ups and downs. I'm here to listen, help you plan, or just chat about how you're feeling. What would help you most right now?",
            "Thanks for sharing. Let's work together to make your study session a positive experience. What topic are we working on today?"
        ]
    }
    
    # Choose template list
    template_list = responses.get(intent, responses["general"])
    
    # Pick a response based on mood or simple alternating
    import random
    response_text = random.choice(template_list)
    return response_text

def generate_bot_tips(mood, intent):
    tips = []
    if intent == "stress_exam" or mood == "stressed":
        tips.append({"title": "WELLNESS TIP", "text": "Try a short breathing break and notice how your body feels."})
        tips.append({"title": "STUDY TIP", "text": "Break your work into smaller chunks and focus for 25 minutes at a time."})
    elif intent == "focus_help" or mood == "distracted":
        tips.append({"title": "WELLNESS TIP", "text": "Put your phone away and take a 60-second stretch before starting."})
        tips.append({"title": "STUDY TIP", "text": "Write down one simple study goal, then reward yourself after finishing it."})
    elif intent == "biology_test" or mood == "happy":
        tips.append({"title": "CELEBRATION TIP", "text": "Great job! Celebrate your progress with a small break or treat."})
        tips.append({"title": "REFLECTION TIP", "text": "Take a moment to note what study habit helped you succeed today."})
    elif intent == "confused_topic" or mood == "anxious":
        tips.append({"title": "WELLNESS TIP", "text": "Acknowledge that confusion is part of learning, and you're doing the right thing."})
        tips.append({"title": "STUDY TIP", "text": "Try explaining the topic out loud in your own words to make it clearer."})
    elif intent == "overwhelmed" or mood == "overwhelmed":
        tips.append({"title": "WELLNESS TIP", "text": "Take a few deep breaths and write down the most urgent task first."})
        tips.append({"title": "STUDY TIP", "text": "Choose one small action you can complete in 5 minutes to get started."})
    else:
        tips.append({"title": "WELLNESS TIP", "text": "Pause for a moment and notice how your body feels before you keep studying."})
        tips.append({"title": "STUDY TIP", "text": "Pick one topic and study it for a short, focused interval."})
    return tips

# Serves static frontend index
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

# Serves other static files (js, css, etc.)
@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# --- API ENDPOINTS ---

# Authentication
@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.json
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")
    
    if not all([first_name, last_name, email, password]):
        return jsonify({"error": "All fields are required"}), 400
        
    user = database.create_user(first_name, last_name, email, password)
    if not user:
        return jsonify({"error": "User with this email already exists"}), 400
        
    return jsonify(user), 201

@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    if not all([email, password]):
        return jsonify({"error": "Email and password are required"}), 400
        
    user = database.verify_user(email, password)
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401
        
    return jsonify(user), 200

# Chat sessions
@app.route("/api/chats", methods=["GET", "POST"])
def manage_chats():
    user_id = request.args.get("user_id") or request.headers.get("X-User-Id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
        
    if request.method == "POST":
        data = request.json
        title = data.get("title", "New conversation")
        chat_id = str(uuid.uuid4())
        chat = database.create_chat(chat_id, user_id, title)
        return jsonify(chat), 201
    else:
        chats = database.get_chats_by_user(user_id)
        return jsonify(chats), 200

@app.route("/api/chats/<chat_id>", methods=["GET", "PUT", "DELETE"])
def chat_details(chat_id):
    user_id = request.args.get("user_id") or request.headers.get("X-User-Id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
        
    chat = database.get_chat(chat_id)
    if not chat or str(chat["user_id"]) != str(user_id):
        return jsonify({"error": "Chat not found"}), 404
        
    if request.method == "DELETE":
        database.delete_chat_tips(chat_id)
        database.delete_chat(chat_id, user_id)
        return jsonify({"message": "Chat deleted"}), 200
    elif request.method == "PUT":
        data = request.json or {}
        title = data.get("title", "").strip()
        if not title:
            return jsonify({"error": "Chat title is required"}), 400
        updated_chat = database.update_chat_title(chat_id, user_id, title)
        return jsonify(updated_chat), 200
    else:
        messages = database.get_messages_by_chat(chat_id)
        tips = database.get_tips_by_chat(chat_id)
        return jsonify({"messages": messages, "tips": tips}), 200

# Messaging
@app.route("/api/chats/<chat_id>/message", methods=["POST"])
def post_message(chat_id):
    user_id = request.headers.get("X-User-Id") or request.json.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
        
    chat = database.get_chat(chat_id)
    if not chat or str(chat["user_id"]) != str(user_id):
        return jsonify({"error": "Chat not found"}), 404
        
    data = request.json
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Message content cannot be empty"}), 400
        
    # Run NLP Mood and Intent classifier
    mood = "neutral"
    intent = "general"
    
    if nlp_model is not None:
        try:
            mood_pred = nlp_model["mood_pipeline"].predict([text])
            intent_pred = nlp_model["intent_pipeline"].predict([text])
            mood = mood_pred[0]
            intent = intent_pred[0]
        except Exception as e:
            print(f"Prediction failed: {e}")
            mood, intent = fallback_nlp(text)
    else:
        mood, intent = fallback_nlp(text)
        
    # Get user profile information to personalize response
    user_info = database.get_user_by_id(user_id)
    first_name = user_info["first_name"] if user_info else "there"
    
    # Save user message
    user_msg = database.add_message(chat_id, "user", text, mood)
    
    # Generate bot response
    bot_reply_text = generate_bot_response(text, mood, intent, first_name)
    bot_tips = generate_bot_tips(mood, intent)
    
    # Save bot message
    bot_msg = database.add_message(chat_id, "bot", bot_reply_text)
    
    # Save the tip cards so they can be restored for this chat later
    if bot_tips:
        database.add_chat_tips(chat_id, bot_tips)
    
    # Automatically log the mood to user mood logs (if it's not neutral)
    if mood != "neutral":
        database.add_mood_log(user_id, mood, f"Auto-detected from chat: '{text[:30]}...'" )
        
    return jsonify({
        "user_message": user_msg,
        "bot_message": bot_msg,
        "detected_mood": mood,
        "detected_intent": intent,
        "tips": bot_tips
    }), 200

# Mood tracker
@app.route("/api/mood/history", methods=["GET"])
def mood_history():
    user_id = request.args.get("user_id") or request.headers.get("X-User-Id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
        
    history = database.get_mood_history(user_id)
    return jsonify(history), 200

@app.route("/api/mood/log", methods=["POST"])
def log_mood():
    user_id = request.headers.get("X-User-Id") or request.json.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
        
    data = request.json
    mood = data.get("mood")
    notes = data.get("notes")
    
    if not mood:
        return jsonify({"error": "Mood is required"}), 400
        
    log = database.add_mood_log(user_id, mood, notes)
    return jsonify(log), 201

# Study planner
@app.route("/api/tasks", methods=["GET", "POST"])
def manage_tasks():
    user_id = request.args.get("user_id") or request.headers.get("X-User-Id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
        
    if request.method == "POST":
        data = request.json
        title = data.get("title", "").strip()
        if not title:
            return jsonify({"error": "Task title is required"}), 400
        task = database.create_task(user_id, title)
        return jsonify(task), 201
    else:
        tasks = database.get_tasks_by_user(user_id)
        return jsonify(tasks), 200

@app.route("/api/tasks/<int:task_id>", methods=["PUT", "DELETE"])
def update_task(task_id):
    user_id = request.headers.get("X-User-Id") or request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
        
    if request.method == "PUT":
        status = database.toggle_task(task_id, user_id)
        if not status:
            return jsonify({"error": "Task not found"}), 404
        return jsonify(status), 200
    else:
        database.delete_task(task_id, user_id)
        return jsonify({"message": "Task deleted"}), 200

if __name__ == "__main__":
    load_model()
    app.run(host="0.0.0.0", port=10000)
