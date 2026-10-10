import numpy as np

from xgboost import XGBClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

# ==========================================================
# LOAD EMBEDDINGS
# ==========================================================

train_x = np.load(
    "ml_pipeline/faiss/index_data/train_embeddings.npy"
)

train_y = np.load(
    "ml_pipeline/faiss/index_data/train_labels.npy"
)

test_x = np.load(
    "ml_pipeline/faiss/index_data/test_embeddings.npy"
)

test_y = np.load(
    "ml_pipeline/faiss/index_data/test_labels.npy"
)

print("=" * 70)
print("HYRAGE EMBEDDING CLASSIFICATION")
print("=" * 70)

print("Train:", train_x.shape)
print("Test :", test_x.shape)

# ==========================================================
# XGBOOST
# ==========================================================

model = XGBClassifier(
    objective="multi:softmax",
    num_class=len(np.unique(train_y)),
    n_estimators=300,
    max_depth=8,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    tree_method="hist",
    eval_metric="mlogloss"
)

print("\nTraining XGBoost...")

model.fit(train_x, train_y)

print("Training Completed.")

# ==========================================================
# PREDICTION
# ==========================================================

pred = model.predict(test_x)

acc = accuracy_score(test_y, pred)
prec = precision_score(
    test_y,
    pred,
    average="macro",
    zero_division=0,
)
rec = recall_score(
    test_y,
    pred,
    average="macro",
    zero_division=0,
)
f1 = f1_score(
    test_y,
    pred,
    average="macro",
    zero_division=0,
)

print("\n" + "=" * 70)
print("RESULTS")
print("=" * 70)

print(f"Accuracy : {acc*100:.2f}%")
print(f"Precision: {prec*100:.2f}%")
print(f"Recall   : {rec*100:.2f}%")
print(f"Macro F1 : {f1*100:.2f}%")

print("\nClassification Report\n")

print(
    classification_report(
        test_y,
        pred,
        digits=4,
        zero_division=0
    )
)

cm = confusion_matrix(
    test_y,
    pred
)

np.save(
    "experiments/E4_XGBoost_On_Embeddings/confusion_matrix.npy",
    cm
)

print("\nConfusion matrix saved.")
