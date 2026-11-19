import sys

# sys.stdin = open("input.txt", "r")  # 로컬 파일 테스트 시 주석 해제

"""
문제 구상
N x N 크기의 격자에 각각 숫자가 적혀 있다.
각 행과 각 열에서 정확히 하나씩만 선택해 총 N개의 칸을 색칠해야 한다.
조건에 맞게 칸을 선택했을 때 선택한 숫자들의 합이 가장 큰 경우를 구한다.

로직 구상
1. N과 N x N 크기의 격자를 입력받는다. # 2차원 리스트
2. 이미 선택한 열을 다시 선택하지 않도록 방문 여부를 기록한다. # visited
3. 첫 번째 행부터 하나씩 내려가며 색칠할 열을 선택한다. # 백트래킹(순열)
4. 선택한 칸의 숫자를 현재까지의 합에 더해 다음 행으로 이동한다.
5. 모든 행에서 하나씩 선택했다면 가장 큰 합을 갱신한다.
6. 선택했던 열을 다시 선택할 수 있게 되돌리고 다른 경우를 확인한다. # 백트래킹
7. 조건에 맞는 칸들의 합 중 최댓값을 출력한다.
"""

# 1. N과 N x N 크기의 격자를 입력받는다. # 2차원 리스트
N = int(input())
arr = [list(map(int, input().split())) for _ in range(N)]

# 2. 이미 색칠한 열인지 확인하기 위한 방문 리스트 만들기
visited = [False] * N

# 5-1. 가장 큰 합을 구하기 위한 초기값 세팅
max_score = 0


# 3. 현재 행에서 어떤 열을 선택할지 확인하는 함수 # 백트래킹
def find_max(row, score):
    global max_score

    # 5. 모든 행에서 하나씩 선택했으면 최댓값 갱신
    if row == N:
        if max_score < score:
            max_score = score
        return

    # 3-1. 현재 행에서 모든 열을 돌아가면서 확인
    for j in range(N):
        # 2-1. 이미 선택한 열이라면 다시 선택하지 않는다.
        if visited[j]:
            continue

        # 2-2. 현재 열을 선택했다고 표시한다.
        visited[j] = True

        # 4. 현재 칸의 숫자를 더하고 다음 행을 확인한다.
        find_max(row + 1, score + arr[row][j])

        # 6. 다른 경우도 확인할 수 있도록 방문 여부를 되돌린다.
        visited[j] = False


# 3-2. 첫 번째 행부터 현재 합 0으로 탐색 시작
find_max(0, 0)

# 7. 조건에 맞는 수들의 합 중 최댓값 출력
print(max_score)
