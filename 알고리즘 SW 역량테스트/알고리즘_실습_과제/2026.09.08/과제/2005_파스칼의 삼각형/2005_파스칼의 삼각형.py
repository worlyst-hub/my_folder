import sys
sys.stdin = open("input.txt", "r")

"""
문제 구상
첫째 줄에는 숫자 1이 있음
두번째 줄부터 양쪽 끝은 항상 1이고 가운데 있는 것들은 왼쪽과 오른쪽 숫자를 더해서 만듬
이걸 반복해서 숫자로 삼각형을 만듬

로직 구상
1. 만들어야 하는 삼각형의 크기 N을 입력받음
2. 첫번째 줄부터 N번째 줄까지 순서대로 만듬
3. 각 줄의 처음과 끝에는 1을 넣음
4. 처음과 끝이 아닌 위치는 이전 줄의 왼쪽 값과 오른쪽 값을 더해서 만듬
5. 완성된 한 줄을 삼각형에 추가
6. N개 줄을 모두 만든 후 테스트케이스와 함께 순서대로 출력
"""

T = int(input())
for test_case in range(1, T + 1):
    # 1. 삼각형의 크기 입력
    N = int(input())

    # 완성된 삼각형을 저장
    arr = []

    # 2. 첫 번째 줄부터 N번째 줄까지 만들기
    for i in range(N):

        # 현재 줄의 크기만큼 공간 만들기
        row = [0] * (i + 1)

        # 3. 현재 줄의 처음과 끝은 1
        row[0] = 1
        row[i] = 1

        # 4. 처음과 끝이 아닌 위치 계산
        for j in range(1, i):
            row[j] = arr[i - 1][j - 1] + arr[i - 1][j]

        # 5. 완성된 줄 추가
        arr.append(row)

    # 6. 출력
    print(f"#{test_case}")

    for row in arr:
        print(*row)