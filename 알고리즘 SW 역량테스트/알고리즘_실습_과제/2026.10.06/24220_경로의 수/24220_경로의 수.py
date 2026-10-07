import sys
import os
sys.stdin = open(os.path.join(os.path.dirname(__file__), "test_in.txt"), "r")

"""
문제 구상

"""

def dfs(now):
    global count

    if now == G:
        count += 1
        return

    for next in range(N + 1):
        if arr[now][next] == 1 and used[next] == 0:  # now에서 next로 갈 수 있고 next에 아직 방문하지 않았다면
            used[next] = 1  # 방문처리
            dfs(next)       # 다음 정점 탐색
            used[next] = 0  # 방문해제 ㅡ


T = int(input())
for test_case in range(1, T+1):
    N, E = map(int, input().split())
    data = list(map(int, input().split()))

    arr = [[0] * (N + 1) for _ in range(N + 1)]

    for i in range(0, E * 2, 2):
        start = data[i]
        end = data[i + 1]

        arr[start][end] = 1

    S, G = map(int, input().split())

    used = [0] * (N + 1)
    count = 0
    used[S] = 1
    dfs(S)

    print(f"#{test_case} {count}")