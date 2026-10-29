arr = [5,6,1,4,3,9,3,8]

max_v = 0
for num in arr:
    if num > max_v:
        max_v = num

max_v = 0
for i in range(len(arr)):
    if arr[i] > max_v:
        max_v = arr[i]

print(max_v)

max_idx = 0
for i in range(len(arr)):
    if arr[i] > arr[max_idx]:
        max_idx = i

print(arr[max_idx])



