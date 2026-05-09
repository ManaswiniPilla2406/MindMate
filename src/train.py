from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import StratifiedKFold, cross_val_predict, train_test_split

from src.modeling import HybridEmotionClassifier

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "emotion_dataset.csv"
MODEL_DIR = BASE_DIR / "model"
MODEL_PATH = MODEL_DIR / "emotion_pipeline.joblib"
METRICS_PATH = MODEL_DIR / "metrics.json"


def build_pipeline() -> HybridEmotionClassifier:
    return HybridEmotionClassifier()


def augment_dataset(df: pd.DataFrame) -> pd.DataFrame:
    augmented_rows: list[dict[str, str]] = []

    for _, row in df.iterrows():
        text = str(row["text"]).strip()
        emotion = str(row["emotion"]).strip()

        variants = {
            text,
            f"Today {text.lower()}",
            f"Lately {text.lower()}",
            f"As a student, {text.lower()}",
            text.replace("I am", "I'm").replace("I feel", "I'm feeling"),
            text.replace("I cannot", "I can't"),
            f"{text} and it is affecting my studies",
        }

        for variant in variants:
            augmented_rows.append({"text": variant, "emotion": emotion})

    augmented_df = pd.DataFrame(augmented_rows).drop_duplicates().reset_index(drop=True)
    return augmented_df


def train_and_save() -> dict:
    base_df = pd.read_csv(DATA_PATH, sep="|").dropna()
    df = augment_dataset(base_df)
    X = df["text"].astype(str)
    y = df["emotion"].astype(str)

    pipeline = build_pipeline()

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_predictions = cross_val_predict(pipeline, X, y, cv=cv)
    cv_accuracy = accuracy_score(y, cv_predictions)
    report = classification_report(y, cv_predictions, output_dict=True, zero_division=0)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    pipeline.fit(X_train, y_train)
    test_accuracy = accuracy_score(y_test, pipeline.predict(X_test))

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)

    metrics = {
        "cross_validation_accuracy": round(float(cv_accuracy) * 100, 2),
        "test_accuracy": round(float(test_accuracy) * 100, 2),
        "dataset_size": int(len(df)),
        "base_dataset_size": int(len(base_df)),
        "class_report_macro_f1": round(float(report["macro avg"]["f1-score"]) * 100, 2),
        "labels": sorted(df["emotion"].unique().tolist()),
    }
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics


if __name__ == "__main__":
    results = train_and_save()
    print(json.dumps(results, indent=2))
