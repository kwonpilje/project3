# 1. 라이브러리 불러오기
from sklearn.ensemble import RandomForestClassifier
import joblib
import pandas as pd
import numpy as np

# 2. 모델 준비

# 2-1. 훈련 데이터 불러오기
df = pd.read_csv('flight_data_copy_csv_practice.csv')

# 2-2. 데이터 분리하기
target = "target"

X_train = df.drop(columns=target)
y_train = df[target]

# 2-3. randomforest 인스턴스 선언하기
model_rf = RandomForestClassifier(random_state=1)

# 2-4. 학습하기
model_rf.fit(X_train, y_train)

# 3. 모델 저장하기
joblib.dump(model_rf, "./flask_app/services/model.pkl")




