"""
A사는 여러 공장을 가지고 있음
N종의 제품을 N곳의 공장에서 한 곳당 한가지씩 생산하려고 함
각 공장의 생산비용이 주어질 때 최소 생산 비용을 계산하는 프로그램을 만들어라
"""
import sys
import os
sys.stdin = open(os.path.join(os.path.dirname(__file__), "sample_input.txt"), "r")

## 5209_최소 생산 비용
def solve(idx,cost):
    global min_cost
    if cost >= min_cost:
        return
 
    if idx == N:
        if cost < min_cost:
            min_cost = cost

    for i in range(N):
        if not check[i]:
            check[i] = 1
            solve(idx+1,cost + data[idx][i])
            check[i] = 0
 
T = int(input())
for test_case in range(1,T+1):
    N = int(input())
    data = [list(map(int,input().split())) for _ in range(N)]

    check = [0] * N
    min_cost = 10000

    solve(0,0)
    print(f'#{test_case} {min_cost}')



