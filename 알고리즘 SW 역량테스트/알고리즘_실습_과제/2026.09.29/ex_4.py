# 순열
# level = 3
# branch = 4
card = "ABCD"
path = [""] * 3  # 경로 저장하는 배열의 크기는 = level

def abc(level):
    if level == 3:
        for i in range(level):
            print(path[i], end=' ')
        print()
        return

    for i in range(4):
        path[level] = card[i]
        abc(level + 1)
        # path[level] = 0

abc(0)

print("###########")

card = "ABCD"
path = [""] * 3  # level (depth 크기)
used = [0] * 4  # branch 크기
def abc(level):
    if level == 3:
        print(*path)
        return

    for i in range(4):
        if used[i] == 1: continue  # 방문한 적이 있는지 확인
        used[i] = 1  # 방문체크
        path[level] = card[i]  # 앞으로 들어갈 경로 적기
        abc(level + 1)  # 다음 함수 들어가기
        path[level] = 0  # 경로 적었던것 지우고
        used[i] = 0  # 방문체크 해제

abc(0)