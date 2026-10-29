arr = ['A', 'B', 'C']
N = len(arr)
###
for tar in range(1 << N):
    answer = []
    for i in range(N):
        if tar & 1:  # if tar & 0x1:
            answer.append(arr[i])
        tar >>= 1

    print(answer)

###
for tar in range(1 << N):
    answer = []
    for i in range(N):
        if tar & 1:  # if tar & 0x1:
            answer.append(arr[i])
        tar >>= 1
    if len(answer) >= 2:  # 최소 두명 이상이 카페에 간다면
        print(answer)

