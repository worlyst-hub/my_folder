# 반복과 재귀

# 반복
# 주사위 1개 던졌을 때 나올 수 있는 경우
for i in range(1, 7):
    print(i)

# 주사위 2개 던졌을 때 나올 수 있는 경우
for i in range(1, 7):
    for j in range(1, 7):
        print(i, j)

# 주사위 3개 던졌을 때 나올 수 있는 경우
for i in range(1, 7):
    for j in range(1, 7):
        for k in range(1, 7):
            print(i, j, k)

# 재귀
N = int(input())
path = [0] * N

def abc(level):
    if level == N:
        print(*path)
        return
    for i in range(1, 7):
        path[level] = i
        abc(level + 1)

abc(0)

# 함수 작동 순서
def kfc(test):  # 5
    print(test)  # 6
    print("!!")  # 7

def abc(test):  # 2
    print('#')  # 3
    print(test)  # 4
    kfc(456)  # 5
    print("**")  # 8
    print(test)  # 9

def bbq():  # 1
    abc(123)  # 2
    print('@')  # 10

# 출력 : # 123 456 !! ** 123 @

# 재귀 연습
def abc(level):

    if level == 2:
        return

    abc(level + 1)

abc(0)