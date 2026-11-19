import sys
from collections import deque

# sys.stdin = open("input.txt", "r")  # 로컬 파일 테스트 시 주석 해제

"""
문제 구상
N x N 크기의 격자에 사람 H명과 비를 피할 수 있는 장소 M개가 있다.
사람은 상하좌우로 이동할 수 있고, 한 칸을 이동하는 데 1초가 걸린다.
벽은 지나갈 수 없고 나머지 칸은 모두 이동할 수 있다.
사람마다 가장 가까운 비를 피할 수 있는 장소까지 걸리는 시간을 구한다.
피할 수 없는 사람은 -1, 사람이 없는 칸은 0을 출력한다.

로직 구상
1. N, H, M과 N x N 격자 정보를 입력받는다. # 2차원 리스트
2. 비를 피할 수 있는 모든 장소를 큐에 넣는다. # 여러 시작점
3. 방문 여부와 각 위치까지의 최단거리를 기록할 배열을 만든다.
4. 큐에서 하나씩 꺼내 상하좌우를 확인한다. # BFS, 델타
5. 격자 안에 있고 벽이 아니며 방문하지 않은 위치로만 이동한다.
6. 이동한 위치의 거리를 이전 위치 + 1로 기록하고 큐에 넣는다.
7. 모든 위치를 확인해 사람인 곳에만 가장 가까운 장소까지의 거리를 출력한다.
"""

# 1. N, H, M과 격자 정보를 입력받는다. # 2차원 리스트
N, H, M = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]

# 2-1. BFS 탐색에 사용할 큐 생성
q = deque()

# 3. 방문 여부와 최단거리를 기록하는 배열 만들기
visited = [[False] * N for _ in range(N)]
step = [[0] * N for _ in range(N)]

# 4-1. 상하좌우 방향을 나타내는 델타 설정
di = [-1, 1, 0, 0]
dj = [0, 0, -1, 1]

# 2. 비를 피할 수 있는 장소(3)를 모두 시작점으로 큐에 넣는다.
for i in range(N):
    for j in range(N):
        if arr[i][j] == 3:
            q.append((i, j))
            # 3-1. 시작점은 방문한 것으로 표시한다.
            visited[i][j] = True

# 4. 큐에 남아있는 위치를 하나씩 확인한다. # BFS
while q:
    i, j = q.popleft()

    # 4-2. 현재 위치에서 상하좌우 4방향을 확인
    for k in range(4):
        ni = i + di[k]
        nj = j + dj[k]

        # 5-1. 격자 안에 들어오는지 확인
        if 0 <= ni < N and 0 <= nj < N:
            # 5-2. 벽이 아니면서 아직 방문하지 않은 곳만 이동
            if arr[ni][nj] != 1 and not visited[ni][nj]:
                # 3-2. 중복 방문을 막기 위해 방문 표시
                visited[ni][nj] = True

                # 6. 최단거리는 이전 위치의 거리 + 1
                step[ni][nj] = step[i][j] + 1
                q.append((ni, nj))

# 7. 사람의 위치에만 최단거리를 출력하고 나머지는 0 출력
for i in range(N):
    result = []
    for j in range(N):
        # 7-1. 사람이 없는 칸은 0
        if arr[i][j] != 2:
            result.append(0)
        # 7-2. 사람이 있지만 대피 장소까지 도달할 수 없으면 -1
        elif not visited[i][j]:
            result.append(-1)
        # 7-3. 이동할 수 있다면 최단거리 출력
        else:
            result.append(step[i][j])
    print(*result)
