### lambda - 익명함수
## 1. 
def Sum(a, b):
    return a + b

result = Sum(3, 4)
print(result)
## 2. 
result = (lambda a, b: a + b)(3, 4)
print(result)
## 3. 
result = (lambda a, b: a + b)
print(result(3, 4))


### sort # 원본 값 바꾸는거,, (sorted는 원본 값 바꾸지 않는것)
## 1. 
arr = [3, 1, 2, 5, 1, 3, 6, 5, 3, 2, 21, 5]
arr.sort(reverse=True)  # 내림차순

## 2. 정수인 경우에만 -x 활용 가능,, (문자열인 경우 reverse=True 활용)
def test(x):
    return -x

arr = [3, 1, 2, 5, 1, 3, 6, 5, 3, 2, 21, 5]
arr.sort(key=test)
print(arr)

## 3. 
arr = [3, 1, 2, 5, 1, 3, 6, 5, 3, 2, 21, 5]
arr.sort(key=lambda x: -x)
print(arr)

## 4. 
# 4-1. 튜플의 1번 인덱스 기준으로 정렬
salt = [(5, 50), (10, 60), (20, 140)]
salt.sort(lambda x: x[1], reverse=True)
print(salt)

# 4-2. 단위당 단가가 가장 높은 순으로 (단위당 단가 = 가치 // 무게)
salt = [(5, 50), (10, 60), (20, 140)]
salt.sort(key=lambda x: x[1] // x[0], reverse=True)
print(salt)