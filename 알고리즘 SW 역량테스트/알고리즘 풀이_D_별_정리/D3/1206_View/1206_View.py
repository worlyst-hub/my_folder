import sys
sys.stdin = open("sample_input.txt", "r")

T = 10
for test_case in range(1, T + 1):
    N = int(input())
    buildings = list(map(int, input().split()))

    result = 0
    for i in range(2, N - 2):
        left_2 = buildings[i] - buildings[i - 2]
        left_1 = buildings[i] - buildings[i - 1]
        right_1 = buildings[i] - buildings[i + 1]
        right_2 = buildings[i] - buildings[i + 2]

        min_result = left_2
        if min_result > left_1:
            min_result = left_1
        if min_result > right_1:
            min_result = right_1
        if min_result > right_2:
            min_result = right_2

        if min_result > 0:
            result += min_result

    print(f"#{test_case} {result}")