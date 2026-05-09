from __future__ import annotations

from typing import Iterable

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

from src.config import EMOTION_LABELS
from src.text_utils import normalize_text

EMOTION_KEYWORDS = {
    "happy": ["happy", "joy", "glad", "great", "excited", "cheerful", "optimistic", "content"],
    "sad": ["sad", "cry", "down", "heartbroken", "miserable", "unhappy", "empty", "gloomy"],
    "stressed": ["stress", "deadline", "pressure", "overwhelmed", "burnout", "urgent", "workload"],
    "anxious": ["anxious", "nervous", "worried", "panic", "uneasy", "restless", "overthinking"],
    "angry": ["angry", "mad", "furious", "annoyed", "frustrated", "rage", "irritated"],
    "lonely": ["lonely", "alone", "isolated", "disconnected", "unseen", "forgotten", "distant"],
    "motivated": ["motivated", "driven", "focused", "determined", "inspired", "productive", "goal"],
    "tired": ["tired", "exhausted", "sleepy", "fatigued", "drained", "drowsy", "sluggish"],
}


class EmotionKeywordFeatures(BaseEstimator, TransformerMixin):
    """Counts how strongly each input matches emotion-specific keywords."""

    def fit(self, X: Iterable[str], y: Iterable[str] | None = None) -> "EmotionKeywordFeatures":
        return self

    def transform(self, X: Iterable[str]) -> np.ndarray:
        rows = []
        for text in X:
            normalized = normalize_text(str(text))
            tokens = normalized.split()
            row = []
            for emotion in EMOTION_LABELS:
                keywords = EMOTION_KEYWORDS[emotion]
                count = sum(1 for token in tokens for keyword in keywords if keyword in token)
                row.append(count)
            rows.append(row)
        return np.asarray(rows, dtype=float)
