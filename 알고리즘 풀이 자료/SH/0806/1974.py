import sys
sys.stdin = open("input.txt", "r")

"""
초기 풀이 구상
인풋을 받아 퍼즐형태의 리스트로 만듬
for 문을 사용해 중복되지 않게 만듬
    가로, 세로 줄 중복안되게
    3 x 3 크기안에 중복 안되게
if 문을 사용해 겹치는 숫자가 없을 때 1을 출력, 그렇지 않을 때 0을 출력
"""

# 10개의 스도쿠 게임 만듬
T = int(input())                                      # 테스트 케이스를 몇 번 반복할 건지 개수가 입력됨 문제의 경우 10번 반복
for test_case in range(1, T + 1):                     # 10번 반복이기 때문에 range를 사용해 1부터 10까지 반복
    puzzle = []                                       # 9x9의 리스트를 만들 빈 리스트 생성
    for i in range(9):                                # 리스트에 0부터 8까지 총 9개의 인덱스 범위를 설정
        raw_data = list(map(int, input().split()))    # raw_data를 리스트 형식으로 불러오는 코드
        puzzle.append(raw_data)                       # 불러온 raw_data를 빈리스트인 puzzle에 추가


    for nums in puzzle:
        row = []
        for num in nums:
            row.append(num)



