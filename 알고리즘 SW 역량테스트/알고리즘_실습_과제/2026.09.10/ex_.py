# [
#     [0, 1, 0, 0],
#     [0, 0, 0, 1],
#     [1, 0, 0, 0],
#     [0, 0, 1, 0]
# ]

# 델타 활용
# 하나씩 놓다가 델타로 범위안에 들어가면 2로 변경
# 다음 0에 1 놓고 범위안에 들어가면 2로 변경
# 반복 만약 1이 4(N)개가 아니라면 초기화하고 이전거 다음부터 다시 놓기 시작
# 그렇게 4개가 되면 정답 출력

N = 4
chess_board = [[0] * N for _ in range(N)]

print(chess_board)

# queen의 이동 방향 정하기 좌상, 상, 우상, 좌, 우, 좌하, 하, 우하
di = [-1, -1, -1, 0, 0, 1, 1, 1]
dj = [-1, 0, 1, -1, 1, -1, 0, 1]

result = 0
# 체스판 순회
for i in range(N):
    for j in range(N):
        # 현재 자기 위치 1로 변경
        if chess_board[i][j] == 0:
            chess_board[i][j] = 1
            # 현재 자기 위치를 기준으로 방향 정하기(자기 자신은 포함x)
            for d in range(1, N):
                for k in range(8):
                    ni = i + di[k]*d
                    nj = j + dj[k]*d
                    # 방향에 따라 체스 범위안에 있는 queen의 경로에 해당하는 범위를 2로 변경
                    if 0 <= ni < N and 0 <= nj < N:
                        if chess_board[ni][nj] == 0:
                            chess_board[ni][nj] = 2
count = 0
for i in range(N):
    for j in range(N):
        if chess_board[i][j] == 1:
            count += 1

            if count == 4:
                result += 1
            else:
                count = 0


            for row in chess_board:
                print(row)


