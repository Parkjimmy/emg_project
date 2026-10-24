
```markdown
# sEMG 팔동작 및 팔꿈치 각도 동시 분류 프로젝트
> Simultaneous Classification of Hand Gestures and Elbow Angles using sEMG Signals

본 프로젝트는 전완(Forearm)과 상완(Upper Arm)의 5채널 표면 근전도(sEMG) 생체 신호를 활용하여 손동작 4종과 팔꿈치 관절 각도 2종이 결합된 8개 다차원 동작 클래스(8-Class)를 동시에 분류하는 경량 머신러닝 파이프라인 재현 및 성능 비교 연구입니다.

---

## 📌 목차
1. 프로젝트 개요
2. 코드 설명 및 사용 방법
3. 모델 성능 비교
4. Confusion Matrix 분석
5. 최종 결과 및 결론

---

## 1. 프로젝트 개요

* 연구 목적: IMU와 같은 보조 센서 추가나 고비용 딥러닝 모델 없이, 5채널 sEMG 신호와 경량 머신러닝 알고리즘만으로 동작 유형과 관절 각도를 동시에 식별할 수 있는 예비 타당성(Pre-feasibility) 검증.
* 데이터셋 구성:
  * 피험자: 총 8명 (남성 5명, 여성 3명, 평균 연령 23 ± 2세, 오른손잡이)
  * 채널 구성 (5채널): 
    * 전완(Forearm) 3채널: ECR (요측수근신근), ED (총지신근), FDS (천지굴근)
    * 상완(Upper Arm) 2채널: BB (상완이두근), TB (상완삼두근)
  * 샘플링 주파수: 1,000 Hz (IX-BIO8 장비 사용)
* 클래스 정의 (4 Gestures x 2 Angles = 8-Class):
  * 손동작 (4종): extor (손목 신전/회외), fist (주먹 쥐기), open (손 펴기), pro (회내)
  * 팔꿈치 각도 (2종): 30도, 60도

---

## 2. 코드 설명 및 사용 방법

### 데이터 전처리 및 특징 추출 파이프라인
1. 신호 필터링:
   * 60 Hz Notch Filter: 상용 전원선 간섭 잡음 제거
   * 20 ~ 450 Hz 4차 Butterworth Bandpass Filter: sEMG 주요 유효 생체 신호 대역 보존
2. 슬라이딩 윈도잉 (Sliding Window):
   * 2초 세그먼트 signal -> 200 ms 윈도우 크기, 50% 오버랩 (100 ms 이동) 적용 (세그먼트당 19개 윈도우 생성)
3. 시간영역(Time Domain, TD) 특징 추출 (25 차원):
   * 각 윈도우 및 채널별 5종 특징 산출: RMS (근수축 강도), MAV (평균 진폭), WL (파형 누적 길이), ZC (부호 변화 횟수, threshold=0.01), SSC (기울기 방향 전환 횟수)
   * 5 채널 x 5 특징 = 25차원 특징 벡터
4. 특징 표준화:
   * StandardScaler (z-score normalization) 적용

---

### 프로젝트 코드 구조

```text
.
├── outputs/
│   └── confusion8.png   # 혼동행렬 (Confusion Matrix) 결과 이미지
├── src/
│   ├── main.py          # 전체 실험 실행 메인 스크립트
│   ├── data.py          # sEMG 신호 로딩, 전처리, 윈도잉 및 25D 특징 추출 모듈
│   ├── model.py         # SVM, Random Forest, XGBoost 모델 생성 및 설정
│   └── evaluation.py    # Hold-out, 5-Fold 교차검증, Confusion Matrix 시각화 및 t-검정
├── .gitignore
├── requirements.txt
└── README.md            # 프로젝트 결과 문서

```

| 파일명 | 역할 및 주요 기능 |
| --- | --- |
| main.py | 파이프라인 전체를 제어하며 학습, 검증, 성능 비교 및 리포트를 한 번에 실행 |
| data.py | 원시 EMG 신호에 필터링(Notch+BPF)을 적용하고 25차원 TD 특징 벡터 집합 생성 |
| model.py | 분류 모델(RF, SVM, XGBoost)의 하이퍼파라미터 및 인스턴스 정의 |
| evaluation.py | 성능 평가 지표(Accuracy, Precision, Recall, F1) 계산, 통계 검정, Confusion Matrix 시각화 |

---

### 실행 방법

```bash
# 환경 설정 및 의존성 패키지 설치
pip install -r requirements.txt

# 메인 실행 스크립트 동작
python src/main.py

