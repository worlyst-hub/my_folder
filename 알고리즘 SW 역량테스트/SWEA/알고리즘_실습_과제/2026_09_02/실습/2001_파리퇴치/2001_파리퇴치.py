T = int(input())
for test_case in range(1, T + 1):
    N, M = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(N)]
    # 파리채로 잡은 파리의수 중 제일 큰 값에 대한 초기값 세팅
    max_sum = 0
    # 파리채가 도는 범위 설정
    for i in range(N - M + 1):
        for j in range(N - M + 1):
            # 파리채로 잡은 파리의 수 초기값 세팅
            sum_v = 0
            # 돌면서 파리를 잡기
            for a in range(i, i + M):
                for b in range(j, j + M):
                    # 잡은 파리를 전부 더하기
                    sum_v += arr[a][b]
            # 만약 현재 파리를 잡은 수가 제일 큰 값보다 크다면 재할당
            if sum_v > max_sum:
                max_sum = sum_v

    print(f"#{test_case} {max_sum}")



"""
풀이 구상

"""



























