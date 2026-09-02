# 이전 충전 정류장에서 현재 정류장에 올 수 있는지 확인
# 만약에 도착이 불가능하면 직전 정류장에서 충전해야 한다.
# 마지막 충전 정류장을 저장하면서 풀이 진행

T = int(input())
for test_case in range(1, T + 1):
    K, N, M = map(int, input().split()):
    stations = list(map(int, input().split()))

    last = 0  # 마지막 충전 위치
    count = 0  # 충전 횟수

    # 1. 현재 정류장과 이전 정류장의 거리 차이 구하기... K를 초과하면 목적지 도착 불가능
    # 2. 마지막 충전소에서 현재 정류장에 도착가능한지 확인하고, 도착 불가능하면 이전 정류장에서 충전하기
    stations.insert(0, 0)
    stations.append(N)
    for i in range(1, M+2):  # 시작 정류장과 목적지 정류장 추가
        # 현재 정류장과 이전 정류장의 거리 차이 구하기
        if stations[i] - stations[i-1] <= K:
            # 도착 가능하면...
            count = 0  # 목적지 도착 불가능
            break  # 더이상 안 돌아도 됨
        # 마지막 충전소에서 현재 정류장에 도착가능한지
        # 도착 불가능하면 >> 이전 정류장에서 충전하기
        if last + K < stations[i]:
            last = stations[i-1]  # 이전 정류장에서 충전
            count += 1

    print(f"#{test_case} {count}")