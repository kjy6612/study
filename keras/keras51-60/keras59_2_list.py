import numpy as np
import pandas as pd
a = [[1,2,3],[4,5,6]]
b = np.array(a)
print(b)
c = [[1,2,3],[4,5]]
print(c)
# 리스트 -> 파이썬 , 크기가 달라도 상관 없다. 
# 넘파이는 크기가 다르면 오류 난다.
d = np.array(c)
print(d) #[list([1, 2, 3]) list([4, 5])]
# 넘파이 안에 리스트 두 개 
# 1. 리스트는 크기가 달라도 상관이 없다. 

##################################################
e = [[1,2,3],['바보','맹구',5,6]]
print(e)
#리스트 안에는 수치형 문자형 등 다른 자료형을 넣어도 상관이 없다.

f = np.array(e)
print(f) #[list([1, 2, 3]) list(['바보', '맹구', 5, 6])] -> 안에 리스트 형태이기 때문에 연산이 안된다. 
print(e.shape)
# 크기가 다르면 쉐이프가 제공되지 않는다. 
# 다를 경우 len으로 수치를 확인해야한다. 
# 넘파이랑 판다스는 한 가지 자료 형만 사용해야한다.
