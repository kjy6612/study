import math
import numpy as np
import pandas as pd
import glob
from sklearn.neighbors import KNeighborsRegressor
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler, MaxAbsScaler, RobustScaler
from sklearn.metrics import r2_score, mean_squared_error,mean_absolute_error
from sklearn.utils import all_estimators
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import SimpleImputer, KNNImputer, IterativeImputer
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from sklearn.preprocessing import LabelEncoder
import pprint
import time
from pprint import pprint
import warnings
warnings.filterwarnings('ignore')
import datetime 
date = datetime.datetime.now()  
date = date.strftime("%m%d_%H%M") 
def split_x(dataset, timesteps): # split_x라는 함수를 정의
    aaa = [] # aaa 에 빈칸의 리스트를 만든다.
    for i in range(len(dataset) - timesteps + 1): # for : 반복문, i 변수에, range 일정 간격으로 숫자를 나열 len 데이터의 길이 시작값 - 끝값 + 증가값, in 과 : 사이가 반복할 횟수 
        subset = dataset[i : (i + timesteps)] # subset 변수에 dataset i0 : (i0 + 5)
        aaa.append(subset) # aaa 리스트에 subset 값 이어붙힌다. aaa.i0 : (i0 + 5)
    return np.array(aaa) # 충족할때까지 반복한다.
col_name = ['연도','일시', '측정소', 'PM2.5']
le_col_name = ['일시', '측정소']
path = "./_data/aifact_05/"
path_train = "./_data/aifact_05/TRAIN/"
path_test = "./_data/aifact_05/TEST_INPUT/"
path_train_AWS = "./_data/aifact_05/TRAIN_AWS/"
path_test_AWS = "./_data/aifact_05/TEST_AWS/"
path_save = "./_save/aifact_05/"
path_data_imputer = "./_data/aifact_05/train_pd_inter/"
path_data_inter = "./_data/aifact_05/train_pd_inter/"
data_name_list = [
    '공주.csv','노은동.csv','논산.csv','대천2동.csv','독곶리.csv','동문동.csv',
    '모종동.csv','문창동.csv','성성동.csv','신방동.csv','신흥동.csv','아름동.csv','예산군.csv',
    '읍내동.csv','이원면.csv','정림동.csv','홍성읍.csv']
path_meta = './_data/aifact_05/META/'

# read in the csv files
pmmap_csv = pd.read_csv(path_meta+'pmmap.csv', index_col=False, encoding='utf-8')
awsmap_csv = pd.read_csv(path_meta+'awsmap.csv', index_col=False, encoding='utf-8')

# create a dictionary of places in awsmap.csv
places_awsmap = {}
for i, row in awsmap_csv.iterrows():
    places_awsmap[row['Description']] = (row['Latitude'], row['Longitude'])

# define a function to calculate the distance between two points
def distance(lat1, lon1, lat2, lon2):
    R = 6371 # earth radius in kilometers
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    a = math.sin(dLat/2) * math.sin(dLat/2) + \
        math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# loop over the locations in pmmap.csv
for i, row_a in pmmap_csv.iterrows():
    # find the closest places in awsmap.csv to the location in pmmap.csv
    closest_places = []
    closest_distances = []
    for j, row_b in awsmap_csv.iterrows():
        dist = distance(row_a['Latitude'], row_a['Longitude'], row_b['Latitude'], row_b['Longitude'])
        if len(closest_places) < 3:
            closest_places.append(row_b['Location'])
            closest_distances.append(dist)
        else:
            max_index = closest_distances.index(max(closest_distances))
            if dist < closest_distances[max_index]:
                closest_places[max_index] = row_b['Location']
                closest_distances[max_index] = dist
    
    # sort the distances in ascending order
    closest_places = [x for _, x in sorted(zip(closest_distances, closest_places))]
    closest_distances.sort()
    
    # print the closest places for the location in pmmap.csv with their distances
    print("Closest places to {} (in ascending order of distance):".format(row_a['Location']))
    for k in range(1):
        print("{}, distance: {:.2f} km".format(closest_places[k], closest_distances[k]))


#### 1. 데이터

train_files = glob.glob(path+'TRAIN/*.csv')
train_aws_files = glob.glob(path+'TRAIN_AWS/*.csv')

test_input_files = glob.glob(path+'test_input/*.csv')
# test_aws_files = glob.glob(path+'test_aws/*.csv')

############################# train 폴더 #########################################

