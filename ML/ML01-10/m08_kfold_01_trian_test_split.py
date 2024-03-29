import numpy as np
from sklearn.datasets import load_wine, load_digits, load_breast_cancer, fetch_covtype, load_iris, load_diabetes
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MaxAbsScaler, RobustScaler, MinMaxScaler, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.utils import all_estimators

import warnings
warnings.filterwarnings('ignore')

#1. 데이터
datasets=[load_iris(return_X_y=True),
       load_breast_cancer(return_X_y=True),
       load_wine(return_X_y=True),
       load_digits(return_X_y=True)] 
datasets_name = ['아이리스', '캔서', '와인', '비아벳']
n_splits = 5
kfold = KFold(n_splits = n_splits,
      shuffle=True,  
      random_state=123
      )
max_r2 = 0
for index, value in enumerate(datasets) : 
    #1. 데이터 
    x,y = value
    #2. 모델 구성 
    allAlgoritms = all_estimators(type_filter='classifier')
    for (name,algorithm) in allAlgoritms :
        try:
            model = algorithm()
            scores = cross_val_score(model,x,y,cv=kfold)
            results = round(np.mean(scores),4)
            if max_score < results :
                max_score = results
                max_name = name
            # 1등에서 3등까지하려면 if문을 세개까지하면된다.  
        except : 
            continue
    print('===============',datasets_name[index],'====================')
    print('최고 모델 : ',max_name,max_score)
'''
=========== 아이리스 ==========
최고모델 : GaussianProcessClassifier 
Score: 0.9852 
ACC: 0.8
=================================
=========== 캔서 ==========
최고모델 : ExtraTreesClassifier 
Score: 0.9667 
ACC: 0.9122807017543859
=================================
=========== 와인 ==========
최고모델 : ExtraTreesClassifier 
Score: 0.9875 
ACC: 0.5
=================================
=========== 디지트 ==========    
최고모델 : SVC 
Score: 0.9901 
ACC: 0.9166666666666666
=================================

'''
