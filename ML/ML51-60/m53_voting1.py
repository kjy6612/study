# 
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier


# 1. 데이터
x,y = load_breast_cancer(return_X_y=True)

x_train, x_test, y_train, y_test = train_test_split(
    x,y,random_state=337,train_size=0.8,shuffle=True,
    stratify=y
)
scaler = StandardScaler()
x_train =scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# 2. 모델 

from sklearn.ensemble import RandomForestClassifier, BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
lr = LogisticRegression()
knn = KNeighborsClassifier(n_neighbors=8)
dt =DecisionTreeClassifier()
# 고만고만한 친구들 
# model= DecisionTreeClassifier()
model = VotingClassifier(
    estimators=[('LR',lr),('KNN',knn),('DT',dt)], # # 이제 모델 작성  평가
    # voting = 'hard', # 디폴트는 hard
    voting = 'soft', # 디폴트는 hard
)
# 3. 훈련 
model.fit(x_train,y_train)
print(model)
print(model.__class__.__name__) # 모델 이름만 나옴 
# 4. 평가,예측
y_pred = model.predict(x_test)
print('model.score: ',model.score(x_test,y_test))
print('acc : ',accuracy_score(y_test,y_pred))

classifiers = [lr,knn,dt]
for model2 in classifiers :
    model2.fit(x_train,y_train)
    y_pred = model2.predict(x_test)
    score2= accuracy_score(y_test,y_pred)
    class_name = model2.__class__.__name__
    print("{0}정확도 : {1:.4f}".format(class_name,score2)) # 0 에 클래스 네임 , 스코어2는 1:4f 이고 소수 4번째 짜리 까지 
'''
acc :  0.9385964912280702
LogisticRegression정확도 : 0.9561
KNeighborsClassifier정확도 : 0.9737
DecisionTreeClassifier정확도 : 0.8860
단일 모델 보다 좋을 수도 있고 나쁠수도 있다. 알아서 잘 사용해야한다. 
'''
    



'''
랜덤포레스트
model.score:  0.9385964912280702
acc :  0.9385964912280702
'''
'''
배깅 부트스트랩 펄스
model.score:  0.9385964912280702
acc :  0.9385964912280702
'''
'''
배깅 부트스트랩 트루
model.score:  0.9385964912280702
acc :  0.9385964912280702
'''
'''
하드 보팅
model.score:  0.9736842105263158
acc :  0.9736842105263158   
'''
'''
soft 보팅
model.score:  0.9385964912280702
acc :  0.9385964912280702 
'''
'''
배깅 2개 랜덤포레스트 트루 
model.score:  0.9385964912280702
acc :  0.9385964912280702
'''
