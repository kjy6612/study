#리스트
a=[1,2,3]
b=[4,5,6]
print(a+b)
print(a*3)
#리스트 값 수정하기
a=["김이박","밥밥밥","컵컵컵"]
a[0]="김김김"
print(a)
#연속되게 교체하기
a[0:2]=["이이이","최최최"]
print(a)
#인덱스0부터 2미만
a[0:2]=["이이이","최최최","강강강"]
print(a)
a=["김이박","밥밥밥","컵컵컵"]
a[0:2]=[]
print(a)
#리스트 삭제
a=["김이박","밥밥밥","컵컵컵"]
del a[0]
print(a)
del a[0]
del a[0]
print(a)
#del a를 했을 경우 a를 찾지 못해서 에러가 난다.
