import numpy as np 
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import r2_score
import warnings
warnings.filterwarnings('ignore')
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import all_estimators
import sklearn as sk
print(sk.__version__) # 1.0.2


# 1. 데이터
x,y = fetch_california_housing(return_X_y=True)

x_train, x_test, y_train, y_test = train_test_split(
    x,y, shuffle=True, random_state=123, test_size=0.2
)

scaler=RobustScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)


# 2. 모델 구성

# model = RandomForestClassifier(n_jobs=4)
allAlgoritms = all_estimators(type_filter='regressor')
#allAlgoritms = all_estimators(type_filter='classifier')

print('allAlgoritms : ',allAlgoritms)
#튜플 안에 첫번째는 스트링 형태의 모델, 두번째는 클래스로 정의된 모델
print(len(allAlgoritms)) #55

max_r2 = 0
max_name = '바보'
for (name, algoritm) in allAlgoritms :
    try: # 에외처리 
        model = algoritm()
        # 3. 훈련
        model.fit(x_train,y_train) # 모델 마다 형식이 다르다.
        # 4. 평가, 예측
        results = model.score(x_test,y_test)
        print( name ,'의 정답률 : ',results)
        
        if max_r2 < results:
            max_r2 = results
            max_name = name
        # y_pred = model.predict(x_test)
        # r2_score=r2_score(y_test,y_pred)
        # print("r2_score : ",r2_score)    
    except :  
         #에러가 뜨면 except로 바로 넘어간다. 에러가 안뜨면 정상적으로 for문이 돌아감.
        # 에러가 있을 때 실행하고 나서 다시 for문 실행
        print(name,' : 에러 모델')
        #에러가 난 모델은 안에 파라미터 넣어줘야하는 모델이다.
print('===================================')
print('최고 모델 : ',max_name, max_r2)
print('===================================')



'''
5번째부터 뭔가 넣어야 하는데 그렇지 않으면 오류가 남 
해결 방법은 에러가 나는 모델을 하지 말아주세요라고 부탁하기 
- 예외처리 
'''
