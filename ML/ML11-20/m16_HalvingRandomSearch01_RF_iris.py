#실습 
# #분류
# 1. iris 
# 2. cancer
# 3. dacon_diabets
# 4. wine
# 5. fetch_covtype
# 6. digits

#모델 : RandomForestClassifier
# parameters = [
#     {'n_estimators' : [100,200]},
#     {'max_depth' : [6,8,10,12]},
#     {'min_samples_leaf' : [3,5,7,10]},
#     {'min_samples_split' : [2,3,5,10]},
#     {'n_jobs' : [-1, 2, 4]}]
#파라미터 조합으로 2개 이상 엮을 것
####################################################
import time
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold, cross_val_score, StratifiedKFold
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.preprocessing import MaxAbsScaler, RobustScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV   
from sklearn.experimental import enable_halving_search_cv
from sklearn.model_selection import HalvingGridSearchCV, HalvingRandomSearchCV
from sklearn.metrics import accuracy_score

#1. 데이터 
x, y = load_iris(return_X_y=True)

x_train, x_test, y_train, y_test = train_test_split(
    x, y, shuffle=True, random_state=42, test_size=0.2
)

scaler = MinMaxScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.fit_transform(x_test)


n_splits = 5
kfold = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=337)


parameters = [
    {'n_estimators' : [100,200], 'max_depth' : [6,8,10,12], 'min_samples_leaf' : [3,5,7,10]},
    {'max_depth' : [6,8,10,12], 'min_samples_leaf' : [3,5,7,10]},
    {'min_samples_leaf' : [3,5,7,10], 'min_samples_split' : [2,3,5,10]},
    {'min_samples_split' : [2,3,5,10]},
  ]

#2. 모델 
model = HalvingRandomSearchCV(RandomForestClassifier(), parameters,factor=3,
                     cv=kfold, verbose=1, refit=True, n_jobs=-1)

#3. 컴파일, 훈련 
start_time = time.time()
model.fit(x_train, y_train)
end_time = time.time()

print("최적의 매개변수:", model.best_estimator_) 
print("최적의 파라미터:", model.best_params_)
print("best_score:", model.best_score_)
print("model.score:", model.score(x_test, y_test))
print("걸린시간 :", round(end_time-start_time,2), "초")

#4. 평가, 예측
y_predict = model.predict(x_test)
print("accuracy_score:", accuracy_score(y_test, y_predict))

y_pred_best = model.best_estimator_.predict(x_test)            
print("최적 튠 ACC:", accuracy_score(y_test, y_pred_best))

#HalvingRandomSearchCV
'''
최적의 매개변수: RandomForestClassifier(max_depth=10, min_samples_leaf=3, n_estimators=200)
최적의 파라미터: {'n_estimators': 200, 'min_samples_leaf': 3, 'max_depth': 10}
best_score: 0.9555555555555555
model.score: 0.9666666666666667
걸린시간 : 5.16 초
accuracy_score: 0.9666666666666667
최적 튠 ACC: 0.9666666666666667
----------------------------------------
최적의 매개변수: RandomForestClassifier(max_depth=8, min_samples_leaf=7)
최적의 파라미터: {'n_estimators': 100, 'min_samples_leaf': 7, 'max_depth': 8}
best_score: 0.9555555555555555
model.score: 1.0
걸린시간 : 5.04 초
accuracy_score: 1.0
최적 튠 ACC: 1.0
'''
#HalvingGridSearchCV
'''
최적의 매개변수: RandomForestClassifier(max_depth=8, min_samples_leaf=5, n_estimators=200)
최적의 파라미터: {'max_depth': 8, 'min_samples_leaf': 5, 'n_estimators': 200}
best_score: 0.9555555555555555
model.score: 1.0
걸린시간 : 22.19 초
accuracy_score: 1.0
최적 튠 ACC: 1.0
'''
#RandomizedSearchCV
'''
Fitting 5 folds for each of 10 candidates, totalling 50 fits
최적의 매개변수: RandomForestClassifier(max_depth=12, min_samples_leaf=7, n_estimators=200)
최적의 파라미터: {'n_estimators': 200, 'min_samples_leaf': 7, 'max_depth': 12}
best_score: 0.9583333333333333
model.score: 1.0  
걸린시간 : 5.11 초
accuracy_score: 1.0
최적 튠 ACC: 1.0
'''
#GridSearchCV
'''
Fitting 5 folds for each of 68 candidates, totalling 340 fits
최적의 매개변수: RandomForestClassifier(max_depth=6, min_samples_leaf=3)
최적의 파라미터: {'max_depth': 6, 'min_samples_leaf': 3, 'n_estimators': 100}
best_score: 0.9583333333333333
model.score: 1.0
걸린시간 : 17.21 초
accuracy_score: 1.0
최적 튠 ACC: 1.0
'''