def pre_order(T):
    global cnt
    if T:
        cnt += 1
        pre_order(left[T])
        pre_order(right[T])



T = int(input())
for test_case in range(1, T+1):
    # 간선의 개수 E, 서브트리 루트 N
    E, N = map(int, input().split())
    V = E + 1  # 마지막 정점 번호

    arr = list(map(int, input().split()))

    # 부모를 인덱스로 자식번호 저장
    left = [0] * (V + 1)  # N번 인덱스 필요
    right = [0] * (V + 1)

    for i in range(E):
        p, c = arr[i * 2], arr[i * 2 + 1]
        if left[p] == 0:
            left[p] = c
        else:
            right[p] = c

    cnt = 0
    pre_order(N)
    print(f"#{test_case} {cnt}")