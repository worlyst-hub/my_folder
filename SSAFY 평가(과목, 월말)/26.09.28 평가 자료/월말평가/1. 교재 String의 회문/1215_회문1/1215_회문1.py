import sys
sys.stdin = open("input.txt", "r")



# 길이가 M인 회문의 개수를 구하는 함수
def solve(data):
    cnt = 0

    # 가로 방향 검사
    for i in range(8):
        # 길이 M짜리 문자열이 시작할 수 있는 위치
        for j in range(8 - M + 1):

            is_find = True

            # 앞과 뒤를 하나씩 비교
            for k in range(M // 2):
                if data[i][j + k] != data[i][j + M - 1 - k]:
                    is_find = False
                    break

            # 회문이라면 개수 증가
            if is_find:
                cnt += 1

    # 세로 방향 검사
    for i in range(8):
        # 길이 M짜리 문자열이 시작할 수 있는 위치
        for j in range(8 - M + 1):

            is_find = True

            # 위와 아래를 하나씩 비교
            for k in range(M // 2):
                if data[j + k][i] != data[j + M - 1 - k][i]:
                    is_find = False
                    break

            # 회문이라면 개수 증가
            if is_find:
                cnt += 1

    return cnt


T = 10
for test_case in range(1, T + 1):
    M = int(input())
    # 8x8 글자판 입력
    data = [input().strip() for _ in range(8)]
    result = solve(data)
    print(f"#{test_case} {result}")