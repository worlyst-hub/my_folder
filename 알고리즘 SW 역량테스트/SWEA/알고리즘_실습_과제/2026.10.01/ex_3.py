## arr = list(range(2, 31, 2))
## print(arr)
# arr = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]

# target = 20
# start = 0
# end = 14  # len(arr) - 1

# check = False
# while 1:
#     mid = (start + end) // 2
#     if arr[mid] == target:
#         check = True
#         break

#     if arr[mid] < target:  # 찾고자 하는 값이 중간값 보다 크다면... 우측 탐색
#         start = mid + 1

#     if arr[mid] > target:  # 찾고자 하는 값이 중간값 보다 작다면... 좌측 탐색
#         end = mid - 1

#     if start > end:
#         break

# if check:
#     print("찾았음")
# else:
#     print("못찾음")


arr = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
arr.sort()
target = 20
check = False

def binary_search(start, end):
    global check

    if start > end:
        return
    
    mid = (start + end) // 2
    if target == arr[mid]:
        check = True
        return

    if arr[mid] < target:
        binary_search(mid + 1, end)
    else:
        binary_search(start, mid - 1)

binary_search(0, 14)

if check:
    print("찾았음")
else:
    print("못찾음")