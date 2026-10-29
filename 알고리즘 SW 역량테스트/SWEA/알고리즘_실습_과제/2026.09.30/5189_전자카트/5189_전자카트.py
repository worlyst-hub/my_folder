import sys
import os
sys.stdin = open(os.path.join(os.path.dirname(__file__), "sample_input.txt"), "r")

"""
문제 구상
전기 카트로 골프장 관리를 한다.
사무실에서 출발해 각 구역을 돌고 다시 사무실로 돌아와야한다.
한번씩만 방문해야하고 돌오왔을 때의 최소 배터리 사용량을 구하라.

단, 두 구역 사이도 경사나 통행로가 다르기 때문에 갈 때 올 때 소비량이 다를 수 있다.

로직 구상
1. 관리 구역의 방문 순서를 만든다.
2. 가능한 모든 방문 순서를 확인한다.
3. 각 방문 순서마다 1번 사무실에서 출발한다.
4. 방문 순서대로 이동하면서 각 구간의 배터리 사용량을 더한다.
5. 
"""

def dfs(now, count, battery):
        global min_battery


        if count == N:
            total = battery +field[now][0]
            min_battery = min(min_battery, total)
            return


        for next in range(1, N):

            if not visited[next]:
                visited[next] = 1
                dfs(next, count + 1, battery + field[now][next])
                visited[next] = 0


T = int(input())
for test_case in range(1, T+1):
    N = int(input())
    field = [list(map(int, input().split())) for _ in range(N)]

    visited = [0] * N
    visited[0] = 0
    min_battery = N * 100

    dfs(0, 1, 0)

    print(f"#{test_case} {min_battery}")