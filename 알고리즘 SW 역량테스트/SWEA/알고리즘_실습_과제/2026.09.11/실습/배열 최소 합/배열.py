# 행 하나에서 열 하나 선택하기
# idx행에서 열하나 선택하기
# [1,0,1]
def solve(idx,check,sum_v):
    global min_v
    if sum_v >= min_v:
        return
    if idx == N:
        # print(selected_nums)
        # if min_v > sum(selected_nums):
        #     min_v = sum(selected_nums)
        if min_v > sum_v:
             min_v = sum_v
        return
 
    for i in range(N):
        if check[i] == 0:
            # selected_nums[idx] = arr[idx][i]            
            check[i] = 1
            # 하나 골랐으니까.. .다음행 고르기
            solve(idx+1, check, sum_v + arr[idx][i])
 
            check[i] = 0
 
 
 
T = int(input())
 
for tc in range(1, T + 1):
    N = int(input())
    arr = []
 
    for row in range(N):
        row = list(map(int, input().split()))
        arr.append(row)
 
    # for row in arr:
    #     print(row)
    # print(arr)
 
    # selected_nums = [0] * N
    min_v = 99999999
    solve(0,[0]*N,0)
    print(f'#{tc} {min_v}')
    # 각 행에서 모든 열
 
 
    # total = 0
    # []
    # for i in range(N):  
    #     num = 10      
    #     for j in range(N):
    #         if arr[i][j] < num:
    #             num = arr[i][j]
    #     total += num
 
    # print(total)