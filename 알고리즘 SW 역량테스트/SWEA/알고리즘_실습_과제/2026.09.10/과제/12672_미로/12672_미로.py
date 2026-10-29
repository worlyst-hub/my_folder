import sys
sys.stdin = open("sample_input.txt", "r")

"""
문제 구상
미로를 탈출해야한다.
통로는 0, 벽은 1, 출발지는 2, 도착지는 3이다.
모든 미로를 가보고 도착할 수 있으면 성공이라는 의미의 1을 출력하고
도착할 수 없으면 실패라는 의미의 0을 출력한다.

로직 구상
1. 시작 위치 찾기
2. 현재 위치를 저장할 빈리스트 stack과 방문기록을 남길 리스트 초기값 세팅
3. 통로 0을 따라 미로 출발하기
4. 미로를 한 방향으로 끝까지 갔다면 되돌아온다.
5. 출발지를 기준으로 미로 탐색을 반복한다.
6. 도착지에 도착했다면 성공이라는 의미의 1을 반환한다.
7. 도착지에 도착하지 못했다면 실패라는 의미의 0을 반환한다.
8. 결과를 테스트케이스와 함께 출력한다.
"""

def dfs(maze):
    # 1. 시작 위치 찾기
    # 1-1. 미로를 순회해서 출발지(2)인 위치 찾기
    for i in range(N):
        for j in range(N):
            if maze[i][j] == 2:
                # 1-2. 출발지의 좌표 저장하기
                sr = i
                sc = j
    # 2. 현재 위치를 저장할 빈리스트 stack과 방문기록을 남길 리스트 초기값 세팅
    stack = []
    # 2-1. 현재 출발지 좌표 저장하기
    stack.append((sr, sc))
    visited = [[0] * N for _ in range(N)]
    # 2-2. 현재 위치 방문기록 남기기
    visited[sr][sc] = 1

    # 5. 출발지를 기준으로 미로 탐색을 반복한다.
    while stack:
        cr, cc = stack[-1]
        # 6. 도착지에 도착했다면 성공이라는 의미의 1을 반환한다.
        if maze[cr][cc] == 3:
            return 1

        # 3. 통로 0을 따라 미로 출발하기
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr = cr + dr
            nc = cc + dc
            # 3-1. 미로의 범위안에 들어오고 이동할 곳이 벽이 아니며 방문한 적이 없는 경우 방문하기
            if 0 <= nr < N and 0 <= nc < N and maze[nr][nc] != 1 and visited[nr][nc] == 0:
                stack.append((nr, nc))
                visited[nr][nc] = 1
                break
        # 4. 미로를 한 방향으로 끝까지 갔다면 되돌아온다.
        else:
            stack.pop()
    # 7. 도착지에 도착하지 못했다면 실패라는 의미의 0을 반환한다.
    return 0


T = int(input())
for test_case in range(1, T+1):
    N = int(input())
    maze = [list(map(int, input().strip())) for _ in range(N)]
    # 8. 결과를 테스트케이스와 함께 출력한다.
    print(f"#{test_case} {dfs(maze)}")