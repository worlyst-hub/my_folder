import sys
sys.stdin = open("input.txt", "r")

T = int(input())
for test_case in range(1, T + 1):
    N = int(input())
    farm = [list(map(int, input().split())) for _ in range(N)]

    income = 0

    for i in range(N):
        center = N // 2
        distance = abs(i - center)
        harvest = []
        for a in farm[i]:
            pass
            

    print("#{test_case} {income}")

