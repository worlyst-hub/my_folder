# 병합정렬 할건데
# .sort() 쓴건지 병합정렬 쓴건지 어떻게 아냐?
# 병합할 때 확인
# 병합 : 정렬된 2개 합치기
# [1, 4, 5] + [3, 6, 7] >> [1, 3, 4, 5, 6, 7]

import sys
import os
sys.stdin = open(os.path.join(os.path.dirname(__file__), "sample_input.txt"), "r")

### 나누기만
# def merge_sort(arr):
#     # 전체를 정렬하기 위해서
#     # 각 절반을 각각 정렬
#     # 병합

#     # 각각 절반씩 나누기
#     L = len(arr)
#     if L == 1:
#         return arr
#     left = arr[ : L//2]
#     right = arr[L//2 : L]
#     left = merge_sort(left)
#     right = merge_sort(right)

#     # 병합
#     # 절반씩 나눈거에서 하나하나 비교한다음 작은거 넣기
#     merged_arr = []
#     while left and right:  # 왼쪽, 오른쪽 배열에 값이 둘 다 남아 있을 때
#         # 각각 정렬되어 있으니까.. 제일 왼쪽(0번)끼리 비교
#         if left[0] < right[0]:
#             merged_arr.append(left.pop(0))
#         else:
#             merged_arr.append(right.pop(0))
#     # 왼쪽, 오른쪽 두 배열 중 한 배열은 남아있는 상태
#     while left:
#         merged_arr.append(left.pop(0))
#     while right:
#         merged_arr.append(right.pop(0))

#     return merged_arr


# T = int(input())
# for test_case in range(1, T+1):
#     N = int(input())
#     arr = list(map(int, input().split()))
#     arr = merge_sort(arr)
#     print(f"#{test_case} {arr[N//2]}")


# ### count 포함
# def merge_sort(arr):
#     global count   ###
#     # 전체를 정렬하기 위해서
#     # 각 절반을 각각 정렬
#     # 병합

#     # 각각 절반씩 나누기
#     L = len(arr)
#     if L == 1:
#         return arr
#     left = arr[ : L//2]
#     right = arr[L//2 : L]
#     left = merge_sort(left)
#     right = merge_sort(right)

#     if left[-1] > right[-1]:  ###
#         count += 1

#     # 병합
#     # 절반씩 나눈거에서 하나하나 비교한다음 작은거 넣기
#     merged_arr = []
#     while left and right:  # 왼쪽, 오른쪽 배열에 값이 둘 다 남아 있을 때
#         # 각각 정렬되어 있으니까.. 제일 왼쪽(0번)끼리 비교
#         if left[0] < right[0]:
#             merged_arr.append(left.pop(0))
#         else:
#             merged_arr.append(right.pop(0))
#     # 왼쪽, 오른쪽 두 배열 중 한 배열은 남아있는 상태
#     while left:
#         merged_arr.append(left.pop(0))
#     while right:
#         merged_arr.append(right.pop(0))

#     return merged_arr


# T = int(input())
# for test_case in range(1, T+1):
#     N = int(input())
#     arr = list(map(int, input().split()))
#     count = 0  ###
#     arr = merge_sort(arr)
#     print(f"#{test_case} {arr[N//2]} {count}")



###
def merge_sort(start, end):
    global count
    if start == end:
        return

    mid = (start + end - 1) // 2
    merge_sort(start, mid)
    merge_sort(mid + 1, end)
    if arr[mid] > arr[end]:
        count += 1

    i = start
    j = mid + 1
    tmp_arr = []

    while i <= mid and j <= end:
        if arr[i] < arr[j]:
            tmp_arr.append(arr[i])
            i += 1
        else:
            tmp_arr.append(arr[j])
            j += 1
    # 남아 있는 요소 붙이기
    while i <= mid:
        tmp_arr.append(arr[i])
        i += 1
    while j <= end:
        tmp_arr.append(arr[j])
        j += 1

    for p in range(len(tmp_arr)):
        arr[start + p] = tmp_arr[p]
    

T = int(input())
for test_case in range(1, T+1):
    N = int(input())
    arr = list(map(int, input().split()))
    count = 0
    merge_sort(0, N - 1)
    print(f"#{test_case} {arr[N//2]} {count}")