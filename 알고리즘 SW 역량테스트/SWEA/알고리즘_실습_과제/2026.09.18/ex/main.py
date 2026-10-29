# 시간복잡도!!! = 기본연산 수행횟수 + 입력받는 데이터를
#                종합적으로 고려해서 계산하는 점근적 표기법

# import sys
# import os
# sys.stdin = open(os.path.join(os.path.dirname(__file__), "input.txt"), "r")

# a = 13
# b = bin(a)  # 2진수
# c = oct(a)  # 8진수
# d = hex(a)  # 16진수
#
# print(b, c, d)
# print(type(b))
#
# # 다시 10진수로 b, c, d 값을 바꿔보다
# print(int(b, 2))
# print(int(c, 8))
# print(int(d, 16))

# 10진수 17을 3진수로 바꾸기

# a = 17
# trans = ""
# while a != 0:
#     rest = a % 3
#     trans += str(rest)
#     a //= 3
#
# answer = trans[::-1]
# print(answer)
#
# result = int(answer, 3)
# print(result)

from decimal import Decimal
a = Decimal('1.2') - Decimal('1.1')
print(a)

a = 1.2 - 1.1
print(a)

a = 1.25
print(f'{a:.1f}')
a = 1.35
print(f'{a:.1f}')
# 파이썬은 반올림을 가까운 짝수쪽으로 한다...
print(round(4.5))  # 4
print(round(5.5))  # 6

# 1.25를 정확하게!! 표현하고 싶다!!
# 1.25 -> '1.25' -> .빼버리기 -> 10으로 나누기 -> 출력할 때 소수점 따로 출력하기
a = 1.25
a = str(a)
a = int(a.replace(".", ''))  # '125'
a = ((a+5) // 10)
print(a)
print(f"{a // 10}.{a % 10}")
