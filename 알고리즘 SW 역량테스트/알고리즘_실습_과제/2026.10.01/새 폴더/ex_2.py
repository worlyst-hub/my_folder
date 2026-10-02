arr = [6, 8, 1, 3, 4, 5, 9, 2, 7]
# 전체를 정렬하기 위해서 절반을 각각 정렬해서 합치기

def merge_sort(start, end):
    if start == end:  # 요소가 하나인 경우에는 정렬 필요x
        return
    
    mid = (start + end) // 2
    # 왼쪽 절반 정렬
    merge_sort(start, mid)
    # 오른쪽 절반 정렬
    merge_sort(mid + 1, end)

    sorted_arr = []
    i = start
    j = mid + 1

    while i <= mid and j <= end:
        if arr[i] < arr[j]:  # 왼쪽이 더 작으면
            sorted_arr.append(arr[i])
            i += 1
        else:  # 오른쪽이 더 작거나 같으면
            sorted_arr.append(arr[j])
            j += 1

    # 남아있으면 붙이기
    while i <= mid:
        sorted_arr.append(arr[i])
        i += 1
    while j <= end:
        sorted_arr.append(arr[j])
        j += 1

    # 원본 배열에 임시 저장 배열 붙여넣기
    b = 0
    for a in range(start, end + 1):
        arr[a] = sorted_arr[b]
        b += 1


N = len(arr)
merge_sort(0, N - 1)  # 시작은 전체 범위
print(arr)
