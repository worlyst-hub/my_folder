### DFS (인접 행렬) = 가능한 모든 정점 1번씩 탐색 ###
name = "BACD"
arr = [
    [0, 0, 1, 1],
    [1, 0, 1, 0],
    [1, 0, 0, 1],
    [0, 0, 0, 0]
]

used = [0] * 4  # 정점의 개수만큼 방문체크

def dfs(now):

    print(name[now], end=' ')
    for i in range(4):
        if arr[now][i] == 1 and used[i] == 0:
            used[i] = 1
            dfs(i)


used[1] = 1  # 탐색 시작 인덱스에 1 중bhul/복체크
dfs(1)  # 탐색 시작 인덱스



### DFS (인접 리스트) = 가능한 모든 정점 1번씩 탐색 ###
# 4 6
# 0 2
# 0 3
# 1 0
# 1 2
# 2 0
# 2 3
name = "BACD"
N, M = map(int, input().split())  # 정점, 간선 정보의 개수
arr = [[] for _ in range(N)]
for _ in range(M):
    start, end = map(int, input().split())
    arr[start].append(end)  # 이것만 있으면 유향 그래프
    # arr[end].append(start)  # 이거까지 있으면 무향 그래프

used = [0] * N

def dfs(now):

    print(name[now], end=' ')
    for i in arr[now]:
        if used[i] == 0:
            used[i] = 1
            dfs(i)


used[1] = 1  # DFS 시작 인덱스에 1 체크
dfs(1)



### DFS (인접 리스트) = 갈 수 있는 방법 몇가지인지 탐색 ###
# 4 6
# 0 2
# 0 3
# 1 0
# 1 2
# 2 0
# 2 3
name = "BACD"
N, M = map(int, input().split())  # 정점, 간선 정보의 개수
arr = [[] for _ in range(N)]
for _ in range(M):
    start, end = map(int, input().split())
    arr[start].append(end)  # 이것만 있으면 유향 그래프
    # arr[end].append(start)  # 이거까지 있으면 무향 그래프

used = [0] * N
count = 0

def dfs(now):
    global count
    if now == 3:  # if name[now] == 'D':
        count += 1

    print(name[now], end=' ')
    for i in arr[now]:
        if used[i] == 0:
            used[i] = 1
            dfs(i)
            used[i] = 0


used[1] = 1  # DFS 시작 인덱스에 1 체크
dfs(1)
print(count)

### 연습 ###

#     1, 2, 3, 4, 5, 6, 7
#
# 1   0, 1, 1, 0, 0, 0, 0
# 2   1, 0, 0, 1, 1, 0, 0
# 3   1, 0, 0, 0, 0, 0, 1
# 4   0, 1, 0, 0, 0, 1, 0
# 5   0, 1, 0, 0, 0, 1, 0
# 6   0, 0, 0, 1, 1, 0, 1
# 7   0, 0, 1, 0, 0, 1, 0

