# 요소의 개수가 N개의 배열에서
# 길이 M인 모든 구간의 합을 구하기
# 길이 M인 모든 구간의 합을 구하기 위해서
# 구간의 시작점을 설정
# 시작점 : 0번부터 N-M까지
# 각 시작점에서 길이 M 만큼의 합 구하기
T = int(input())
for test_case in range(1, T + 1):
    # 테스트 케이스의 첫번째 줄 입력받기
    N, M = map(int, input().split())
    # 테스트 케이스의 두번째 줄 입력받기
    numbers = list(map(int, input().split()))
    # 시작점이 여러개니까... 시작점 먼저 설정
    max_sum = 0
    min_sum = 1000000
    for i in range(N - M + 1):  # 0번부터 N-M까지
        # 각 시작점에서 길이 M 만큼의 합 구하기
        # i 번부터 i+M-1번까지 돌면서 합 구하기
        sum_v = 0
        for j in range(i, i + M):  # 구간을 순회하는 반복문
            sum_v = sum_v + numbers[j]
        if sum_v > max_sum:
            max_sum = sum_v
        if sum_v < min_sum:
            min_sum = sum_v

    print(f"#{test_case} {max_sum - min_sum}")







# import sys
# sys.stdin = open("sample_input.txt", "r")

# T = int(input())
# for test_case in range(1, T + 1):
#     N, M = map(int, input().split())
#     arr = list(map(int, input().split()))
#
#     max_sum = 0
#     min_sum = 100000000000000000
#     for i in range(N - M + 1):
#         current_sum = 0
#         for j in range(M):
#             current_sum += arr[i + j]
#         if max_sum < current_sum:
#             max_sum = current_sum
#         if min_sum > current_sum:
#             min_sum = current_sum
#
#     print(f"#{test_case} {max_sum - min_sum}")
