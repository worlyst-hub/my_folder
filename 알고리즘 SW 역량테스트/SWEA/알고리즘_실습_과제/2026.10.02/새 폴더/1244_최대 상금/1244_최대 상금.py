import sys
import os
sys.stdin = open(os.path.join(os.path.dirname(__file__), "input.txt"), "r")

# 카드를 한 번 교환하는 경우의 수는
# i번 카드와 그 이후에 나오는 카드 바꿔보기
# for i in range(N):
#     for j in range(i + 1, N):
#         i번과 j번을 교환

### 런타임 에러 ###
# def suffle(cards, count):
#     global max_v
#     if count == N:
#         # print(cards)
#         num = int(''.join(cards))
#         if num > max_v:
#             max_v = num
#         return

#     # 한 번 교환하는 모든 경우의 수
#     for i in range(len(cards)):
#         for j in range(i + 1, len(cards)):
#             # 카드 교환
#             cards[i], cards[j] = cards[j], cards[i]
#             # print(cards)
#             # count + 1 : 카드 교환횟수 증가
#             suffle(cards, count + 1)
#             # 원래 모양으로 바꾸기
#             cards[i], cards[j] = cards[j], cards[i]
            

# T = int(input())
# for test_case in range(1, T+1):
#     cards, N = input().split()
#     cards = list(cards)
#     N = int(N)
#     max_v = 0
#     suffle(cards, 0)

#     print(f"#{test_case} {max_v}")


def suffle(cards, count):
    global max_v
    num = int(''.join(cards))
    if (count, num) in check:  # 이미 수행해본 경우의 수인지 확인
        return
    
    check.add((count, num))  # 교환 횟수랑 상태랑 같이 저장
    if count == N:
        # print(cards)
        if num > max_v:
            max_v = num
        return

    # 한 번 교환하는 모든 경우의 수
    for i in range(len(cards)):
        for j in range(i + 1, len(cards)):
            # 카드 교환
            cards[i], cards[j] = cards[j], cards[i]
            # print(cards)
            # count + 1 : 카드 교환횟수 증가
            suffle(cards, count + 1)
            # 원래 모양으로 바꾸기
            cards[i], cards[j] = cards[j], cards[i]
            

T = int(input())
for test_case in range(1, T+1):
    cards, N = input().split()
    cards = list(cards)
    N = int(N)
    max_v = 0
    # 중복 교환을 막기위해서 set()
    check = set()
    suffle(cards, 0)

    print(f"#{test_case} {max_v}")


