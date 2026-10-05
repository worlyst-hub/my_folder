import sys
sys.stdin = open("sample_input.txt", "r")

def solve(data):

    # 가로열을 하나씩 검사하는데
    # 회문이 길이 M이기 때문에 범위를 벗어나지 않게 설정
    # i열에서 시작점부터 j까지 확인하면서 회문인지 확인
    for i in range(N):
        for j in range(N - M + 1):
            # 회문이라면 True
            is_find = True
            # 회문인지 확인할 때 반으로 나눠
            for k in range(M // 2):
                # 만약 앞부분이랑 뒤부분이랑 같지 않다면
                if data[i][j+k] != data[i][j+M-1-k]:
                    # 회문이 아니기 때문에 False로 재할당
                    is_find = False

            # 만약 회문이라면 회문을 출력
            if is_find:
                palindrome = ''
                for l in range(j, j+M):
                    palindrome += data[i][l]
                return palindrome







T = int(input())
for test_case in range(1, T+1):
    N, M = map(int, input().split())
    data = [input().strip() for _ in range(N)]
    result = solve(data)
    print(f"#{test_case} {result}")