from __future__ import annotations

from typing import Iterable

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.svm import LinearSVC

from src.config import EMOTION_LABELS
from src.features import EMOTION_KEYWORDS, EmotionKeywordFeatures
from src.text_utils import normalize_text


class HybridEmotionClassifier(BaseEstimator, ClassifierMixin):
    """Combines an ML classifier with lightweight emotion lexicon scoring."""

    def __init__(self, ml_weight: float = 0.78, keyword_weight: float = 0.22) -> None:
        self.ml_weight = ml_weight
        self.keyword_weight = keyword_weight

    def _build_pipeline(self) -> Pipeline:
        return Pipeline(
            steps=[
                (
                    "features",
                    FeatureUnion(
                        transformer_list=[
                            (
                                "word_tfidf",
                                TfidfVectorizer(
                                    preprocessor=normalize_text,
                                    ngram_range=(1, 2),
                                    min_df=1,
                                    sublinear_tf=True,
                                    strip_accents="unicode",
                                ),
                            ),
                            (
                                "char_tfidf",
                                TfidfVectorizer(
                                    analyzer="char_wb",
                                    preprocessor=normalize_text,
                                    ngram_range=(3, 5),
                                    min_df=1,
                                    sublinear_tf=True,
                                    strip_accents="unicode",
                                ),
                            ),
                            ("emotion_keywords", EmotionKeywordFeatures()),
                        ]
                    ),
                ),
                (
                    "clf",
                    CalibratedClassifierCV(
                        estimator=LinearSVC(class_weight="balanced"),
                        cv=3,
                    ),
                ),
            ]
        )

    def fit(self, X: Iterable[str], y: Iterable[str]) -> "HybridEmotionClassifier":
        self.pipeline_ = self._build_pipeline()
        self.pipeline_.fit(X, y)
        self.classes_ = self.pipeline_.classes_
        return self

    def predict_proba(self, X: Iterable[str]) -> np.ndarray:
        ml_probs = self.pipeline_.predict_proba(X)
        hybrid_probs = []

        for idx, text in enumerate(X):
            keyword_probs = self._keyword_distribution(str(text))
            combined = (self.ml_weight * ml_probs[idx]) + (self.keyword_weight * keyword_probs)
            combined = combined / combined.sum()
            hybrid_probs.append(combined)

        return np.asarray(hybrid_probs)

    def predict(self, X: Iterable[str]) -> np.ndarray:
        probs = self.predict_proba(X)
        indices = probs.argmax(axis=1)
        return np.asarray([self.classes_[idx] for idx in indices])

    def _keyword_distribution(self, text: str) -> np.ndarray:
        normalized = normalize_text(text)
        tokens = normalized.split()
        scores = []

        for emotion in self.classes_:
            keywords = EMOTION_KEYWORDS.get(emotion, [])
            token_matches = sum(1.0 for token in tokens for keyword in keywords if keyword in token)
            phrase_matches = sum(1.5 for keyword in keywords if keyword in normalized)
            scores.append(token_matches + phrase_matches)

        scores_array = np.asarray(scores, dtype=float)
        if scores_array.sum() == 0:
            scores_array = np.ones(len(self.classes_), dtype=float)
        return scores_array / scores_array.sum()
