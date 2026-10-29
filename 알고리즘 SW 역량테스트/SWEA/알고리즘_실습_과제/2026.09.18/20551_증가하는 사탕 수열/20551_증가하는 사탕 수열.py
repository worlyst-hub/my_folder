import sys
sys.stdin = open("sample_input.txt", "r")

"""
문제 구상
상자 세 개가 있음
세 개의 상자는 각각 사탕이 들어있음
사탕을 먹고 난 후 
각 상자에 사탕이 최소한 1개는 들어있어야 하며
첫번째 보다 두번째가 더 많기를 원하고 두번째 보다 세번째가 더많기를 원함(1 < 2 < 3)
사탕을 최소 몇개를 먹어야 하는지 구하기

로직 구상

"""

T = int(input())
for test_case in range(1, T+1):
    boxes = list(map(int, input().split()))

    eat = 0
    for i in range(2):
        if boxes[i] >= boxes[i + 1]:
            if boxes[i + 1] > 1:
                eat += boxes[i] - boxes[i + 1] + 1
                boxes[i] = boxes[i + 1] - 1
            else:
                eat = -1
                break

    print(f"#{test_case} {eat}")



