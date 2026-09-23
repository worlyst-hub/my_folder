# 월말평가 대비!
# 인덱스 하나씩 살펴보면서 이전 인덱스와 현재인덱스 비교
# 현재 인덱스 숫자가 크면 >> 구간길이 증가
# 구간이 끝나면(data가 끝이 나거나, 숫자가 작아진 경우)
# 구간의 길이가 최대인지 확인하고 교체

T = int(input())
for test_case in range(1, T + 1):
    N = int(input())
    carrots = list(map(int, input().split()))

    # 당근 하나씩 살펴보면서 앞 당근이랑 크기비교
    # i 번, i-1 번을 비교, 0번 비교 불필요
    length = 1  # 구간의 최소길이가 1이기 때문에
    # 증가하는 구간의 최대값을 저장해야 하니...
    max_length = 1
    for i in range(1, N):
        # 현재 당근의 크기가 이전 당근 보다 크면
        if carrots[i] > carrots[i - 1]:
            length += 1

        else:  # 현재 당근의 크기가 이전 당근보다 작거나 같으면
            # 증가하는 구간이 끝난거니... 구간의 길이가 몇인지 확인
            if length > max_length:
                max_length = length
            # 최장구간 여부와 관계없이 구간의 길이는 초기화
            length = 1

    # data가 끝나면 작아지는 당근이 없어서 계산이 안될 수 있음
    if length > max_length:
        max_length = length

    print(f"#{test_case} {max_length}")

# 프로그램이 내 생각대로 돌아가는지 잠시 멈춰놓고 확인하기!
# 1
# 5
# 1 1 3 3 5