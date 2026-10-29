import sys
sys.stdin = open("sample_input.txt", 'r')

"""
풀이 구상
가로 세로 10칸의 격자가 그려진 도화지가 있음
빨간색과 파란색으로 정해진 구역에 색을 칠하는데
겹쳐진 구역은 색이 섞여 보라색으로 칠해짐
보라색으로 칠해진 구역의 개수를 출력

로직 구상
1. 10x10 크기의 공간을 만든다.
2. 시작 위치부터 끝 위치까지 모든 칸을 확인하면서
    빨간색이면 1을 더한다.
    파란색이면 2를 더한다.
3. 모든 색칠이 끝난 후 10x10 전체를 확인한다.
4. 값이 3인 칸의 개수를 센다.
5. 그 개수를 출력한다.
"""

T = int(input())
for test_case in range(1, T + 1):
    N = int(input())
    # 공간을 0으로 채운, 10x10 크기의 공간을 만듬
    arr = [[0] * 10 for _ in range(10)]
    for _ in range(N):
        r1, c1, r2, c2, color = map(int, input().split())
        # 시작 위치부터 끝 위치까지 모든 칸을 확인
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                # 빨간색이면 1을 더하고 파란색이면 2를 더한다.
                arr[r][c] += color
    # purple(3)에 해당하는 부분을 찾기 위한 초기값 세팅
    purple = 0
    # 모든 색칠이 끝난 배열을 다시 확인해주기
    for r in range(10):
        for c in range(10):
            # 만약 Purple(3)인 부분을 확인하면 purple에 1더해주기
            if arr[r][c] == 3:
                purple += 1

    print(f"#{test_case} {purple}")

