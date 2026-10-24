
```markdown
# 🚀 sEMG Motion Prediction Project

근전도(sEMG) 신호를 활용한 동작 예측 및 성능 평가를 수행하는 머신러닝/딥러닝 프로젝트입니다[cite: 2].

---

## 1. 코드 설명[cite: 2]

본 과제에서 구현한 코드의 전체적인 내용을 간단히 설명한다[cite: 2].

### 사용한 데이터 및 전처리 방법[cite: 2]
- **데이터:** sEMG(근전도) 시계열 센서 데이터셋[cite: 2]
- **전처리 방법:** 노이즈 제거, 신호 필터링 및 모델 학습에 적합한 형태로 데이터 정제 및 스케일링 수행[cite: 2] (`src/01_preprocess.py`)[cite: 2]

### 사용한 AI/ML 모델[cite: 2]
- sEMG 신호 패턴을 학습하고 분류하기 위해 앙상블 기반의 **Random Forest** 모델 및 비교를 위한 **SVM** 모델을 구축하였습니다[cite: 2, 3] (`src/02_train_evaluate.py`)[cite: 2].

### 학습 및 테스트 방법[cite: 2]
- 데이터를 학습 및 테스트 셋으로 분할하고, 교차 검증(`src/03_cross_validation.py`)을 거쳐 모델의 일반화 성능을 객관적으로 평가했습니다[cite: 2]. 또한 연산 비용 및 효율성을 함께 분석했습니다[cite: 2] (`src/04_compute_cost.py`)[cite: 2].

### 실행 방법[cite: 2]
프로젝트에 필요한 실행 방법은 다음과 같습니다[cite: 2]:
```bash
python src/01_preprocess.py
python src/02_train_evaluate.py
python src/03_cross_validation.py
python src/04_compute_cost.py

```

### 코드 설명



각 코드 파일의 역할을 간단히 설명한다.

| 파일명 | 설명

 |
| --- | --- |
| `src/01_preprocess.py` | sEMG 신호 데이터 전처리 및 정제

 |
| `src/02_train_evaluate.py` | 모델 학습 및 성능 평가

 |
| `src/03_cross_validation.py` | 교차 검증(Cross-Validation) 수행

 |
| `src/04_compute_cost.py` | 연산 비용 및 효율성 분석

 |

---

## 2. 모델 성능 비교



2개 이상의 모델을 사용하여 성능을 비교한다.

| Model | Accuracy | Precision | Recall | F1-score |
| --- | --- | --- | --- | --- |
| **Random Forest (Model 1)**

 | 0.743 | 0.745 | 0.743 | 0.744 |
| **SVM (Model 2)**

 | 0.698 | 0.695 | 0.698 | 0.696 |

### 성능 분석



* Random Forest 모델이 가장 높은 F1-score를 나타냈으며, 대부분의 클래스에서 안정적인 분류 성능을 보였다.



---

## 3. Confusion Matrix 분석



각 모델의 Confusion Matrix를 첨부한다.

### Random Forest (Model 1)



**분석:**

* **가장 잘 분류된 클래스:** `30 open_` (1,920건 정분류)


* **가장 많이 오분류된 클래스:** `60 fist_` (`30 fist_`로 191건 오분류)


* **주요 오분류 유형:** 동일한 형태의 동작(주먹 쥐기, 손 펴기 등)이지만 각도 조건(`30도` vs `60도`)이 다른 클래스 간의 혼동


* **오분류가 발생한 이유에 대한 분석:** 관절 각도 변화에 따른 sEMG 신호의 패턴 차이가 미세하여, 특징 추출 단계에서 일부 구간이 인접 조건의 클래스로 중복 인식되었기 때문



---

## 4. 최종 결과



실험 결과를 간단히 정리한다.

* **가장 성능이 좋은 모델:** Random Forest (Model 1)


* **가장 성능이 낮은 모델:** SVM (Model 2)


* **주요 오분류 클래스:** `30 fist_`와 `60 fist_`, `30 open_`과 `60 open_` 등 각도별 유사 동작 클래스 간 상호 오분류


* **전체적인 실험 결과 및 느낀 점:** sEMG 신호 처리 시 각도 조건에 따른 물리적 신호 변동성을 세밀하게 반영하는 전처리가 성능 향상의 핵심임을 확인했으며, 교차 검증을 통해 과적합 없이 신뢰성 있는 성능 평가를 수행하는 방법을 체득함



```

