import sys
sys.stdin = open("sample_input.txt", "r")

"""
문제 구상
주어진 문장에서 괄호 {}, ()가 제대로 짝지어져있는지 검사

로직 구상
1. 문장을 입력받음
2. 괄호가 제대로 있는지 확인할 빈리스트 생성
3. 하나씩 확인하며 {, (라면 있으면 빈리스트에 append
4. }, )일 경우, 만약 리스트 안에 마지막 위치에 있는게 짝일 경우, pop으로 지우기
5. 만약 리스트가 비어있거나 짝이 아닐 경우, 실패인 0을 출력
6. 최종적으로 리스트가 비어있지 않을 경우, 실패인 0을 출력
7. 모두 짝이 맞아 리스트가 빈 리스트라면 성공인 1을 출력
8. 결과를 테스트케이스와 함께 출력
"""

T = int(input())
for test_case in range(1, T+1):
    # 1. 문장을 입력받음
    words = input()
    # 2. 괄호가 제대로 있는지 확인할 빈리스트 생성
    stack = []
    result = 1
    # 3. 하나씩 확인하며 {, (라면 있으면 빈리스트에 append
    for i in words:
        if '{' == i or '(' == i:
            stack.append(i)
        # 4. }, )일 경우, 만약 리스트 안에 마지막 위치에 있는게 짝일 경우, pop으로 지우기
        elif '}' == i:
            # 5. 만약 리스트가 비어있거나 짝이 아닐 경우, 실패인 0을 출력
            if not stack or stack[-1] != '{':
                result = 0
                break  # break를 하지 않으면 실패했는데도 계속 검사하는 상황 발생
            stack.pop()

        # 4. }, )일 경우, 만약 리스트 안에 마지막 위치에 있는게 짝일 경우, pop으로 지우기
        elif ')' == i:
            # 5. 만약 리스트가 비어있거나 짝이 아닐 경우, 실패인 0을 출력
            if not stack or stack[-1] != '(':
                result = 0
                break
            stack.pop()
    # 6. 최종적으로 리스트가 비어있지 않을 경우, 실패인 0을 출력
    if stack:
        result = 0
    # 8. 결과를 테스트케이스와 함께 출력
    print(f"#{test_case} {result}")
    


