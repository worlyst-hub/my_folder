import sys
import os
sys.stdin = open(os.path.join(os.path.dirname(__file__), "input.txt"), "r")

"""
문제 구상
8개의 숫자로 이루어진 암호코드
올바른 암호코드인지, 잘못된 암호코드인지 판별해라

올바른 암호코드 : ((홀수 자리의 합 * 3) + (짝수 자리의 합))이 10배수인 것
잘못된 암호코드 : 10의 배수가 아닌 것

로직 구상


"""

T = int(input())
for test_case in range(1, T+1):
    N, M = map(int, input().split())

    code = 