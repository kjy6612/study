import numpy as np
from sklearn.datasets import load_iris
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.pipeline import make_pipeline, Pipeline
#make_pipeline : 함수
#Pipeline : 클래스

#1. 데이터 
x,y = load_iris(return_X_y=True)

x_train, x_test, y_train, y_test = train_test_split(
    x, y, train_size=0.8, shuffle=True, random_state=337
)

#scaler +모델 합침
# model = make_pipeline(MinMaxScaler(), RandomForestClassifier())
# model = make_pipeline(StandardScaler(), RandomForestClassifier())
# model = Pipeline(StandardScaler(), SVC()) => # TypeError: __init__() takes 2 positional arguments but 3 were given 
model = Pipeline([('std', StandardScaler()), ('svc', SVC())])    #Pipeline은 list형식으로 입력받음 + 튜플 형태로 받음('이름 명시')


#3. 훈련 
model.fit(x_train, y_train)

#4. 평가, 예측
result = model.score(x_test, y_test)
print("model.score:", result)

y_predict = model.predict(x_test)
acc = accuracy_score(y_test, y_predict)
print("accuracy_score:", acc)

'''
#model = Pipeline([('std', StandardScaler()), ('svc', SVC())])
model.score: 0.9333333333333333
accuracy_score: 0.9333333333333333
'''
