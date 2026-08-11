# 문제를 풀 때 하지 말아야 할 것
# SWEA의 목표


"""
파리 퇴치
(0,0) (0,1) (0,2) (0,3) (0,4)
(1,0) (1,1) (1,2) (1,3) (1,4)
(2,0) (2,1) (2,2) (2,3) (2,4)
(3,0) (3,1) (3,2) (3,3) (3,4)
(4,0) (4,1) (4,2) (4,3) (4,4)
"""

arr = [[1, 2, 3, 4, 5],
       [1, 2, 3, 4, 5],
       [1, 2, 3, 4, 5],
       [1, 2, 3, 4, 5],
       [1, 2, 3, 4, 5]]

N = len(arr)
M = 2
a = 0
b = 1


# 파리채 시작점 바꿔주기
max_sum = 0
for i in range(N - M + 1):
    for j in range(N - M + 1):
        # i, j가 시작점, i, j에서 시작하는 m*m 짜리 파리채
        sum_v = 0
        for a in range(i, i + M):
            for b in range(j, j + M):
            #     print(arr[k][l], end=' ')
                sum_v += arr[k][l]
            # print()
            print(sum_v)
        if sum_v > max_sum:
            max_sum = sum_v
    print(max_sum)

T = int(input()) # 테스트 케이스 개수
# 각 테스트 케이스 마다 N, M이 주어짐 <<< T개
for _ in range(T):
    N, M = map(int, input().split()) # N, M 을 입력받음, 문자열 가르고, 숫자로 바꾸고
    # N * M 짜리 행렬 >> 요소가 리스트인 리스트
    # arr = []
    # for _ in range(N):
       # arr.append(list(map(int, input().split())))
        # 이건 알고리즘에서 무조건 쓰임
    arr = [list(map(int, input().split())) for _ in range(N)]

    # 모든 파리채 위치 합 구해보기
    # 시작점 반복문 돌리기
    max_sum = 0
    for i in range(N - M + 1):   # 시작점 도는 반복문
        for j in range(N - M + 1):
            sum_v = 0
            for a in range(i, i + M):   # 파리채 영역을 도는 반복문
                for b in range(j, j + M):
                    sum_v += arr[a][b]
                # 파리채 영역 다 돌았으니 몇마리인지 확인
                # 현재 잡은 파리수가 제일 많으면 저장
            if sum_v > max_sum:
                max_sum = sum_v