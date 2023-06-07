import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import tensorflow as tf 
tf.random.set_seed(337) # 초기 가중치가 고정되지만, 연산하면서 고정된게 틀어진다. 
# 역전파하면서 값이 틀어진다. => 가중치 저장이 중요한 것 

# 1. 데이터
x = np.array([1,2,3,4,5])
y = np.array([1,2,3,4,5])

# 2. 모델
model = Sequential()
# [[0.94719875, 0.4854678 , 0.43610287]] 3노드의 임의 웨이트값 
model.add(Dense(3, input_dim = 1))
model.add(Dense(2))
model.add(Dense(1))
model.summary()
'''
Total params: 17
Trainable params: 17
Non-trainable params: 0
'''
print('==========================================================================================================================')
print('==========================================================================================================================')

print(model.weights)

'''
[<tf.Variable 'dense/kernel:0' shape=(1, 3) dtype=float32, 
numpy=array([[0.94719875, 0.4854678 , 0.43610287]], #  3노드의 임의 웨이트값 
dtype=float32)>, <tf.Variable 'dense/bias:0' shape=(3,) dtype=float32, numpy=array([0., 0., 0.], dtype=float32)>, <tf.Variable 'dense_1/kernel:0' shape=(3, 2) dtype=float32, numpy=
array([[0.77921295, 0.11311173],
       [0.6042062 , 0.6113721 ],
       [0.3735602 , 0.6884283 ]],' # 6개의 웨이트 생성되어있음 노드 끼리 연결된게 6개라서 그렇다. 
       dtype=float32)>, <tf.Variable 
       'dense_1/bias:0' - > # 바이어스의 값 
       shape=(2,) dtype=float32, numpy=array([0., 0.], dtype=float32)>, <tf.Variable 'dense_2/kernel:0' shape=(2, 1) dtype=float32, numpy=
array(
    [[ 1.3816797 ],[-0.24688137]], # 2개의 웨이트, 
    dtype=float32)>, <tf.Variable 'dense_2/bias:0' shape=(1,) dtype=float32, numpy=array([0.], dtype=float32)>]
'''

print('==========================================================================================================================')
print('==========================================================================================================================')
print(model.trainable_weights) # model.weights와 값이 똑같음
print('==========================================================================================================================')
print('==========================================================================================================================')
print(len(model.weights)) # 6 # 레이어 3 x (노드 +바이어스 ) # 노드랑 바이어스 각 한개로 생각해서 
print(len(model.trainable_weights)) # 6
##########################################################
model.trainable = False # ★★★
##########################################################

print(len(model.weights)) # 6
print(len(model.trainable_weights)) # 0

print('==========================================================================================================================')
print(model.weights) # []
print('==========================================================================================================================')
print(model.trainable_weights) # []
print('==========================================================================================================================')
model.summary()
'''
Total params: 17
Trainable params: 0
Non-trainable params: 17
훈련을 안시켜야하는 모델이 있다.
부스팅계열은 안고정해도 그대로 나오는 경우도 있음 
딥러닝은 시드 고정해도 틀어지는 경우도 생김 
가중치 가져다 사용한다는건 훈련안시키는 것 

전이 학습 | 구글 랩 ,  vgg 
어차피 괜찮으걸 재학습(가중치 찾기)을 시켜야하는가? 
와꾸가 달라도 같은 분류계열, 회귀 계열이라면 잘 맞는다. 
그래서 따로 가져와서 훈련시키지 않는다. 
새로운 데이터로 훈련시키면 오히려 안좋을수도 있다. 
그래서 훈련하는 것을 꺼두는 것임 # Non-trainable params: 17

모델과 그 가중치가 받아들일수있는 쉐이프로 바꾸기 
입출력만 다시 커스터 마이징 하면 된다. 



'''
