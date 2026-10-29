# 재귀 이용해서 출력해보기
# 0 1 2 3 2 1 0

# 1.
def abc(level):

    print(level, end=' ')
    if level == 3:
        return

    abc(level + 1)
    print(level, end=' ')

abc(0)

# 2.
def abc(level):

    if level == 3:
        print(level, end=' ')
        return
    
    print(level, end=' ')
    abc(level + 1)
    print(level, end=' ')

abc(0)

# 0 1 2 3 4 5 5 4 3 2 1 0

def abc(level):
    print(level, end=' ')

    if level == 5:
        print(level, end=' ')
        return
    
    abc(level + 1)
    print(level, end=' ')

abc(0)