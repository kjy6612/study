import tensorflow as tf
tf.compat.v1.set_random_seed(337)
x_data = [
    [73,51,65],
    [92,98,11],
    [89,31,33],
    [99,33,100],
    [17,66,79],
          ] # (5,3)
'''
아까는 x를 나눠서 3개로 줬지만 지금으 ㄴ아니라서 5행 3열 이라는 것을 인식시켜줘야한다. 

'''

y_data = [
    [152],
    [185],
    [180],
    [205],
    [142],
          ] # 5,1

x = tf.compat.v1.placeholder(tf.float32)
y = tf.compat.v1.placeholder(tf.float32)
w = tf.compat.v1.Variable(tf.compat.v1.random_normal([]),name = 'weight')
b = tf.compat.v1.Variable(tf.compat.v1.random_normal([]), name = 'bias')

#  hypothesis = x1 * w1 + x2 * w2 + x3 * w3 + b
hypothesis = x * w + b

sess = tf.compat.v1.Session()
sess.run(tf.compat.v1.global_variables_initializer()) 
print(sess.run([hypothesis,w,b],feed_dict={x:x_data}))

'''
[array([[25.064732 , 17.198214 , 22.20418  ],
       [31.858541 , 34.003956 ,  2.8954527],
       [30.785837 , 10.046833 , 10.7619705],
       [34.361523 , 10.7619705, 34.719093 ],
       [ 5.040867 , 22.561749 , 27.210146 ]], dtype=float32), 0.357569]
웨이트 : 0.357569
바이어스 : -1.0378063
위에 x_data와 계산시
hypothesis : 5.040867
'''
