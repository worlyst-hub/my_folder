def dfs(maze):

    # 초기화
    visited = [[0] * N for _ in range(N)]
    stack = []
    stack.append((si, sj))

    visited[si][sj] = 1

    while stack:
        ti, tj = stack[-1]
        if maze[ti][tj] == '3':
            return 1
        for di, dj in [[0,1],[1,0],[0,-1],[-1,0]]:
            ni, nj = ti + di, tj + dj
            if 0 <= ni < N and 0 <= nj < N and maze[ni][nj] != '1' and visited[ni][nj] == 0:
                stack.append((ni, nj))
                visited[ni][nj] = 1
                break
        else:
            stack.pop()
    return 0


def find_start(maze, N):
    for i in range(N):
        for j in range(N):
            if maze[i][j] == '2':
                return i, j

T = 10

for tc in range(1, T + 1):
    N = 16
    test_case = int(input())
    maze = [input() for _ in range(N)]

    si, sj = find_start(maze, N)

    print(f'#{test_case} {dfs(maze)}')