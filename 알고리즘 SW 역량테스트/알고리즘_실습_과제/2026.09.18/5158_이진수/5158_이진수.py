import sys
import os
sys.stdin = open(os.path.join(os.path.dirname(__file__), "sample_input.txt"), "r")

T = int(input())
for test_case in range(1, T+1):
    N, N_hexa = input().split()
    N = int(N)

    result = list(bin(int(N_hexa, 16)))
    result.pop(1)

    print(N)
    print(N_hexa)
    print(f"#{test_case} {result}")