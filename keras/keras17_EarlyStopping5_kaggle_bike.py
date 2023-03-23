#캐글 
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
import pandas as pd
# 여러 데이터를 읽기 쉽다.

# 1. 데이터
path = "./_data/kaggle/"
path_save = "./_save/kaggle/"
train_csv = pd.read_csv(path + 'train.csv',index_col=0)
print("train_csv : ",train_csv)
print("train_csv.shape : ", train_csv.shape)

test_csv = pd.read_csv(path + 'test.csv', index_col=0)
print(test_csv)
print("test_csv : ",test_csv)
print("test_csv.shape : ", test_csv.shape)
print("train_csv.columns : ",train_csv.columns) #test_csv.shape :  (6493, 8)
# train_csv.columns :  Index(['season', 'holiday', 'workingday', 'weather', 'temp', 'atemp',
#        'humidity', 'windspeed', 'casual', 'registered', 'count'],
#       dtype='object')
print('train_csv.info() : ',train_csv.info()) #train_csv.info() :  None
print('type(train_csv) : ',type(train_csv)) #type(train_csv) :  <class 'pandas.core.frame.DataFrame'>
#dtype: int64 (int= 정수)
#결측치 처리
print("isnull sum01 : ",train_csv.isnull().sum())
print(train_csv.shape)#(10886, 11)

train_csv = train_csv.dropna()
print('train_csv.info()02 :', train_csv.info())#None
print("isnull sum 02: ",train_csv.isnull().sum())
print(train_csv.shape)#(10886, 11)

# x와 y를 분리
x= train_csv.drop(['casual','registered','count'],axis=1) 
print("x : ",x)
print("x.shape : ",x.shape) #(10886, 8)
y=train_csv['count']
print("y : ",y)
print("y.shape : ",y.shape) #(10886,)

x_train, x_test, y_train, y_test = train_test_split(
    x,y,
    train_size=0.9, random_state= 1234
)
print("x_train.shape : ",x_train.shape ) #(7620, 10)
print("y_train.shape : ",y_train.shape ) #(7620,)

# 2. 모델구성
model=Sequential()
model.add(Dense(16,activation='relu',input_dim=8))
model.add(Dense(12,activation='relu'))
model.add(Dense(20,activation='relu'))
model.add(Dense(15,activation='relu'))
model.add(Dense(50,activation='relu'))
model.add(Dense(70))
model.add(Dense(50,activation='relu'))
model.add(Dense(25))
model.add(Dense(8))
model.add(Dense(4))
model.add(Dense(2))
model.add(Dense(1))

# 3. 컴파일, 훈련
model.compile(loss='mse',optimizer='adam')
from tensorflow.python.keras.callbacks import EarlyStopping
es = EarlyStopping(monitor='val_loss',patience=40,mode='min',
               verbose=1,restore_best_weights=True)
model.fit(x_train,y_train,epochs=2850,batch_size=4000,validation_split=0.2,verbose=1,callbacks=[es])

# 4. 평가, 예측
loss=model.evaluate(x_test,y_test)
print('loss : ',loss)
y_predict=model.predict(x_test)
r2=r2_score(y_test,y_predict)
print('r2 스코어 :',r2)
#rmse  만들기
def rmse(y_test,y_predict) :  #함수 정의만 한 것 
    return np.sqrt(mean_squared_error(y_test,y_predict))

rmse=rmse(y_test,y_predict)
print("rmse : ",rmse)



#submission.csv  만들기
y_submit = model.predict(test_csv)
#count에 넣기
submission = pd.read_csv(path+'sampleSubmission.csv',index_col=0)
submission['count'] = y_submit
submission.to_csv(path_save + 'submit_0314_02.csv')

'''
Dense : 
model.add(Dense(2,input_dim=8))
model.add(Dense(4))
model.add(Dense(10))
model.add(Dense(15))
model.add(Dense(32))
model.add(Dense(100))
model.add(Dense(50))
model.add(Dense(25))
model.add(Dense(12))
model.add(Dense(8))
model.add(Dense(6))
model.add(Dense(4))
model.add(Dense(2))
model.add(Dense(1))
epoch : 850
batch_size : 100
loss() :
r2스코어 : 
'''

"""
    validation_split=0.2  
    61/61 [==============================] - 0s 2ms/step - loss: 22093.4336 - val_loss: 23196.1133
103/103 [==============================] - 0s 968us/step - loss: 24305.5215
loss :  24305.521484375
103/103 [==============================] - 0s 890us/step
r2 스코어 : 0.29695156020980873
rmse :  155.9022723677876  
"""
"""
   non- validation_split=0.2 
   \oss :  24226.3828125
103/103 [==============================] - 0s 756us/step
r2 스코어 : 0.29924075548113804
rmse :  155.64824880674
"""
"""
TRIN X,Y있음
TEST X,Y있음
VAL X,Y있음
predict는 X있음 Y없음
예측값을 내놔야하니까

"""
