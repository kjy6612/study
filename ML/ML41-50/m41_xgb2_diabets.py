# 리그레서로 해서 분류랑 비교

    # "n_estimators" : [100,200,300,400,500,600], # 디폴트 100 / 1 ~ inf / 정수
    # "learning_rate" : [0.1,0.2,0.3,0.5,1,0.01,0.001], # 디폴트 0.3 / 0 ~ 1 / eta
    # "max_depth" : [None,2,3,4,5,6,7,8,9,10], # 디폴트 6 / 0 ~ inf / 정수
    # "gamma" : [0,1,2,3,4,5,7,8,9,10], # 디폴트 0 / 0 ~ inf 
    # "min_child_weight" : [0,0.1,0.01,0.001,0.5,1,5,10,100], # 디폴트 1 / 0 ~ inf 
    # "subsample" : [0,0.1,0.2,0.3,0.5,0.7,1], # 디폴트 1 / 0 ~ 1 
    # "colsample_bytree" : [0,0.1,0.2,0.3,0.5,0.7,1], # 디폴트 / 0 ~ 1 
    # "colsample_bylevel":[0,0.1,0.2,0.3,0.5,0.7,1], # 디폴트 / 0 ~ 1 
    # "colsample_bynode":[0,0.1,0.2,0.3,0.5,0.7,1], # 디폴트 / 0 ~ 1 
    # "reg_alpha":[0,0.1,0.01,0.001,1,2,10], # 디폴트 0 / 0 ~ inf / L1 절대값 가중치 규제 / alpha
    # "reg_lambda":[0,0.1,0.01,0.001,1,2,10], # 디폴트 1 / 0 ~ inf / L2 제곱 가중치 규제 / lambda
import numpy as np
import pandas as pd
from xgboost import XGBClassifier, XGBRegressor
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold, StratifiedKFold, GridSearchCV, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler,MinMaxScaler,MaxAbsScaler,RobustScaler

# 1.데이터 
x,y = load_breast_cancer(return_X_y=True)

x_train, x_test, y_train,y_test = train_test_split(
    x,y, random_state=337,train_size=0.8,stratify=y
)


x_train= RobustScaler().fit_transform(x_train)
x_test= RobustScaler().fit_transform(x_test)

n_split = 5
kfold = StratifiedKFold(n_splits=n_split)
parameter =  {
    "n_estimators" : [100], # 디폴트 100 / 1 ~ inf / 정수
    "learning_rate" : [0.5], # 디폴트 0.3 / 0 ~ 1 / eta
    "max_depth" : [3], # 디폴트 6 / 0 ~ inf / 정수
    "gamma" : [0], # 디폴트 0 / 0 ~ inf 
    "min_child_weight" : [5], # 디폴트 1 / 0 ~ inf 
    "subsample" : [1], # 디폴트 1 / 0 ~ 1 
    "colsample_bytree" : [0.3], # 디폴트 / 0 ~ 1 
    "colsample_bylevel":[1], # 디폴트 / 0 ~ 1 
    "colsample_bynode":[1], # 디폴트 / 0 ~ 1 
    "reg_alpha":[1], # 디폴트 0 / 0 ~ inf / L1 절대값 가중치 규제 / alpha
    "reg_lambda":[0.001], # 디폴트 1 / 0 ~ inf / L2 제곱 가중치 규제 / lambda
}

#2. 모델 
xgb = XGBRegressor(random_state=1234)
model = XGBRegressor(random_state=1234)
model = GridSearchCV(xgb,parameter,cv=kfold,n_jobs=-1)

# 3. 훈련
model.fit(x_train,y_train)

# 4. 평가, 예측 
print("최상의 매개변수 : ",model.best_params_)
print("최상의 매개변수 : ",model.best_score_)
result = model.score(x_test,y_test)
print("최종점수 : ", result)

'''
그냥 돌렸을 때 
최종점수 :  0.6365166363751928

최상의 매개변수 :  {'colsample_bylevel': 1, 'colsample_bynode': 1, 'colsample_bytree': 0.3, 'gamma': 
0, 'learning_rate': 0.5, 'max_depth': 3, 'min_child_weight': 5, 'n_estimators': 100, 'reg_alpha': 1, 
'reg_lambda': 0.001, 'subsample': 1}
최상의 매개변수 :  0.8783374214281701
최종점수 :  0.680229131710399

'''
