# parametric search

battery = "*******___"

def parametric_search(start, end):
    Max = -1
    while 1:
        mid = (start + end) // 2

        if battery[mid] == '_':
            end = mid - 1

        elif battery[mid] == '*':
            Max = mid
            start = mid + 1

        if start > end:
            break

    return Max + 1


answer = parametric_search(0, 9)
print(answer)