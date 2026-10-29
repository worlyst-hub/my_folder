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

def gwaje(start, end):
    global count
    if start == end:
            return
    mid = (start + end - 1) // 2

    # 왼쪽 절반 정렬
    gwaje(start, mid)
    # 오른쪽 절반 정렬
    gwaje(mid + 1, end)

    # 왼쪽 마지막 원소가 오른쪽 마지막 원소보다 큰 경우, count += 1
    if arr[mid] > arr[end]:
        count += 1

    a = start
    b = mid + 1
    result = []

    while True:
        # 왼쪽, 오른쪽 모두 다 사용했다면 종료
        if a > mid and b > end: break

        # 왼쪽을 다 사용한 경우
        if a > mid:
            result.append(arr[b])
            b += 1
        # 오른쪽을 다 사용한 경우
        elif b > end:
            result.append(arr[a])
            a += 1
        # 왼쪽 값이 더 작거나 같은 경우
        elif arr[a] <= arr[b]:
            result.append(arr[a])
            a += 1
        # 오른쪽 값이 더 작은 경우
        else:
            result.append(arr[b])
            b += 1
    # 정렬된 결과를 원본 배열에 반영
    for i in range(len(result)):
        arr[start + i] = result[i]



T = int(input())
for test_case in range(1, T+1):
    N = int(input())
    arr = list(map(int, input().split()))

    count = 0
    gwaje(0, N - 1)

    print(f"#{test_case} {arr[N // 2]} {count}")

