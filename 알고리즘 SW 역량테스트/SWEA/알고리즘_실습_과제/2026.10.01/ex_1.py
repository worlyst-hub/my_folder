# arr = [2, 3, 5, 7, 1, 2, 5, 9]
# start = 0
# end = 7
# mid = (start + end) // 2

# a = start
# b = mid + 1
# result = []

# while 1:
#     if a > mid and b > end: break
#     if a > mid:
#         result.append(arr[b])
#         b += 1

#     elif b > end:
#         result.append(arr[a])
#         a += 1

#     elif arr[a] <= arr[b]:
#         result.append(arr[a])
#         a += 1

#     else:
#         result.append(arr[b])
#         b += 1

# print(*result)

arr = [2, 7, 5, 3, 1, 6, 9, 2]

def merge(start, end):
    if start == end:
        return
    mid = (start + end) // 2

    merge(start, mid)
    merge(mid + 1, end)

    a = start
    b = mid + 1
    result = []

    while 1:
        if a > mid and b > end: break
        if a > mid:
            result.append(arr[b])
            b += 1

        elif b > end:
            result.append(arr[a])
            a += 1

        elif arr[a] <= arr[b]:
            result.append(arr[a])
            a += 1

        else:
            result.append(arr[b])
            b += 1

    for i in range(len(result)):
        arr[start + i] = result[i]

merge(0, 7)
print(*arr)