import heapq

N = int(input())  # 노드의 수
M = int(input())  # 간선의 수

arr = [[] for _ in range(N)]

# 무방향 그래프이므로 양방향 저장
for _ in range(M):
    start, end, cost = map(int, input().split())

    arr[start].append((cost, end))
    arr[end].append((cost, start))


used = [0] * N  # 내가 선택한 정점인지 체크
heap = []  # 최소 비용을 뽑기 위함

# (비용, 정점)
heapq.heappush(heap, (0, 0))  # 비용 시작정점

total = 0  # 총 비용을 합치기
count = 0  # 연결한 간선의 개수

while heap:
    cost, now = heapq.heappop(heap)

    # 이미 MST에 포함된 정점이면 무시
    if used[now] == 1:
        continue

    # MST에 정점 포함
    used[now] = 1  # 방문 체크
    total += cost  # 비용의 합
    count += 1  # 연결된 간선의 개수 1증가

    # 모든 정점을 선택했다면 종료
    if count == N:
        break

    # 현재 정점과 연결된 간선들을 우선순위 큐에 추가
    for next_cost, next_node in arr[now]:
        if used[next_node] == 0:
            heapq.heappush(heap, (next_cost, next_node))

print(total)