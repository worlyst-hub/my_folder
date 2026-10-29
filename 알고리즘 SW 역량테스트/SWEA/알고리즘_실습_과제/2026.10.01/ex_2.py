# arr = [4, 7, 1, 6, 2, 8, 5, 3, 9]
# start = 0
# end = 8
# pivot = start
# a = start + 1
# b = end

# while 1:
#     while a <= end and arr[a] <= arr[pivot]: a += 1  # 배열범위 안이고, a의 값이 pivot보다 작다면
#     while b >= start and arr[b] > arr[pivot]: b -= 1  # 배열범위 안이고, b의 값이 pivot보다 크다면
#     if a > b: break
#     arr[a], arr[b] = arr[b], arr[a]
# arr[b], arr[pivot] = arr[pivot], arr[b]
# print(*arr)


arr = [4, 7, 1, 6, 2, 8, 5, 3, 9]

def quick(start, end):
    if start >= end:
        return

    pivot = start
    a = start + 1
    b = end

    while 1:
        while a <= end and arr[a] <= arr[pivot]: a += 1  # 배열범위 안이고, a의 값이 pivot보다 작다면
        while b >= start and arr[b] > arr[pivot]: b -= 1  # 배열범위 안이고, b의 값이 pivot보다 크다면
        if a > b: break
        arr[a], arr[b] = arr[b], arr[a]
    arr[b], arr[pivot] = arr[pivot], arr[b]


    quick(start, b - 1)
    quick(b + 1, end)


quick(0, 8)
print(*arr)