### BFS 너비 우선 탐색 (모든 정점을 한번씩 탐색)
# 4 6
# 0 1
# 0 2
# 1 2
# 1 3
# 2 1
# 2 3

from collections import deque
N, M = map(int, input().split())
arr = [[] for _ in range(N)]
for _ in range(M):
    a, b = map(int, input().split())
    arr[a].append(b)

q = deque()
used = [0] * N
q.append(0)  # 시작점 큐에 넣기
used[0] = 1  # 시작점 방문 체크
name = "ABCD"

while q:
    now = q.popleft()  # 큐에 있는 것 먼저 빼기
    print(name[now], end=' ')
    for i in arr[now]:  # 현재 위치에서 이동 가능한 것 탐색
        if used[i] == 0:  # 방문 여부 확인
            used[i] = 1  # 방문 체크
            q.append(i)  # 큐에 넣기

