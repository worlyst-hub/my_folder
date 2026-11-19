import sys

# sys.stdin = open("input.txt", "r")  # 로컬 파일 테스트 시 주석 해제

"""
문제 구상
N개의 정점과 M개의 간선으로 구성된 양방향 그래프가 있다.
K개의 정점이 순서대로 주어지면 그 순서대로 이동할 수 있는지 확인한다.
두 정점 사이에 직접 간선이 없어도 다른 정점을 거쳐 이동할 수 있다.
전부 이동 가능하면 1, 하나라도 이동할 수 없다면 0을 출력한다.

로직 구상
1. 정점 개수 N, 간선 개수 M, 경로의 길이 K를 입력받는다.
2. 각 정점의 부모 배열을 만든다. # Union-Find
3. 각 정점이 속한 그룹의 대표를 찾는 함수를 만든다. # find
4. 두 정점이 속한 그룹을 합치는 함수를 만든다. # union
5. M개의 간선을 입력받아 연결된 정점들을 같은 그룹으로 만든다.
6. K개의 정점으로 이루어진 이동 순서를 입력받는다. # 리스트
7. 연속된 두 정점이 같은 그룹에 있는지 차례대로 확인한다.
8. 모든 정점으로 이동할 수 있으면 1, 불가능한 구간이 있으면 0을 출력한다.
"""

# 1. 정점의 개수 N, 간선의 개수 M, 이동 경로의 길이 K 입력
N, M, K = map(int, input().split())

# 2. 각 정점의 부모를 자기 자신으로 초기화 # Union-Find
parent = [i for i in range(N + 1)]
# 4-1. 그룹의 크기를 기록해 작은 그룹을 큰 그룹에 연결한다.
size = [1] * (N + 1)


# 3. 정점 x가 속한 그룹의 대표를 찾는다. # find
def find(x):
    # 3-1. 자기 자신이 대표라면 그대로 반환
    if parent[x] == x:
        return x

    # 3-2. 부모를 따라가며 대표를 찾는다.
    # 3-3. 찾은 대표를 저장해 다음 탐색을 빠르게 한다. # 경로 압축
    parent[x] = find(parent[x])
    return parent[x]


# 4. 두 정점이 속한 그룹을 하나로 합친다. # union
def union(x, y):
    # 4-2. 연결된 두 정점의 대표 번호 확인
    root_x = find(x)
    root_y = find(y)

    # 4-3. 이미 같은 그룹이면 합칠 필요가 없다.
    if root_x == root_y:
        return

    # 4-4. 작은 그룹을 큰 그룹 밑에 연결한다.
    if size[root_x] < size[root_y]:
        root_x, root_y = root_y, root_x
    parent[root_y] = root_x
    size[root_x] += size[root_y]


# 5. M개의 간선을 하나씩 입력받아 연결 관계를 만든다.
for _ in range(M):
    a, b = map(int, input().split())
    # 5-1. 양방향으로 연결된 정점은 하나의 그룹으로 만든다.
    union(a, b)

# 6. 주어진 정점의 이동 순서를 리스트로 만든다.
path = list(map(int, input().split()))

# 8-1. 처음에는 모든 위치로 이동 가능하다고 가정한다.
result = 1

# 7. 현재 정점에서 다음 정점으로 이동 가능한지 확인
for i in range(K - 1):
    # 7-1. 대표가 다르면 두 정점은 연결되어 있지 않다.
    if find(path[i]) != find(path[i + 1]):
        # 8-2. 이동할 수 없는 구간이 하나라도 있다면 0으로 변경
        result = 0
        break

# 8. 이동 가능 여부 출력
print(result)
