import sys
sys.stdin = open("input.txt", "r")

N, M = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]

for i in range(M):
    arr_2 = []
    for j in range(N - 1, -1, -1):
        arr_2.append(arr[j][i])

    print(*arr_2)
