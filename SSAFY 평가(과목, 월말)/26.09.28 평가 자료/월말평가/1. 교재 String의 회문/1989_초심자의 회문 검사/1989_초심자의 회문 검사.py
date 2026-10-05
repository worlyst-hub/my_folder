import sys
sys.stdin = open("input.txt", "r")

"""
문제 구상
똑바로 읽어도 거꾸로 읽어도 같은 문장이면 회문이라고 함
회문인 경우 1 출력
회문이 아닌 경우 0 출력

로직 구상
1. 인풋을 받아와
2. 만약 똑바로 된것과 거꾸로 된것이 같으면 1출력
3. 아닐 경우 0출력
"""


T = int(input())
for test_case in range(1, T+1):
    word = input().strip()

    if word == word[::-1]:
        result = 1
    else:
        result = 0

    print(f"#{test_case} {result}")



T = int(input())
for test_case in range(1, T+1):
    word = input().strip()

    # 기본 초기값을 1로 세팅
    result = 1
    # 문자열을 반으로 나눴을 때
    for i in range(len(word) // 2):
        # 앞의 문자들과 뒤의 문자들이 같지 않다면
        if word[i] != word[-1-i]:
            # 결과를 0으로 재할당
            result = 0
            # 회문이 아니기 때문에 멈추기
            break

    print(f"#{test_case} {result}")

