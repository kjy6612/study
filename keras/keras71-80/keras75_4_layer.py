import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

model = Sequential()
model.add(Dense(3, input_dim=1, name='hidden1'))
model.add(Dense(2,name='hidden2'))
model.add(Dense(1,name='outputs'))
model.summary()

# 1. 전체 동결
# model.trainable = False

# 2. 전체 동결
# for layer in model.layers : 
#     layer.trainable = False
    
# 3. 부분 동결
# print(model.layers[0])  # <keras.layers.core.dense.Dense object at 0x000002F02A5ED280>
# model.layers[0].trainable = False # hidden1
model.layers[1].trainable = False # hidden2
# model.layers[2].trainable = False # output
model.summary()

import pandas as pd
# 확인용 
pd.set_option('max_colwidth',-1)
layers = [(layer,layer.name,layer.trainable) for  layer in model.layers]
print(layers)
result= pd.DataFrame(layers, columns=['Layer Type','Layer Name','Layer Trainable'])
print(result)
