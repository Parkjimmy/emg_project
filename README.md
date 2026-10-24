
```markdown
# 🚀 sEMG Motion Prediction Project

근전도(sEMG) 신호를 활용한 동작 예측 및 성능 평가를 수행하는 머신러닝/딥러닝 프로젝트입니다[cite: 2].

---

## 1. 코드 설명[cite: 2]

### 사용한 데이터 및 전처리 방법[cite: 2]
- **데이터:** sEMG(근전도) 시계열 센서 데이터셋[cite: 2]
- **전처리 방법:** 잡음 제거, 필터링 및 모델 학습에 적합한 형태로 데이터 정제 및 스케일링 수행[cite: 2] (`src/01_preprocess.py`)[cite: 2]

### 사용한 AI/ML 모델[cite: 2]
- sEMG 신호 패턴을 학습하고 분류하기 위해 머신러닝 및 분류 모델을 구축하였습니다[cite: 2]. (`src/02_train_evaluate.py`)[cite: 2]

### 학습 및 테스트 방법[cite: 2]
- 데이터를 학습/테스트셋으로 분할하고, 교차 검증(`src/03_cross_validation.py`)을 거쳐 모델의 일반화 성능을 객관적으로 평가했습니다[cite: 2]. 또한 연산 비용 및 효율성을 함께 분석했습니다[cite: 2] (`src/04_compute_cost.py`)[cite: 2].

### 코드 실행 방법[cite: 2]
```bash
python src/01_preprocess.py
python src/02_train_evaluate.py
python src/03_cross_validation.py
python src/04_compute_cost.py

```

### 파일 설명



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



2개 이상의 모델을 사용하여 성능을 비교한 결과입니다. *(※ 본인의 실제 실험 수치로 수정해 주세요)*

| Model | Accuracy | Precision | Recall | F1-score |
| --- | --- | --- | --- | --- |
| Model 1 (예: XGBoost) | 0.XX | 0.XX | 0.XX | 0.XX |
| Model 2 (예: Random Forest) | 0.XX | 0.XX | 0.XX | 0.XX |

### 성능 분석



* Model 1이 가장 높은 F1-score를 나타냈으며, 대부분의 클래스에서 안정적인 분류 성능을 보였다.



---

## 3. Confusion Matrix 분석



각 모델의 Confusion Matrix 결과입니다.

### Model 1 분석



* **가장 잘 분류된 클래스:** (예: 동작 A)


* **가장 많이 오분류된 클래스:** (예: 동작 B)


* **주요 오분류 유형:** 유사한 근육 수축 패턴을 가진 동작 간의 혼동


* **오분류가 발생한 이유에 대한 분석:** 두 동작 간 센서 신호의 물리적 특성이 유사하여 특징 추출 단계에서 구분이 명확하지 않았기 때문



---

## 4. 최종 결과



실험 결과를 간단히 정리합니다.

* **가장 성능이 좋은 모델:** Model 1


* **가장 성능이 낮은 모델:** Model 2


* **주요 오분류 클래스:** 유사 동작 클래스 간 상호 오분류


* **전체적인 실험 결과 및 느낀 점:** sEMG 신호의 특성상 노이즈 처리와 전처리 과정이 모델의 최종 성능에 결정적인 영향을 미친다는 것을 확인했으며, 교차 검증을 통해 과적합을 방지하는 방법을 체득함
