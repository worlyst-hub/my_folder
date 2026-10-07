# 우선순위 큐
import heapq
# arr = []
# heapq.heappush(arr, 13)  # min heap
# heapq.heappush(arr, 5)
# heapq.heappush(arr, 17)
# heapq.heappush(arr, 9)
# print(arr)  # [5, 9, 17, 13]

###
# # print(heapq.heappop(arr))  # 5
# # print(heapq.heappop(arr))  # 9
##
# # for i in range(len(arr)):
# #     print(heapq.heappop(arr), end=' ')
##
# # while arr:
# #     node = heapq.heappop(arr)
# #     print(node, end=' ')

###
# arr = [3, 234, 23, 12, 31]
# heap = []
# for i in range(len(arr)):
#     heapq.heappush(heap, -arr[i])

# for i in range(len(arr)):
#     # print(heapq.heappop(heap)*-1, end=' ')
#     print(-heapq.heappop(heap), end=' ')

###
# arr = [3, 234, 23, 12, 31]
# arr = list(map(lambda x:-x, arr))  # arr 배열의 모든 원소에 - 붙인 후, arr 재할당
# heapq.heapify(arr)
# for i in range(len(arr)):
#     print(-heapq.heappop(arr), end=' ')