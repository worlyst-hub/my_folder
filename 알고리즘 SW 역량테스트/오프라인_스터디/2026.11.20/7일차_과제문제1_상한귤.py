import sys
from collections import deque

# sys.stdin = open("input.txt", "r")  # 로컬 파일 테스트 시 주석 해제

"""
문제 구상
N x N 격자에 귤이 놓여 있고 처음부터 상한 귤이 K개 있다.
상한 귤은 1초마다 상하좌우에 있는 신선한 귤을 상하게 만든다.
각 귤이 최초로 상하는 시간을 구해야 한다.
빈칸은 -1, 끝까지 상하지 않는 귤은 -2를 출력한다.

로직 구상
1. 격자의 크기 N, 상한 귤의 개수 K, N x N 격자를 입력받는다. # 2차원 리스트
2. 처음부터 상한 귤들의 위치를 전부 찾아 큐에 넣는다. # 여러 시작점
3. 귤을 확인했는지 기록할 방문 배열과 상하는 시간을 기록할 배열을 만든다.
4. 큐에서 하나씩 꺼내 상하좌우를 확인한다. # BFS, 델타
5. 배열 안에 있고 신선한 귤이며 아직 방문하지 않은 경우만 이동한다.
6. 새로 상한 귤의 시간을 이전 귤의 시간 + 1로 기록하고 큐에 넣는다.
7. 모든 칸을 확인하여 빈칸은 -1, 상하지 않은 귤은 -2, 그 외에는 시간을 출력한다.
"""

# 1. N과 K를 입력받고 귤의 위치를 2차원 리스트로 만든다.
N, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]

# 2-1. BFS 탐색에 사용할 큐 생성
q = deque()

# 3. 방문 여부와 상하는 시간을 기록하는 배열 만들기
visited = [[False] * N for _ in range(N)]
step = [[0] * N for _ in range(N)]

# 4-1. 상하좌우 방향을 나타내는 델타 설정
di = [-1, 1, 0, 0]
dj = [0, 0, -1, 1]

# 2. 처음부터 상해있는 귤들을 전부 시작점으로 큐에 넣는다.
for i in range(N):
    for j in range(N):
        if arr[i][j] == 2:
            q.append((i, j))
            # 3-1. 처음부터 상한 귤은 이미 방문한 것으로 처리한다.
            visited[i][j] = True

# 4. 큐에 귤이 남아있는 동안 상하좌우로 탐색한다. # BFS
while q:
    i, j = q.popleft()

    # 4-2. 현재 귤을 기준으로 상하좌우 4방향 확인
    for k in range(4):
        ni = i + di[k]
        nj = j + dj[k]

        # 5-1. 격자 안에 들어오는 위치인지 확인
        if 0 <= ni < N and 0 <= nj < N:
            # 5-2. 신선한 귤이고 아직 방문하지 않은 경우에만 이동
            if arr[ni][nj] == 1 and not visited[ni][nj]:
                # 3-2. 방문 여부를 먼저 기록해 중복 방문을 막는다.
                visited[ni][nj] = True

                # 6. 이전 귤이 상한 시간보다 1초 뒤에 상한다.
                step[ni][nj] = step[i][j] + 1
                q.append((ni, nj))

# 7. 빈칸, 상하지 않은 귤, 상한 귤의 시간을 구분하여 출력한다.
for i in range(N):
    result = []
    for j in range(N):
        # 7-1. 귤이 없는 칸은 -1 출력
        if arr[i][j] == 0:
            result.append(-1)
        # 7-2. 귤이 있지만 방문하지 않았다면 끝까지 상하지 않은 것이므로 -2
        elif not visited[i][j]:
            result.append(-2)
        # 7-3. 상한 귤은 최초로 상한 시간 출력
        else:
            result.append(step[i][j])
    print(*result)
