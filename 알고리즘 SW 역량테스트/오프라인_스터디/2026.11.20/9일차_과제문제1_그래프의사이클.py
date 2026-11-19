import sys

# sys.stdin = open("input.txt", "r")  # 로컬 파일 테스트 시 주석 해제

"""
문제 구상
1번부터 N번까지 정점이 있는 그래프에 M개의 간선을 순서대로 추가한다.
간선을 하나씩 추가할 때 처음으로 사이클이 생기는 시점을 구해야 한다.
M개의 간선을 모두 추가해도 사이클이 없으면 happy를 출력한다.

로직 구상
1. 정점 개수 N과 간선 개수 M을 입력받는다.
2. 각 정점이 속한 그룹의 대표를 저장할 배열을 만든다. # Union-Find
3. 두 정점이 속한 그룹의 대표를 찾는 함수를 만든다. # find
4. 서로 다른 그룹을 하나로 합치는 함수를 만든다. # union
5. 간선을 입력 순서대로 확인하며 양쪽 정점의 대표가 같은지 확인한다.
6. 대표가 같다면 이미 연결된 정점들이므로 최초의 사이클 발생 시점을 기록한다.
7. 대표가 다르면 두 그룹을 합치고 다음 간선을 확인한다.
8. 사이클이 발생한 간선 번호 또는 happy를 출력한다.
"""

# 1. 정점의 개수 N과 간선의 개수 M 입력
N, M = map(int, input().split())

# 2. 각 정점의 부모를 자기 자신으로 초기화 # Union-Find
parent = [i for i in range(N + 1)]
# 4-1. 그룹의 크기도 저장해 작은 그룹을 큰 그룹에 연결한다.
size = [1] * (N + 1)


# 3. 정점 x가 속한 그룹의 대표(루트)를 찾는다. # find
def find(x):
    # 3-1. 자기 자신이 대표라면 그대로 반환
    if parent[x] == x:
        return x

    # 3-2. 대표가 아니라면 부모를 따라가 대표를 찾는다.
    # 3-3. 찾은 대표를 부모로 저장하여 다음 탐색을 빠르게 한다. # 경로 압축
    parent[x] = find(parent[x])
    return parent[x]


# 4. 두 정점이 속한 그룹을 하나로 합친다. # union
def union(x, y):
    # 4-2. 두 정점의 대표 번호 확인
    root_x = find(x)
    root_y = find(y)

    # 4-3. 이미 같은 그룹이라면 합칠 필요가 없다.
    if root_x == root_y:
        return

    # 4-4. 더 작은 그룹을 큰 그룹 밑에 연결한다.
    if size[root_x] < size[root_y]:
        root_x, root_y = root_y, root_x
    parent[root_y] = root_x
    size[root_x] += size[root_y]


# 8-1. 사이클이 생기지 않으면 출력할 초기값
result = "happy"

# 5. 간선을 입력받는 순서대로 하나씩 확인
for i in range(1, M + 1):
    a, b = map(int, input().split())

    # 5-1. 연결 전 두 정점의 대표가 같은지 확인
    # 6. 이미 같은 그룹이면 새 간선에 의해 사이클이 발생한다.
    if find(a) == find(b):
        result = i
        break

    # 7. 다른 그룹이면 연결한 뒤 다음 간선을 확인한다.
    union(a, b)

# 8. 처음 사이클이 발생한 간선의 번호 또는 happy 출력
print(result)
