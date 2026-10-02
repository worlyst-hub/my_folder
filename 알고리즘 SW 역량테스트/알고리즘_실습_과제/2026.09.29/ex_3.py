# 누적합 구하기 - 재귀 DFS 구현시 변수를 global 선언하는가? 매개변수에 선언하는가? 에 따른 차이
# 1.
arr = [1, 3, 5, 7]

Sum = arr[0]

def abc(level):
    global Sum

    if level == 3:
        print(Sum, end=' ')
        return

    Sum += arr[level + 1]
    abc(level + 1)
    Sum -= arr[level + 1]
    print(Sum, end=' ')

abc(0)

# 2.
arr = [1, 3, 5, 7]

def abc(level, Sum):

    if level == 3:
        print(Sum, end=' ')
        return

    abc(level + 1, Sum + arr[level + 1])
    print(Sum, end=' ')

abc(0, arr[0])



# 재귀 DFS
def abc(level):
    # print('#')
    if level == 2:  # 탐색의 깊이
        # print('#')
        return
    
    # print('#')
    for i in range(2):
        # print('#')
        abc(level + i)
        # print('#')

    # print('#')

    # abc(level + 1)  # 개수에 따라 트리 가지의 개수
    # abc(level + 1)

abc(0)

                            #        ()
                            #      /    \
                            #    ()      ()
                            #   /  \    /  \
                            #  ()  ()  ()  ()