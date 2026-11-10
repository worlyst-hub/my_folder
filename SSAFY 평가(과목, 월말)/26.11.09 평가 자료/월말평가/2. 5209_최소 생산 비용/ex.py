import sys
import os
sys.stdin = open(os.path.join(os.path.dirname(__file__), "sample_input.txt"), "r")

T = int(input())
for test_case in range(1, T+1):
    N = int(input())
    data = [list(map(int, input().split())) for _ in range(N)]

    check = [0] * N
    min_cost = 1000000000

    def solve(idx, cost):
        global min_cost
        if cost > min_cost:
            return

        if idx == N:
            if cost < min_cost:
                min_cost = cost

        for i in range(N):
            if not check[i]:
                check[i] = 1
                solve(idx + 1, cost + data[idx][i])
                check[i] = 0

    solve(0, 0)
    print(f"#{test_case} {min_cost}")