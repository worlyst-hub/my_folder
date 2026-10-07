import sys
import os
sys.stdin = open(os.path.join(os.path.dirname(__file__), "sample_input.txt"), "r")


"""
문제 구상


"""
from collections import deque

T = int(input())
for test_case in range(1, T+1):
    N, M = map(int, input().split())
    jido = [list(input().strip()) for _ in range(N)]  # [['W', 'L', 'L'], ['L', 'L', 'L']]
    arr = [[-1] * M for _ in range(N)]
    count = 0

    q = deque()
    for i in range(N):
        for j in range(M):
            if jido[i][j] == 'W':
                q.append((i, j))
                arr[i][j] = 0

    di = [-1, 1, 0, 0]
    dj = [0, 0, -1, 1]

    while q:
        i, j = q.popleft()

        for k in range(4):
            ni = i + di[k]
            nj = j + dj[k]

            if 0 <= ni < N and 0 <= nj < M and arr[ni][nj] == -1:
                arr[ni][nj] = arr[i][j] + 1
                q.append((ni, nj))

    for n in range(N):
        for r in range(M):
            count += arr[n][r]

    print(f"#{test_case} {count}")

