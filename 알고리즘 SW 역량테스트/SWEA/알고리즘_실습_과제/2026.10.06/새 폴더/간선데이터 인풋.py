# 2
# 5 6
# 1 2 1 3 3 2 3 4 2 5 5 4
# 1 4
# 5 7
# 1 2 1 3 3 2 3 4 2 5 5 4 5 3
# 1 4

### 인접 행렬 ###
T = int(input())
for test_case in range(1, T+1):
    N, E = map(int, input().split())
    data = list(map(int, input().split()))  # [1, 2, 1, 3, 3, 2, 3, 4, 2, 5, 5, 4]

    arr = [[0] * (N + 1) for _ in range(N + 1)]

    for i in range(0, E * 2, 2):
        start = data[i]           # idx = 0, 2, 4, 6, 8, 10    # start = 1, 1, 3, 3, 2, 5
        end = data[i + 1]         # idx = 1, 3, 5, 7, 9, 11    # end   = 2, 3, 2, 4, 5, 4

        arr[start][end] = 1

        #     0  1  2  3  4  5
        # 0  [0, 0, 0, 0, 0, 0]
        # 1  [0, 0, 1, 1, 0, 0]
        # 2  [0, 0, 0, 0, 0, 1]
        # 3  [0, 0, 1, 0, 1, 0]
        # 4  [0, 0, 0, 0, 0, 0]
        # 5  [0, 0, 0, 0, 1, 0]


### 인접 리스트 ###
T = int(input())
for test_case in range(1, T+1):
    N, E = map(int, input().split())
    data = list(map(int, input().split()))

    arr = [[] for _ in range(N + 1)]

    for i in range(0, E * 2, 2):
        start = data[i]
        end = data[i + 1]

        arr[start].append(end)

        # [
        #     [],        # 0
        #     [2, 3],    # 1
        #     [5],       # 2
        #     [2, 4],    # 3
        #     [],        # 4
        #     [4]        # 5
        # ]