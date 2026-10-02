arr = [6, 8, 1, 3, 4, 5, 9, 2, 7]
N = len(arr)

def partition(start, end):
    # 피벗을 기준으로 작은 값과 큰 값을 분리하고
    # 피벗 위치 반환
    pivot = arr[start]
    # 큰 값을 찾을 변수
    i = start + 1
    # 작은 값을 찾을 변수
    j = end

    while i <= j:
        # i를 증가 시키면서 pivot보다 큰 값 찾기
        while i <= j and arr[i] <= pivot:
            i += 1
        # j를 감소 시키면서 pivot보다 작은 값 찾기
        while i <= j and arr[j] >= pivot:
            j -= 1

        if i < j:
            # 큰 값은 뒤로 보내고, 작은 값은 앞으로 보내기
            arr[i], arr[j] = arr[j], arr[i]

    # 피벗 제자리 찾아주기
    arr[start], arr[j] = arr[j], arr[start]
    return j


def quick_sort(start, end):
    if start > end:
        return
    # 1. 피벗보다 큰 값과 작은 값으로 나누기 : partition
    pivot = partition(start, end)  # 피벗 위치 반환
    quick_sort(start, pivot - 1)
    quick_sort(pivot + 1, end)


quick_sort(0, N - 1)
print(arr)