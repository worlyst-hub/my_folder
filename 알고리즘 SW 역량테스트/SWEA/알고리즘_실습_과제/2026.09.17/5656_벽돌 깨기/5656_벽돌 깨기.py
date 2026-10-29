# 가장 많은 벽돌 깨뜨리는 경우의 수 찾기
# 완전 탐색 : 모든 경우의 수를 다 수행해보고
#            벽돌을 가장 많이 터트리는 경우의 수 찾기
# 구슬을 발사하는 모든 경우의 수를 고려하기
# 연쇄반응 구현
# 연쇄반응 이후 벽돌 정리

# 구슬을 쏘는 모든 경우의 수 수행하는 재귀함수
# n번째 구슬을 하나의 칸에 쏴보기...
# bricks : 현재 상태 벽돌 모양
def shoot(n, bricks):
    global min_v
    # 이미 N개의 구슬을 발사했으면...그만 쏘기
    if n == N:  # 이미 N개의 구슬을 발사했으면
        # 구슬 다 쏴 봤으니까... 벽돌 상태 확인(남아 있는 벽돌 개수 세기)
        cnt = 0
        for i in range(H):
            for j in range(W):
                if bricks[i][j]:
                    cnt += 1
        if cnt < min_v:
            min_v = cnt
        return

    # 0번부터 W-1번 칸 중에 한 칸에 구슬 쏘기
    for i in range(W):
        # 구슬 쏘기 전에... 원본 벽돌 모양을 복사해서 복사본에 구슬 쏘기
        copy_bricks = [row[:] for row in bricks]
        # i 번에 구슬 쏘기
        # n + 1 번째 구슬 쏴보기
        shoot(n+1, copy_bricks)

# 구슬을 쏘면 벽돌 깨기
def bomb(col, target_bricks):
    # sr = 0
    # sc = col
    # 연쇄 시작점 찾기
    for i in range(H):
        if target_bricks[i][col]:
            sr = i
            sc = col
            break

    queue = [(sr, sc)]
    check = [[0] * W for _ in range(H)]
    # 벽돌이 사방으로 터지니까..
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]
    while queue:
        cr, cc = queue.pop(0)
        check[cr][cc] = 1  # 터트릴 위치 표시
        length = target_bricks[cr][cc]  # 벽돌 숫자

        for d in range(4):
            for l in range(length):  # 벽돌 숫자 만큼
                nr = cr + dr[d] * l
                nc = cc + dc[d] * l
                # 벽돌이 있고, 아직 터뜨린 벽돌이 아니라면 터트릴 대상에 추가
                if 0 <= nr < H and 0 <= nc < W and target_bricks[nr][nc] and not check[nr][nc]:
                    queue.append((nr, nc))
    # 표시가 되어있는 곳 벽돌 없애주기
    for i in range(H):
        for j in range(W):
            if check[i][j]:  # 표시가 되어있으면, 벽돌 깨기
                target_bricks[i][j] = 0
    # 남은 벽돌 정리...
    # i = 벽돌 위치, j = 벽돌을 가져다 놓을 위치
    # i를 1씩 증가 시키면서.. 벽돌이라면 j 번째에 가져다 놓기
    for i in range(W):
        k = H - 1  # 벽돌을 가져다 놓을 위치(벽돌이 놓여지면 1증가)
        for j in range(H-1, -1, -1):
            # 만약에 j 번째에 벽돌이 있으면 가장 아래칸에 가져다 놓기
            if target_bricks[j][i]:
                target_bricks[j][i], target_bricks[k][i] = target_bricks[k][i], target_bricks[j][i]
                k -= 1


# 벽돌 연쇄 반응 끝나고, 중력 처리 까지 끝난 벽돌..
T = int(input())
for test_case in range(1, T+1):
    N, W, H = map(int, input().split())
    data = [list(map(int, input().split())) for _ in range(H)]
    # 남은 최소 벽돌 개수를 저장하기 위한 글로벌 변수
    min_v = 0xffffffff  # W*H면 충분
    shoot(0, data)
    print(f"#{test_case} {min_v}")