```

---

## 3. 모델 성능 비교

### Hold-out 평가 결과 (80% Train / 20% Test)

| Model | Accuracy | Precision | Recall | F1-score |
| --- | --- | --- | --- | --- |
| Random Forest | 0.9688 | 0.9695 | 0.9688 | 0.9687 |
| Support Vector Machine (SVM) | 0.9635 | 0.9641 | 0.9635 | 0.9635 |
| XGBoost | 0.9557 | 0.9567 | 0.9557 | 0.9559 |

---

### 5-Fold Stratified Cross-Validation 결과

| Model | 5-Fold Mean Accuracy | Standard Deviation (+/-) | 학습 시간 (s) | 샘플당 추론 속도 (ms) |
| --- | --- | --- | --- | --- |
| Random Forest | 96.72 % | +/- 0.58 % | 0.313 s | 0.036 ms |
| XGBoost | 96.15 % | +/- 0.56 % | 19.846 s | 0.031 ms |
| SVM | 95.83 % | +/- 0.79 % | 0.334 s | 0.382 ms |

* 대응표본 t-검정 (Paired t-test) 결과:
* RF vs SVM: p = 0.1193 (유의하지 않음)
* RF vs XGBoost: p = 0.1609 (유의하지 않음)
* SVM vs XGBoost: p = 0.3739 (유의하지 않음)
* 해석: 세 모델 간 최고 정확도 차이는 통계적으로 유의수준 alpha = 0.05에서 유의하지 않았습니다. 따라서 실시간 임베디드 제어 관점에서는 학습 시간이 매우 짧고 추론 속도가 안정적인 Random Forest가 가장 최선의 모델로 선정되었습니다.



---

## 4. Confusion Matrix 분석

<img width="720" height="600" alt="confusion8" src="https://github.com/user-attachments/assets/59c5dfb1-369a-415b-a75a-709b69143ce8" />

### Random Forest Confusion Matrix 상세 분석 (윈도우 단위 집계)

* 최고 식별 클래스:
* 30 open_: 1,920건 정답 (최고 정확도)
* 30 fist_: 1,915건 정답
* 30 extor_: 1,848건 정답
* 60 open_: 1,798건 정답


* 최다 오분류 클래스:
* 60 fist_: 1,693건 정답 / 오분류 673건 발생
* 30 pro_: 1,742건 정답 / 오분류 599건 발생


* 주요 오분류 패턴 분석:
1. 동일 동작 내 팔꿈치 각도 간 오분류 (60도 -> 30도):
* 60 fist_ -> 30 fist_: 191건 오분류
* 60 pro_ -> 30 pro_: 166건 오분류
* 60 open_ -> 30 open_: 160건 오분류


2. 동일 각도 내 유사 손동작 간 상호 혼동:
* 30 pro_ -> 30 extor_: 156건 오분류
* 30 extor_ -> 30 pro_: 130건 오분류




* 오분류 원인 성찰:
* 손동작 변경 시에는 주동근/길항근의 동원 형태가 크게 바뀌어 뚜렷한 근활성 지표 차이를 형성합니다.
* 반면, 팔꿈치 관절 각도 변화(30도 <-> 60도)에 따른 근활성 진폭 및 형태 변화는 상대적으로 미세합니다. 시간영역(TD) 특징만으로는 관절 각도 변환에 따른 주파수 성분의 특성을 완전히 포착하기 어려워 동일 동작 내 각도 오분류가 주된 오류 원인으로 나타났습니다.



---

## 5. 최종 결과 및 결론

* 최고 성능 모델: Random Forest (Test Accuracy: 96.88%, F1-Score: 0.9687, 5-Fold CV: 96.72%)
* 최다 오분류 패턴: 동일한 손동작을 수행할 때 팔꿈치 관절 각도(60도 -> 30도)를 잘못 식별하는 현상
* 프로젝트 핵심 시사점:
1. 추가적인 IMU 관절 센서 탑재 없이 전완/상완 5채널 표면 근전도 신호만으로 손동작과 팔꿈치 각도가 결합된 8가지 다차원 의도를 96% 이상의 고정밀도로 동시 식별 가능함을 검증함.
2. 단순 정확도뿐만 아니라 통계적 검정(p > 0.05) 및 학습/추론 연산 시간까지 복합적으로 평가하여, 실용적 임베디드 의수/재활 기기 제어에 최적화된 경량 모델(Random Forest)을 선정함.
3. 연구 한계 및 향후 발전 방향:
* Trial-wise 분할의 한계: 동일 피험자의 데이터가 학습/테스트에 함께 분포하므로 미지의 피험자에 대한 LOSO(Leave-One-Subject-Out) 교차검증 추가 필요.
* 특징 영역 확장: 각도 구분력 향상을 위해 주파수영역(MNF, MDF) 및 시간-주파수 영역 특징과의 결합 연구가 권장됨.





```

```
