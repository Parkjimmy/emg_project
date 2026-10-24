import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import os

# 1. 데이터 로드
data = np.load('data/dataset.npz', allow_pickle=True)
Xtr, ytr, Xte, yte = data['Xtr'], data['ytr'], data['Xte'], data['yte']

# 2. 라벨 인코딩 (문자열 라벨을 숫자로 변환)
le = LabelEncoder()
ytr_enc = le.fit_transform(ytr)
yte_enc = le.transform(yte)

# 3. 특징 표준화 (StandardScaler)
scaler = StandardScaler()
Xtr_scaled = scaler.fit_transform(Xtr)
Xte_scaled = scaler.transform(Xte)

# 4. 모델 정의 (XGBoost GPU 가속 설정 포함)
models = {
    'SVM': SVC(kernel='rbf', C=1.0, gamma='scale', decision_function_shape='ovr', random_state=42),
    'RF': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
    'XGB': XGBClassifier(n_estimators=400, max_depth=6, learning_rate=0.05, 
                         subsample=0.9, colsample_bytree=0.8, random_state=42, 
                         tree_method='hist', device='cuda')
}

# 5. Hold-out 평가 수행
rows = []
trained_models = {}

for k, m in models.items():
    m.fit(Xtr_scaled, ytr_enc)
    trained_models[k] = m
    p = m.predict(Xte_scaled)
    
    rows.append([
        k,
        accuracy_score(yte_enc, p),
        precision_score(yte_enc, p, average='macro', zero_division=0),
        recall_score(yte_enc, p, average='macro', zero_division=0),
        f1_score(yte_enc, p, average='macro', zero_division=0)
    ])

df = pd.DataFrame(rows, columns=['model', 'acc', 'precision', 'recall', 'f1'])
print("=== Hold-out 평가 결과 ===")
print(df.round(4))

# 6. 혼동행렬(Confusion Matrix) 시각화 및 저장 (Random Forest 기준)
os.makedirs('outputs', exist_ok=True)
cm = confusion_matrix(yte_enc, trained_models['RF'].predict(Xte_scaled))
fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(cm, cmap='Blues')
ax.set_xticks(range(len(le.classes_)))
ax.set_yticks(range(len(le.classes_)))
ax.set_xticklabels(le.classes_, rotation=45, ha='right')
ax.set_yticklabels(le.classes_)

for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        if cm[i, j]:
            ax.text(j, i, cm[i, j], ha='center', va='center', fontsize=8)

plt.colorbar(im)
plt.title('Confusion Matrix - Random Forest')
plt.tight_layout()
plt.savefig('outputs/confusion8.png', dpi=120)
print("혼동행렬 저장 완료: outputs/confusion8.png")