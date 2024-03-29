'''
테스트 데이터는 훈련에 참여를 안한다. 
데이터 수집에 돈과 인력이 들어가는데, 
테스트 데이터는 훈련에 들어가지 않는것이 아깝다. 
그래서 아깝다고 생각해서 테스트 데이터도 훈련에 이용하고 시팓.
 그래서 나온 것이 크로스 발리데이션 안에  케이 폴드가 잇다. 
예시로 8:2  = train : test/val
순차적으로 앞으로 가면서 테스트 데이터를 하면 된다. 

나온평지표 값에 대한 평균 값을 사용할 수도 있고 잘 나온 값을 사용할 수도 있고 알아서 선택하기 
너무 잘나와도 과적합일 수도 있음
슬라이싱과 if과 for문을 사용하여 만들수 있다.  - 사이킷런에 만들어진 것이 잇다.

트레인 테스트 스플릿
'''

import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.metrics import accuracy_score
# 데이터 전처리 과정 

# 1. 데이터
x, y = load_iris(return_X_y=True)

# x_train, x_test, y_train, y_test = train_test_split(
#     x, y, shuffle=True random_state=123, test_size=0.2
# ) - 만약 이걸 햇다면 여기서 셔플 됏을 수도 잇다. 
n_splits = 5
kfold = KFold(n_splits = n_splits,#디폴트 5  옛날에는 3이였음 근데 바뀐거면 지금것이 좋다는 의미 
        # 데이터가 100프로라면 20프로씩 나눠질 것 
      shuffle=True,  # 처음에 섞고 나서 나중에 잘라서 테스트, 테스트 할때 마다 섞는건 아님 
      #테스트 할 때마다 셔플하면 겹치는 것이 있다. 
      # 수치가 얼마나 좋은지는 데이터의 크기마다 다르다. 
      # 셔플의 디폴트 false
      random_state=123,
      )

# 2. 모델
from sklearn.svm import LinearSVC
model = LinearSVC()

#3, 4. 컴파일, 훈련 ,평가, 예측
#scores = cross_val_score(model,x,y,cv = kfold)
#크로스 발리데이션에서 스코어를 배주는 것 
# ( 모델, 데이터, 크로스 발리데이션 어떻게 할것 인지)
scores = cross_val_score(model,x,y,cv =5) # 회귀일 경우 r2 
# 정의할 필요 없이 그냥 5번 해보자! 이렇게도 되지만 셔플이나 랜덤 스테이트 같은 것이 있기에 그냥 할지 말지 알아서 하기 
# n_jobs : 사용하는 코어의 갯수 
# n_jobs = -1, 최대 코어 사용할거야 라는 말 
print('acc : ',scores,'\n cross_val_score 평균 : ',round(np.mean(scores),4))
