# 완전탐색
# 1.
arr = [3, 4, 7, 1, 6]

count = 0

def abc(level, Sum):
    global count

    if Sum > 10:  # 가지치기
        return
    
    if level == 3:
        if Sum == 10:
            count += 1
        return

    for i in range(5):
        abc(level + 1, Sum + arr[i])  # level 1씩 증가 / Sum 내가 앞으로 들어갈 가지 더하기

abc(0, 0)  # level, Sum
print(count)

# 2. Sum을 전역변수로 지정
arr = [3, 4, 7, 1, 6]

count = 0
Sum = 0

def abc(level):
    global count, Sum

    if Sum > 10:  # 가지치기
        return
    
    if level == 3:
        if Sum == 10:
            count += 1
        return

    for i in range(5):
        Sum += arr[i]
        abc(level + 1)  # level 1씩 증가 / Sum 내가 앞으로 들어갈 가지 더하기
        Sum -= arr[i]

abc(0)  # level
print(count) 