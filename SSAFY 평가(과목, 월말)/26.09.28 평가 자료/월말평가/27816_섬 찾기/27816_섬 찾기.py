# 지도를 살펴보면서 육지라면(섬이 있으니까) 섬 개수 증가시키고
# 그 섬의 모든 육지를 지우기
# 를 반복

# 연결된 육지 지우기 함수
def dfs(r, c):
    data[r][c] = 'W'
    # 상하좌우로 육지가 연결되어 있으면 같은 섬
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]
    for d in range(4):  # 사방으로 연결된 육지 탐색
        nr = r + dr[d]
        nc = c + dc[d]
        # 연결된 육지를 찾았으면, 육지 지우러 가기...
        if 0 <= nr < N and 0 <= nc < M and data[nr][nc] == 'L':
            dfs(nr, nc)

T = int(input())
for test_case in range(1, T + 1):
    N, M = map(int, input().split())
    data = [list(input()) for _ in range(N)]

    # data를 행 우선순위로 순회, << 중첩 반복
    # 육지를 찾으면 연결된 육지를 삭제  << dfs, bfs
    num_of_islands = 0
    for i in range(N):
        for j in range(M):
            if data[i][j] == 'L':  # 육지 찾기
                # 육지다!
                num_of_islands += 1
                # 이 육지와 연결된 모든 육지를 삭제(섬 지우기)
                dfs(i, j)

    print(f"#{test_case} {num_of_islands}")