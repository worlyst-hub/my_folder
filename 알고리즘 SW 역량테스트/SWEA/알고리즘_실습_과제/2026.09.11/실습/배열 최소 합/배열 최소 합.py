import sys
sys.stdin = open("sample_input.txt", "r")

"""
문제 구상
NxN 크기의 배열에 숫자가 있음
N개의 숫자를 골라 합이 최소가 되도록 해야함
숫자 하나를 선택했을때 같은 세로, 가로줄에 있는 숫자는 고를 수 없음

로직 구상
1. N과 배열을 입력받음
2. 
"""


def solve(idx, check, sum_v):
    global min_v



    if sum_v >= min_v:
        return


    
    if idx == N:
        if min_v > sum_v:
             min_v = sum_v
        return


 
    for i in range(N):
        if check[i] == 0:
            check[i] = 1
            solve(idx+1, check, sum_v + arr[idx][i])
            check[i] = 0
 
 
 
T = int(input())
for test_case in range(1, T + 1):
    N = int(input())
    arr = [list(map(int, input().split())) for _ in range(N)]


    min_v = 1000
    solve(0, [0]*N, 0)
    print(f'#{test_case} {min_v}')
