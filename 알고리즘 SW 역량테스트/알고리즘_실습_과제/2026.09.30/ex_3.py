### 조합
card = "ABCD"
path = [""] *3

def abc(level, start):
    if level == 3:
        print(*path)
        return

    for i in range(start, 4):
        path[level] = card[i]  # 내가 앞으로 들어갈 경로를 적고
        abc(level + 1, i + 1)  # 다음 함수에 진입
        # path[level] = ""  # 함수 리턴후, 적었던 경로를 지우기 (없어도 됨)

abc(0, 0)

### 중복 조합
card = "ABCD"
path = [""] *3

def abc(level, start):
    if level == 3:
        print(*path)
        return

    for i in range(start, 4):
        path[level] = card[i]  # 내가 앞으로 들어갈 경로를 적고
        abc(level + 1, i)  # 다음 함수에 진입 (## + 1만 뺌)
        # path[level] = ""  # 함수 리턴후, 적었던 경로를 지우기 (없어도 됨)

abc(0, 0)