train_li=[]
for filename in train_files :
    df = pd.read_csv(filename,index_col=None, 
                     header=0, # 위에 컬럼에 대한 인식하게 함 
                     encoding='utf-8')
    train_li.append(df)
train_dataset= pd.concat(train_li,axis=0,
                         ignore_index=True # 원래 있던 인덱스는 사라지고 새로운 인덱스가 생성된다. 
                         )
# print(train_dataset)
print(train_dataset.shape) # (596088, 4)



sego_train_csv=pd.read_csv(path_train_AWS +'세종고운.csv',encoding='utf-8',index_col=False)
seyun_train_csv=pd.read_csv(path_train_AWS +'세종연서.csv',encoding='utf-8',index_col=False)
gyeryong_train_csv=pd.read_csv(path_train_AWS +'계룡.csv',encoding='utf-8',index_col=False)
Oworld_train_csv=pd.read_csv(path_train_AWS +'오월드.csv',encoding='utf-8',index_col=False)
jangdong_train_csv=pd.read_csv(path_train_AWS +'장동.csv',encoding='utf-8',index_col=False)
Oworld_train_csv02=pd.read_csv(path_train_AWS +'오월드.csv',encoding='utf-8',index_col=False)
gongjoo_train_csv=pd.read_csv(path_train_AWS +'공주.csv',encoding='utf-8',index_col=False)

nonsan_train_csv=pd.read_csv(path_train_AWS +'논산.csv',encoding='utf-8',index_col=False)
deacheon_train_csv=pd.read_csv(path_train_AWS +'대천항.csv',encoding='utf-8',index_col=False)
deasan_train_csv=pd.read_csv(path_train_AWS +'대산.csv',encoding='utf-8',index_col=False)
teaan_train_csv=pd.read_csv(path_train_AWS +'태안.csv',encoding='utf-8',index_col=False)
asan_train_csv=pd.read_csv(path_train_AWS +'아산.csv',encoding='utf-8',index_col=False)
sung_train_csv=pd.read_csv(path_train_AWS +'성거.csv',encoding='utf-8',index_col=False)
yesan_train_csv=pd.read_csv(path_train_AWS +'예산.csv',encoding='utf-8',index_col=False)
teaan02_train_csv=pd.read_csv(path_train_AWS +'태안.csv',encoding='utf-8',index_col=False)
aan_train_csv=pd.read_csv(path_train_AWS +'홍북.csv',encoding='utf-8',index_col=False)
sung02_train_csv=pd.read_csv(path_train_AWS +'성거.csv',encoding='utf-8',index_col=False)

train_aws_li = [sego_train_csv,seyun_train_csv,
    gyeryong_train_csv,Oworld_train_csv,
    jangdong_train_csv,Oworld_train_csv02,
    gongjoo_train_csv,nonsan_train_csv,
    deacheon_train_csv,deasan_train_csv,
    teaan_train_csv,asan_train_csv,
    sung_train_csv,yesan_train_csv,
    teaan02_train_csv,aan_train_csv,sung02_train_csv
]

train_aws_dataset = pd.concat([sego_train_csv,seyun_train_csv,
    gyeryong_train_csv,Oworld_train_csv,
    jangdong_train_csv,Oworld_train_csv02,
    gongjoo_train_csv,nonsan_train_csv,
    deacheon_train_csv,deasan_train_csv,
    teaan_train_csv,asan_train_csv,
    sung_train_csv,yesan_train_csv,
    teaan02_train_csv,aan_train_csv,sung02_train_csv
], axis=0,ignore_index=True)
print(train_aws_dataset.shape)
############################# test 폴더 #########################################

test_li=[]
for filename in test_input_files :
    df = pd.read_csv(filename,index_col=None, 
                     header=0, # 위에 컬럼에 대한 인식하게 함 
                     encoding='utf-8')
    test_li.append(df)
test_input_dataset= pd.concat(test_li,axis=0,
                         ignore_index=True # 원래 잇던 인덱스는 사라지고 새로운 인덱스가 생성된다. 
                         )
print(test_input_dataset)

sego_test_csv=pd.read_csv(path_test_AWS +'세종고운.csv',encoding='utf-8',index_col=False)
seyun_test_csv=pd.read_csv(path_test_AWS +'세종연서.csv',encoding='utf-8',index_col=False)
gyeryong_test_csv=pd.read_csv(path_test_AWS +'계룡.csv',encoding='utf-8',index_col=False)
Oworld_test_csv=pd.read_csv(path_test_AWS +'오월드.csv',encoding='utf-8',index_col=False)
jangdong_test_csv=pd.read_csv(path_test_AWS +'장동.csv',encoding='utf-8',index_col=False)
Oworld_test_csv02=pd.read_csv(path_test_AWS +'오월드.csv',encoding='utf-8',index_col=False)
gongjoo_test_csv=pd.read_csv(path_test_AWS +'공주.csv',encoding='utf-8',index_col=False)

