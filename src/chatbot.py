from __future__ import annotations

import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib

from src.config import MENTAL_HEALTH_TIPS, RESPONSE_LIBRARY, STUDY_SUGGESTIONS
from src.train import METRICS_PATH, MODEL_PATH, train_and_save

BASE_DIR = Path(__file__).resolve().parents[1]


@dataclass
class MindMateReply:
    emotion: str
    confidence: float
    response: str
    study_tip: str
    wellness_tip: str


class EmotionAwareCompanion:
    def __init__(self) -> None:
        self.pipeline = self._load_or_train_model()
        self.metrics = self._load_metrics()

    def _load_or_train_model(self) -> Any:
        if not MODEL_PATH.exists():
            train_and_save()
        return joblib.load(MODEL_PATH)

    def _load_metrics(self) -> dict[str, Any]:
        if not METRICS_PATH.exists():
            train_and_save()
        return json.loads(METRICS_PATH.read_text(encoding="utf-8"))

    def analyze(self, text: str) -> MindMateReply:
        predicted_emotion = self.pipeline.predict([text])[0]
        confidence = self._predict_confidence(text, predicted_emotion)

        response = random.choice(RESPONSE_LIBRARY[predicted_emotion])
        study_tip = random.choice(STUDY_SUGGESTIONS[predicted_emotion])
        wellness_tip = random.choice(MENTAL_HEALTH_TIPS[predicted_emotion])

        return MindMateReply(
            emotion=predicted_emotion,
            confidence=confidence,
            response=response,
            study_tip=study_tip,
            wellness_tip=wellness_tip,
        )

    def _predict_confidence(self, text: str, predicted_emotion: str) -> float:
        if hasattr(self.pipeline, "predict_proba"):
            probabilities = self.pipeline.predict_proba([text])[0]
            return float(max(probabilities))

        if hasattr(self.pipeline, "decision_function"):
            scores = self.pipeline.decision_function([text])[0]
            if scores.ndim == 0:
                return 0.75
            shifted = scores - scores.min()
            total = shifted.sum()
            if total == 0:
                return 0.75
            labels = self.pipeline.classes_
            confidence_map = {label: shifted[idx] / total for idx, label in enumerate(labels)}
            return float(confidence_map.get(predicted_emotion, 0.75))

        return 0.75
