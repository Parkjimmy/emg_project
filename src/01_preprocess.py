import os
import glob
import numpy as np
import pandas as pd
from scipy.signal import butter, iirnotch, filtfilt

def apply_filters(raw_signal, fs=1000):
    # 60Hz 노치 필터 (전원선 간섭 제거)
    bn, an = iirnotch(60, 30, fs)
    filtered = filtfilt(bn, an, raw_signal, axis=0)
    
    # 20~450Hz 4차 Butterworth 대역통과 필터
    b, a = butter(4, [20/(fs/2), 450/(fs/2)], btype='band')
    filtered = filtfilt(b, a, filtered, axis=0)
    return filtered

def extract_time_domain_features(window_data, th=0.01):
    # window_data shape: (200, 5) -> 200샘플, 5채널
    d = np.diff(window_data, axis=0)
    rms = np.sqrt(np.mean(window_data**2, axis=0))
    mav = np.mean(np.abs(window_data), axis=0)
    wl = np.sum(np.abs(d), axis=0)
    zc = np.sum((window_data[:-1] * window_data[1:] < 0) & (np.abs(d) >= th), axis=0)
    ssc = np.sum((window_data[1:-1] - window_data[:-2]) * (window_data[1:-1] - window_data[2:]) > 0, axis=0)
    return np.concatenate([rms, mav, wl, zc, ssc]) # (25,)

def process_dataset():
    data_dir = 'data'
    csv_files = glob.glob(os.path.join(data_dir, '*.csv'))
    
    if not csv_files:
        print("경고: data/ 폴더에 CSV 파일이 없습니다. 경로를 확인해주세요.")
        return

    features = []
    labels = []

    window_size = 200  # 200 ms (at 1000Hz)
    step_size = 100    # 50% overlap (100 ms)

    for file_path in csv_files:
        filename = os.path.basename(file_path)
        # 파일명 형식 예: a_30 fist.csv -> 피험자: a, 각도: 30, 동작: fist
        parts = filename.replace('.csv', '').split('_')
        if len(parts) < 2:
            continue
        
        subject, angle = parts[0], parts[1]
        gesture = "_".join(parts[2:]) # 동작 이름 (fist, open 등)
        class_label = f"{angle}_{gesture}" # 예: 30_fist, 60_open 등

        # CSV 파일 로드 (상위 5개 채널 데이터를 sEMG 신호로 가정)
        df = pd.read_csv(file_path)
        raw_data = df.iloc[:, :5].values # 5채널 신호 추출 (Ch1 ~ Ch5)

        # 전처리 적용
        filtered_data = apply_filters(raw_data, fs=1000)

        # 슬라이딩 윈도우 적용 및 특징 추출
        for start in range(0, len(filtered_data) - window_size + 1, step_size):
            win = filtered_data[start:start + window_size]
            feat_vector = extract_time_domain_features(win)
            features.append(feat_vector)
            labels.append(class_label)

    X = np.array(features)
    y = np.array(labels)

    # Train / Test 분할 (예: 80% 학습, 20% 테스트)
    np.random.seed(42)
    indices = np.random.permutation(len(X))
    split_idx = int(len(X) * 0.8)
    
    train_idx, test_idx = indices[:split_idx], indices[split_idx:]
    Xtr, ytr = X[train_idx], y[train_idx]
    Xte, yte = X[test_idx], y[test_idx]

    np.savez('data/dataset.npz', Xtr=Xtr, ytr=ytr, Xte=Xte, yte=yte)
    print(f"전처리 완료! 저장된 데이터셋 모양 -> Xtr: {Xtr.shape}, Xte: {Xte.shape}")

if __name__ == "__main__":
    process_dataset()