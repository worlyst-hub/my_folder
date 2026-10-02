### N_queen
# branch 4 // level 4
# vertical = [j]
# seven = [i + j]
# five = [i - j + N]

# N * N 사이즈의 체스판에 N개의 퀸을 방해없이 놓을 수 있을 경우
# 그 경우가 몇가지 인가요?  8 입력  97

# N = int(input())  # 체스판의 크기
N = 8
vertical = [0] * N
seven = [0] * (2 * N)
five = [0] * (2 * N)

count = 0
def abc(level):
    global count
    if level == N:
        count += 1
        return

    for j in range(N):
        if vertical[j] == 1: continue
        if seven[level + j] == 1 or five[level - j + N] == 1: continue  # 가지치기
        vertical[j], seven[level + j], five[level - j + N] = 1, 1, 1
        abc(level + 1)
        vertical[j], seven[level + j], five[level - j + N] = 0, 0, 0  # 백트랙킹 개념

abc(0)
print(count)
