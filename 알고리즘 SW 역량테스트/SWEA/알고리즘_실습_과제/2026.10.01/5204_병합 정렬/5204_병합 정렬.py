import sys
import os
sys.stdin = open(os.path.join(os.path.dirname(__file__), "sample_input.txt"), "r")

"""
문제 구상

병합 정렬을 통해 오름차순으로 정렬하는 과제 받음
문제를 풀 때 병합정렬을 사용했는지 확인하기 위해 제약을 주셨음
분할 > [0 : N // 2],, [N // 2 : N]

병합 과정에서 // 왼쪽 마지막 원소 > 오른쪽 마지막 원소 // 경우의 수
정렬이 끝난 상태에서 [N // 2]원소를 출력
최종적으로 test_case // [N // 2] // 경우의 수 출력
"""

# 병합 정렬
def merge_sort(arr):
    global count

    length = len(arr)

    # 원소가 1개라면 이미 정렬된 상태
    if length == 1:
        return arr

    mid = length // 2

    # 왼쪽 / 오른쪽 절반으로 나누기
    left_arr = arr[ : mid]
    right_arr = arr[mid : ]

    # 각각 정렬
    left_arr = merge_sort(left_arr)
    right_arr = merge_sort(right_arr)

    # 문제에서 요구하는 조건
    # 왼쪽 마지막 원소가 오른쪽 마지막 원소보다 크다면
    if left_arr[-1] > right_arr[-1]:
        count += 1

    # 두 배열 병합
    sorted_arr = []

    while left_arr and right_arr:
        if left_arr[0] < right_arr[0]:
            sorted_arr.append(left_arr.pop(0))
        else:
            sorted_arr.append(right_arr.pop(0))

    # 남은 원소 붙이기
    sorted_arr += left_arr
    sorted_arr += right_arr

    return sorted_arr


T = int(input())
for test_case in range(1, T + 1):
    N = int(input())
    arr = list(map(int, input().split()))

    count = 0
    result = merge_sort(arr)

    print(f'#{test_case} {result[N // 2]} {count}')