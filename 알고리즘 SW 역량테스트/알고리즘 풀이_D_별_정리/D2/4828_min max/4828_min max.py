"""
로직 구상
숫자를 하나씩 보면서 가장 큰 수와 가장 작은 수를 골라내 둘의 차이를 계산

왜 안됐는지
한 줄을 입력받는 건데 for문으로 여러 줄을 받으려고 했음
"""

# import sys
# sys.stdin = open("sample_input.txt", "r")

T = int(input())
for test_case in range(1, T + 1):
    N = int(input())
    nums = list(map(int, input().split()))
    
    max_num = nums[0]
    min_num = nums[0]
    for num in nums:
        if max_num < num:
            max_num = num
        if min_num > num:
            min_num = num
            
    print(f"#{test_case} {max_num - min_num}")
