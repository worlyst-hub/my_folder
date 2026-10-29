import sys
sys.stdin = open("sample_input.txt", "r")

"""
문제 구상
문자열에서 중복 문자를 지우고 붙이고 또 중복되면 지우고 붙이고
전부 지워지면 0을 출력
전부 지워지지 않으면 남은 문자열 길이를 출력

로직 구상
1. 문자열 s를 입력받음
2. 문자열을 하나씩 넣을 빈리스트를 만듬
3. 문자를 하나씩 빈리스트에 넣고 하나씩 넣을 때마다 마지막 글자가 같은거라면 pop으로 지우기
4. 빈리스트라면 결과 0을 출력
5. 리스트에 문자가 있으면 결과로 stack 길이를 출력
6. 결과를 테스트 케이스와 함께 출력
"""

T = int(input())
for test_case in range(1, T+1):
    # 1. 문자열 s를 입력받음
    s = input()
    # 2. 문자열을 하나씩 넣을 빈리스트를 만듬
    stack = []
    # 4, 5-1. 결과 초기값 세팅 
    result = 0
    # 3. 문자를 하나씩 빈리스트에 넣고 하나씩 넣을 때마다 마지막 글자가 같은거라면 pop으로 지우기
    # 3-1. 문자를 하나씩 빈리스트에 넣기
    for alpha in s:
        # 3-2. 빈리스트이거나 문자가 마지막 글자와 다르다면 하나씩 추가
        if not stack or alpha != stack[-1]:
            stack.append(alpha)
        # 3-3. 문자가 마지막 글자와 같다면 마지막 글자를 지우기
        elif alpha == stack[-1]:
            stack.pop()
    # 4. 빈리스트라면 결과 0을 출력
    if not stack:
        result = 0
    # 5. 리스트에 문자가 있으면 결과로 stack 길이를 출력
    else:
        result = len(stack)

    # 6. 결과를 테스트 케이스와 함께 출력
    print(f"#{test_case} {result}")

