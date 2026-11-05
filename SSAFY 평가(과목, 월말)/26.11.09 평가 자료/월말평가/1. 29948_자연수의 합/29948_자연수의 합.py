"""
자연수 1부터 N까지의 누적합 S는 다음과 같다.
S = 1 + 2 + 3 + ... + N
자연수 M이 주어질 때 누적합 S가 M 이상이 되는 N의 최솟값을 구하는 프로그램을 작성하시오.

예를 들어 M = 5인 경우,
1 + 2 + 3 = 6 이므로, 조건을 만족하는 N의 최솟값은 3이다.
"""

T = int(input())
for test_case in range(1, T+1):
    M = int(input())

    # 누적합 S가 M이상이 되는 N의 최솟값 구하기
    S = 0
    N = 0
    while S < M:
        N += 1
        S += N

    print(f"{test_case} {N}")