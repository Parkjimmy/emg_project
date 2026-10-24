import time
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

# 데이터 및 전처리
data = np.load('data/dataset.npz', allow_pickle=True)
Xtr, ytr, Xte, yte = data['Xtr'], data['ytr'], data['Xte'], data['yte']

le = LabelEncoder()
ytr_enc = le.fit_transform(ytr)
yte_enc = le.transform(yte)

scaler = StandardScaler()
Xtr_scaled = scaler.fit_transform(Xtr)
Xte_scaled = scaler.transform(Xte)

models = {
    'SVM': SVC(kernel='rbf', C=1.0, gamma='scale', decision_function_shape='ovr', random_state=42),
    'RF': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
    'XGB': XGBClassifier(n_estimators=400, max_depth=6, learning_rate=0.05, 
                         subsample=0.9, colsample_bytree=0.8, random_state=42, 
                         tree_method='hist', device='cuda')
}

print("=== 계산 비용 측정 결과 ===")
for k, m in models.items():
    # 학습 시간 측정
    t0 = time.time()
    m.fit(Xtr_scaled, ytr_enc)
    train_t = time.time() - t0
    
    # 추론 시간 측정 (100회 반복 평균)
    t0 = time.time()
    for _ in range(100):
        m.predict(Xte_scaled[:1])
    infer_ms = (time.time() - t0) * 10  # ms 단위 환산
    
    print(f'{k}: 학습 시간 {train_t:.3f}s, 추론 시간 {infer_ms:.3f} ms/sample')