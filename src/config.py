from __future__ import annotations

EMOTION_LABELS = [
    "happy",
    "sad",
    "stressed",
    "anxious",
    "angry",
    "lonely",
    "motivated",
    "tired",
]

EMOTION_COLORS = {
    "happy": "#f6bd60",
    "sad": "#577590",
    "stressed": "#f94144",
    "anxious": "#7b2cbf",
    "angry": "#d62828",
    "lonely": "#4d908e",
    "motivated": "#2a9d8f",
    "tired": "#6c757d",
}

RESPONSE_LIBRARY = {
    "happy": [
        "That energy sounds wonderful. Let's channel it into something meaningful today.",
        "I'm glad you're feeling positive. This is a great moment to build momentum on your goals.",
    ],
    "sad": [
        "I'm sorry today feels heavy. We can take this one step at a time and keep things gentle.",
        "That sounds difficult. You deserve support, and we can focus on one small helpful action right now.",
    ],
    "stressed": [
        "It sounds like a lot is piling up. Let's reduce the pressure by picking one manageable next step.",
        "Stress can make everything feel urgent. We'll sort it into a clear, calmer plan together.",
    ],
    "anxious": [
        "Anxiety can make the future feel louder than the present. Let's ground ourselves in what you can control next.",
        "You're not alone in this feeling. A steady plan and a short breathing pause can help lower the noise.",
    ],
    "angry": [
        "That frustration makes sense. Let's cool the intensity first, then decide on the most useful response.",
        "I hear the tension in that. Taking a short pause now can help you protect your focus and energy.",
    ],
    "lonely": [
        "That sounds isolating. Even small connection points can help, and we can think of one together.",
        "I'm here with you in this moment. Let's find one supportive action that makes today feel less distant.",
    ],
    "motivated": [
        "That drive is powerful. Let's turn it into a focused plan you can actually finish.",
        "You're in a strong mindset right now. This is a perfect time to commit to a specific goal.",
    ],
    "tired": [
        "It sounds like your energy is low. Let's protect your effort by choosing a lighter, smarter next step.",
        "Fatigue can make even easy tasks feel bigger. A short reset and a reduced workload may help a lot.",
    ],
}

STUDY_SUGGESTIONS = {
    "happy": [
        "Use this positive window for deep work on your toughest subject.",
        "Try a 50-minute focus session followed by a short reward break.",
    ],
    "sad": [
        "Choose a low-pressure task like reviewing notes or flashcards for 15 minutes.",
        "Break one chapter into three micro-goals and stop after the first success.",
    ],
    "stressed": [
        "List every task, then circle the one with the closest deadline.",
        "Use the Pomodoro method: 25 minutes study, 5 minutes rest, repeat four times.",
    ],
    "anxious": [
        "Start with a familiar topic to rebuild confidence before harder material.",
        "Write a two-step plan instead of a full schedule so it feels easier to begin.",
    ],
    "angry": [
        "Switch to structured work like practice questions or problem sets until you feel calmer.",
        "Study somewhere quieter for 20 minutes to reduce extra stimulation.",
    ],
    "lonely": [
        "Try a virtual body-doubling session or study with a classmate over chat.",
        "Join an online study room and commit to one shared study sprint.",
    ],
    "motivated": [
        "Set one ambitious but realistic target for this session and track your finish time.",
        "Use active recall and timed quizzes while your focus is strong.",
    ],
    "tired": [
        "Prioritize revision over new learning so your brain has less cognitive load.",
        "Study for 15 minutes, rest for 5, and stop after two cycles if the fatigue stays high.",
    ],
}

MENTAL_HEALTH_TIPS = {
    "happy": [
        "Take a moment to notice what is going well so you can return to it later.",
        "Share your positive energy with a friend or journal one good thing about today.",
    ],
    "sad": [
        "Drink some water, sit somewhere comfortable, and take five slower breaths.",
        "If this feeling keeps staying intense, reaching out to someone you trust can help.",
    ],
    "stressed": [
        "Try box breathing: inhale 4, hold 4, exhale 4, hold 4.",
        "Close extra tabs and notifications for ten minutes to create mental space.",
    ],
    "anxious": [
        "Name five things you can see to ground yourself in the present.",
        "Relax your jaw and shoulders while taking one slow breath longer than usual.",
    ],
    "angry": [
        "Step away briefly before responding to anything important.",
        "Loosen your hands and shoulders, then take a short walk if possible.",
    ],
    "lonely": [
        "Send one simple message to someone safe, even if it is just a check-in.",
        "A routine activity in a shared space can reduce the feeling of isolation.",
    ],
    "motivated": [
        "Protect this momentum by planning breaks before you need them.",
        "Balance ambition with rest so the energy lasts beyond today.",
    ],
    "tired": [
        "Stand up, stretch, and rest your eyes from screens for a minute.",
        "If you can, a short nap or early night may help more than pushing through.",
    ],
}
