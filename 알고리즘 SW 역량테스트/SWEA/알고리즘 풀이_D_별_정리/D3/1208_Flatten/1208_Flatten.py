import sys
sys.stdin = open("input.txt", "r")

T = 10
for test_case in range(1, T + 1):
    N = int(input())
    boxes = list(map(int, input().split()))

    for _ in range(N):

        max_idx = 0
        min_idx = 0
        for i in range(1, 100):
            if boxes[max_idx] < boxes[i]:
                max_idx = i
            if boxes[min_idx] > boxes[i]:
                min_idx = i

        boxes[max_idx] -= 1
        boxes[min_idx] += 1

    max_idx = 0
    min_idx = 0
    for i in range(1, 100):
        if boxes[max_idx] < boxes[i]:
            max_idx = i
        if boxes[min_idx] > boxes[i]:
            min_idx = i

    result = boxes[max_idx] - boxes[min_idx]

    print(f"#{test_case} {result}")