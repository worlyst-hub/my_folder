###
card = "ABCD"
path = [""] * 3  # 카드 묶음의 개수

def abc(level):
    if level == 3:
        print(*path)
        return

    for i in range(4):
        path[level] = card[i]
        abc(level + 1)
        path[level] = ""

abc(0)

### 중복 순열
card = "ABCD"
path = [""] * 3  # 카드 묶음의 개수
used = [0] * 4  # 선택할 수 있는 카드 종류의 개수 (branch)

def abc(level):
    if level == 3:
        print(*path)
        return

    for i in range(4):
        if used[i] == 1 : continue
        used[i] = 1
        path[level] = card[i]
        abc(level + 1)
        path[level] = ""
        used[i] = 0

abc(0)