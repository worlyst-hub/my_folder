# nqueen 경우의 수 찾기
# N*N크기의 체스판에 N개의 퀸을 놓을 수 있는 경우의 수 찾기
N = 4
case = [-1] * N
# 모든 경우의 수 다 살펴보기



# row 행에 퀸 놓아보기
def nqueen(row):
    if row == N:  # 모든 행에 숫자 넣어봤음!
        print(case)
        return
    for col in range(N):
        case[row] = col
        nqueen(row+1)

nqueen(0)