nonsan_test_csv=pd.read_csv(path_test_AWS +'논산.csv',encoding='utf-8',index_col=False)
deacheon_test_csv=pd.read_csv(path_test_AWS +'대천항.csv',encoding='utf-8',index_col=False)
deasan_test_csv=pd.read_csv(path_test_AWS +'대산.csv',encoding='utf-8',index_col=False)
teaan_test_csv=pd.read_csv(path_test_AWS +'태안.csv',encoding='utf-8',index_col=False)
asan_test_csv=pd.read_csv(path_test_AWS +'아산.csv',encoding='utf-8',index_col=False)
sung_test_csv=pd.read_csv(path_test_AWS +'성거.csv',encoding='utf-8',index_col=False)
yesan_test_csv=pd.read_csv(path_test_AWS +'예산.csv',encoding='utf-8',index_col=False)
teaan02_test_csv=pd.read_csv(path_test_AWS +'태안.csv',encoding='utf-8',index_col=False)
aan_test_csv=pd.read_csv(path_test_AWS +'홍북.csv',encoding='utf-8',index_col=False)
sung02_test_csv=pd.read_csv(path_test_AWS +'성거.csv',encoding='utf-8',index_col=False)

test_csv_list = [sego_test_csv,seyun_test_csv,
    gyeryong_test_csv,Oworld_test_csv,
    jangdong_test_csv,Oworld_test_csv02,
    gongjoo_test_csv,nonsan_test_csv,
    deacheon_test_csv,deasan_test_csv,
    teaan_test_csv,asan_test_csv,
    sung_test_csv,yesan_test_csv,
    teaan02_test_csv,aan_test_csv,sung02_test_csv
]

for v in test_csv_list:
    mode = v['지점'].mode()[0]
    v['지점'] = v['지점'].fillna(mode)
print('Done.')

test_aws_dataset = pd.concat([
    sego_test_csv,seyun_test_csv,
    gyeryong_test_csv,Oworld_test_csv,
    jangdong_test_csv,Oworld_test_csv02,
    gongjoo_test_csv,nonsan_test_csv,
    deacheon_test_csv,deasan_test_csv,
    sung_test_csv,yesan_test_csv,
    teaan_test_csv,asan_test_csv,
    teaan02_test_csv,aan_test_csv,sung02_test_csv],axis=0,ignore_index=True
)


################### 일시 -> 월, 일, 시간으로 분리 ###############################

# 12-31 21 : 00 / 12와 21 추출 
# (596088, 4) (1051920, 8) (131376, 4) (131376, 8)
train_dataset = train_dataset.drop(['일시','연도'],axis=1)
train_all_dataset = pd.concat([train_dataset,train_aws_dataset],axis=1)
print(train_all_dataset)


# 12-31 21 : 00 / 12와 21 추출 
# print(train_aws_dataset['일시'].info()) 
# # print(type(train_aws_dataset['일시'][0])) # <class 'str'>
# print(train_aws_dataset['일시'].dtype) # object
# train_dataset['month'] = train_dataset['일시'].str[:2]
# # print(train_aws_dataset['month'])
# train_dataset['day'] = train_dataset['일시'].str[3:5]
# # print(train_dataset['day'])
# train_dataset['hour'] = train_dataset['일시'].str[6:8]
# # print(train_aws_dataset['hour'])
# train_aws_dataset = train_aws_dataset.drop(['일시'],axis=1)
 
# train_aws_dataset['month'] = train_aws_dataset['month'].astype('Int16')
# train_aws_dataset['day'] = train_aws_dataset['day'].astype('Int16')
# train_aws_dataset['hour'] = train_aws_dataset['hour'].astype('Int16')

# (1051920, 10) (596088, 2) (1051920, 8) (131376, 4) (131376, 8)


train_all_dataset['month'] = train_all_dataset['일시'].str[:2]
# print(train_aws_dataset['month'])
train_all_dataset['day'] = train_all_dataset['일시'].str[3:5]
# print(train_dataset['day'])
train_all_dataset['hour'] = train_all_dataset['일시'].str[6:8]
# print(train_aws_dataset['hour'])
train_all_dataset = train_all_dataset.drop(['일시'],axis=1)

