import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.base import clone
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from scipy.stats import ttest_rel
from itertools import combinations

print("데이터 로딩 중...")
data = np.load('data/dataset.npz', allow_pickle=True)
X_all = np.vstack([data['Xtr'], data['Xte']])
y_all = np.concatenate([data['ytr'], data['yte']])

le = LabelEncoder()
y_all_enc = le.fit_transform(y_all)

models = {
    'SVM': SVC(kernel='rbf', C=1.0, gamma='scale', decision_function_shape='ovr', random_state=42),
    'RF': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
    'XGB': XGBClassifier(n_estimators=400, max_depth=6, learning_rate=0.05, 
                         subsample=0.9, colsample_bytree=0.8, random_state=42, 
                         tree_method='hist', device='cuda')
}

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
fold_acc = {k: [] for k in models}

print("5-Fold 교차검증 시작 (모델 학습 중)...")
for fold_idx, (tr_i, va_i) in enumerate(skf.split(X_all, y_all_enc), 1):
    print(f"\n--- [Fold {fold_idx}/5] 진행 중 ---")
    Xa, ya = X_all[tr_i], y_all_enc[tr_i]
    Xb, yb = X_all[va_i], y_all_enc[va_i]
    
    sc = StandardScaler()
    Xa = sc.fit_transform(Xa)
    Xb = sc.transform(Xb)
    
    for k, proto in models.items():
        print(f"  > {k} 모델 학습 및 평가 중...")
        m = clone(proto)
        m.fit(Xa, ya)
        acc = m.score(Xb, yb)
        fold_acc[k].append(acc)

print("\n=== 5-Fold 교차검증 결과 ===")
for k, v in fold_acc.items():
    print(f'{k}: {np.mean(v)*100:.2f} ± {np.std(v)*100:.2f} %')

print("\n=== 대응표본 t-검정 (Paired t-test) 결과 ===")
for a, b in combinations(models.keys(), 2):
    t, p = ttest_rel(fold_acc[a], fold_acc[b])
    verdict = '유의함 (차이 있음)' if p < 0.05 else '유의하지 않음 (차이 없음)'
    print(f'{a} vs {b}: p = {p:.4f} -> {verdict}')