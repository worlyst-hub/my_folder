# # 버블 정렬
# # [5, 2, 3, 1, 4]
# # >> [1, 2, 3, 4, 5]
# # 2개씩 비교해서 큰거 보내는 작업 x N번 하기
# # 2개씩 비교해서 큰거 뒤로 보내기
# arr = [5, 2, 3, 1, 4]
# N = len(arr)
# for _ in range(N):
#     for i in range(N-1):
#         # i번과 i+1과 비교해서
#         # i번이 크면 자리 바꿔주기
#         if arr[i] > arr[i+1]:
#             # 자리 바꿔주기
#             # arr[i+1], arr[i] = arr[i], arr[i+1]
#             tmp = arr[i]
#             arr[i] = arr[i+1]
#             arr[i+1] = tmp
#
# print(arr)

# # 카운팅 정렬
# # 스킬 >>
# # 값을 배열의 인덱스로 사용하기
# a = [1, 4, 3, 2, 1, 1, 3, 4, 5]
# # a의 요소가 각 몇 번 나왔는지 세는 배열
# b = [0] * 10  # 0번부터 9번 인덱스까지 존재
#
# for i in range(len(a)):
#     # a[i] # a의 요소
#     b[a[i]] += 1
# -------------------------------------------------------------------------------------
# 1. 요소의 개수 세기
# 2. 누적합 구하기(내자리 계산하기)
# 3. 자리 찾아서 넣어주기
arr = [4, 6, 1, 8, 9, 3, 4, 2, 1, 2, 3, 2, 3, 4, 5, 1]
N = len(arr)
cnt = [0] * 10
sorted_arr = [0]*N
# 1. 요소 개수 세기
for i in range(N):
    num = arr[i]
    cnt[num] += 1
# 2. 누적합 구하기
for i in range(1, 10):  # 0번은 누적합 계산x
    # 앞 인덱스 값과 현재 인덱스 값 더해서 현재 인덱스에 재할당
    cnt[i] = cnt[i-1] + cnt[i]
# 3. 제 위치에 맞게 넣어주기
# 원본 arr의 요소가 들어갈 위치를 cnt배열에서 확인하고 sorted_arr에 넣어주기
for i in range(N):
    num = arr[i]
    cnt[num] -= 1  # 들어갈 순번을 인덱스로 변경하기 및 다음 값 순번 계산
    idx = cnt[num]
    sorted_arr[idx] = num
    # sorted_arr[cnt[arr[i]]-1] = arr[i]
    # cnt[arr[i]] -= 1
print(sorted_arr)





