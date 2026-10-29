# Prim : MST를 만들어가는 알고르즘
# 1. 임의의 정점을 선택 (시작 정점)
# 2. 선택한 정점들에서 연결되는 간선 중에 최소비용 간선 선택
# 3. 최소비용 간선을 선택하면 하나의 새로운 정점이 선택
# 4. 2-3을 모든 정점이 선택될 때까지 반복

# 무향 그래프
# 정점번호, 간선개수
# 시작정점, 도착정점, 가중치
# 6 11
# 0 1 32
# 0 2 31
# 0 5 60
# 0 6 51
# 1 2 21
# 2 4 46
# 2 6 25
# 3 4 34
# 3 5 18
# 4 5 40
# 4 6 51

V, E = map(int, input().split())
# 인접행렬
adj = [[0] * (V + 1) for _ in range(V + 1)]
for _ in range(E):
    a, b, w = map(int, input().split())
    adj[a][b] = w  # a에서 b로 가는
    adj[b][a] = w  # b에서 a로 가는

for row in adj:
    print(row)
    # [0, 32, 31, 0, 0, 60, 51]
    # [32, 0, 21, 0, 0, 0, 0]
    # [31, 21, 0, 0, 46, 0, 25]
    # [0, 0, 0, 0, 34, 18, 0]
    # [0, 0, 46, 34, 0, 40, 51]
    # [60, 0, 0, 18, 40, 0, 0]
    # [51, 0, 25, 0, 51, 0, 0]

def prim(start):
    # MST에 선택된 정점들로 부터 각 정점들로 가는 비용
    weights = [0xfffffffffff] * (V + 1)
    MST = set()
    weights[start] = 0
    # 선택된 정점들에서 다른 정점으로 가는 비용 중에 최소비용 선택하기
    while True:
        if len(MST) == (V + 1):
            break

        # 다른 정점으로 가는 비용 중에 최소비용 선택하기
        min_idx = -1
        min_v = 0xfffffffffff
        for i in range(V + 1):  # i : 정점번호
            if i not in MST and weights[i] < min_v:
                min_idx = i
                min_v = weights[i]
        # 최소 비용으로 갈 수 있는 정점이 선택
        MST.add(min_idx)

        for i in range(V + 1):
            # 원래 내가 알고 있던 i번 연결비용 : weights[i]
            # min_idx가 추가되면서 새로운 연결비용 : adj[min_idx][i]
            if adj[min_idx][i] and i not in MST and adj[min_idx][i] < weights[i]:
                weights[i] = adj[min_idx][i]

    print(weights)  # [0, 21, 31, 24, 46, 18, 25]

prim(0)