train_all_dataset['month'] = train_all_dataset['month'].astype('Int16')
train_all_dataset['day'] = train_all_dataset['day'].astype('Int16')
train_all_dataset['hour'] = train_all_dataset['hour'].astype('Int16')

test_input_dataset= test_input_dataset.drop(['일시'],axis=1)

test_aws_dataset['month'] = test_aws_dataset['일시'].str[:2]
test_aws_dataset['day'] = test_aws_dataset['일시'].str[3:5]
test_aws_dataset['hour'] = test_aws_dataset['일시'].str[6:8]
test_aws_dataset['month'] = test_aws_dataset['month'].astype('Int16')
test_aws_dataset['day'] = test_aws_dataset['day'].astype('Int16')
test_aws_dataset['hour'] = test_aws_dataset['hour'].astype('Int16')

test_aws_dataset= test_aws_dataset.drop(['일시'],axis=1)


############################# 라벨 인코더 #########################################

le=LabelEncoder()
train_all_dataset['locate'] = le.fit_transform(train_all_dataset['지점'])
test_aws_dataset['locate'] = le.transform(test_aws_dataset['지점'])


# train_dataset= train_dataset.drop(['측정소'],axis=1)
train_all_dataset= train_all_dataset.drop(['지점','측정소'],axis=1)
test_aws_dataset= test_aws_dataset.drop(['지점'],axis=1)

print('결측치')
print(train_all_dataset.shape,train_dataset.shape,train_aws_dataset.shape,test_input_dataset.shape,test_aws_dataset.shape)
print(train_all_dataset)

print(test_aws_dataset.columns)
'''
['연도', '기온(°C)', '풍향(deg)', '풍속(m/s)', '강수량(mm)', '습도(%)', 'month',
       'day', 'hour', 'locate'],
'''
y = train_all_dataset['PM2.5']
x = train_all_dataset.drop(['PM2.5'],axis=1)
print(x.columns)
'''
[]'연도', '기온(°C)', '풍향(deg)', '풍속(m/s)', '강수량(mm)', '습도(%)', 'month',
       'day', 'hour', 'locate', 'locate02']

'''

############################# 결측치 처리 #########################################
imputer = IterativeImputer(estimator=XGBRegressor(
        n_jobs = -1,                        
        tree_method='gpu_hist',
        predictor='gpu_predictor',
        gpu_id=0
    )) # knn알고리즘으로 평균값을 찾아낸 것이다. 
# train_dataset = train_dataset.interpolate(order=2)
# train_aws_dataset = train_aws_dataset.interpolate(order=2)
# test_aws_dataset = test_aws_dataset.interpolate(order=2)
x = imputer.fit_transform(x)
test_aws_dataset = imputer.transform(test_aws_dataset)
# for i in imputer_list : 
#     train_aws_dataset[i] = imputer.transform(train_aws_dataset[i])
#     test_aws_dataset[i] = imputer.transform(test_aws_dataset[i])
print('x,y')


print('x:',x.shape)
print('y:',y.shape)

x_train,x_test, y_train, y_test = train_test_split(
    x,y,test_size = 0.2, # random_state=337,
    # shuffle=True
)

print('RobustScaler')

scaler = RobustScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

print('reshape')
# x_train = x_train.reshape(x_train.shape[0],x_train.shape[1], 1)
# x_test = x_test.reshape(x_test.shape[0],x_test.shape[1], 1)


#2. 모델 

start= time.time()
model = KNeighborsRegressor(n_neighbors=10,weights='distance')
# model= Sequential()
# model.add(LSTM(1,input_shape=(x_train.shape[1],1)))
# # model.add(LSTM(32))
# model.add(Dense(1, activation='relu'))
# model.summary()

#3. 훈련 
# model.compile(optimizer='adam', loss='mse')
# from tensorflow.python.keras.callbacks import EarlyStopping, ModelCheckpoint
# es = EarlyStopping(monitor='loss',mode='min',restore_best_weights=True,patience=8)
# model.fit(x_train,y_train,epochs=3,
#           verbose=1,
#           batch_size = 1,
#           callbacks =[es])
model.fit(x_train,y_train)
end= time.time()
print('걸린 시간 : ',round(end -start,2),'초')

# 4. 평가, 예측
# result = model.evaluate(x_test,y_test)
result = model.score(x_test,y_test)
y_pred = model.predict(x_test)
print("model.score : ",result)
r2 = r2_score(y_test,y_pred)
print('r2 : ',r2)
mae = mean_absolute_error(y_test,y_pred)
print('mae : ',mae)
