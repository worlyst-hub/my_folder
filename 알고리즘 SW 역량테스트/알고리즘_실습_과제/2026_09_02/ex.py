

# # 7 8 9
# N = int(input())
#
# # arr = [list(map(int, input().split())) for _ in range(N)]
# # [x for x in range(5)]     [0, 1, 2, 3, 4]
# # print(arr)
# arr = []
# for _ in range(N):
#     row = list(map(int, input().split()))
#     arr.append(row)
# print(arr)
#


# T = int(input())
# for test_case in range(1, T + 1):
#     N, M = map(int, input().split())
#     arr = [list(map(int, input().split())) for _ in range(N)]
#
#     max_flower = 0
#
#     dr = [-1, -1, 1, 1]
#     dc = [-1, 1, -1, 1]
#
#     for i in range(N):
#         for j in range(M):
#
#             flower = arr[i][j]
#
#             for k in range(4):
#                 nr = i + dr[k]
#                 nc = j + dc[k]
#
#                 if 0 <= nr < N and 0 <= nc < M:
#                     flower += arr[nr][nc]
#                 else:
#                     flower += 0
#
#             if max_flower < flower:
#                 max_flower = flower
#
#     print(f"#{test_case} {max_flower}")

# arr = [
#     [1, 2, 3, 4, 5],
#     [5, 4, 3, 2, 1],
#     [2, 4, 6, 8, 10],
#     [1, 3, 5, 7, 9],
#     [10, 8, 6, 4, 2]
# ]
# di = [-1, -1, 1, 1]
# dj = [-1, 1, -1, 1]
#
# N = len(arr)
# i = 2
# j = 3
# sum_v = arr[i][j]
# for d in range(4):
#     ni = i + di[d]
#     nj = j + dj[d]
#     sum_v += arr[ni][nj]
# print(sum_v)

# arr = [
#     [1, 2, 3, 4, 5],
#     [5, 4, 3, 2, 1],
#     [2, 4, 6, 8, 10],
#     [1, 3, 5, 7, 9],
#     [10, 8, 6, 4, 2]
# ]
# di = [-1, -1, 1, 1]
# dj = [-1, 1, -1, 1]
#
# N = len(arr)
# i = 2
# j = 3
# sum_v = arr[i][j]
# K = 2
# for k in range(1, K+1):
#     for d in range(4):
#         # K번 더하면.. 길이 K짜리 십자가 만들기
#         ni = i + di[d]*k
#         nj = j + dj[d]*K
#         # if ni >= 0 and ni < N and nj < N:
#         if 0 <= ni < N and nj < N:
#             sum_v += arr[ni][nj]
#     print(sum_v)

# arr = [
#     [1, 2, 3, 4, 5],
#     [5, 4, 3, 2, 1],
#     [2, 4, 6, 8, 10],
#     [1, 3, 5, 7, 9],
#     [10, 8, 6, 4, 2]
# ]
# di = [-1, -1, 1, 1]
# dj = [-1, 1, -1, 1]
#
# N = len(arr)
# i = 2
# j = 3
# sum_v = arr[i][j]
#
# max_v = 0
# for i in range(N):
#     for j in range(N):
#         sum_v = arr[i][j]
#         for d in range(4):
#             # K번 더하면.. 길이 K짜리 십자가 만들기
#             ni = i + di[d]
#             nj = j + dj[d]
#             # if ni >= 0 and ni < N and nj < N:
#             if 0 <= ni < N and nj < N:
#                 sum_v += arr[ni][nj]
#         if sum_v > max_v:
#             max_v = sum_v
#     print(sum_v)




























