# 표준입력 스트림 : 터미널로 기본 설정 되어있음, 파일로 변경하면 파일에서 입력받기
import sys
sys.stdin = open("sample_input.txt", 'r')
sys.stdout = open("sample_output.txt", 'w')

# 현재 위치에서 갈 수 있는 위치에 충전소가 있는지 확인
# 없으면 뒤로 되돌아 가면서 충전하기

T = int(input())
for test_case in range(1, T + 1):
    # K는 충전량, N은 정류장 개수, M은 충전기 개수
    K, N, M = map(int, input().split())
    charger = list(map(int, input().split()))
    stations = [0] * (N+1)
    for idx in charger:
        stations[idx] = 1
    # for i in range(M):
    #     stations[charger[i]] = 1
    # [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    # 현재 위치에서 갈 수 있는 정류장부터 충전소가 있는지 검사
    # 없으면 되돌아 가기
    # 충전소가 있으면 충전하기 >> 반복(목적지에 도착할 때 까지)
    position = 0  # 현재 위치
    count = 0  # 충전 횟수 세기 변수
    while position + K < N:  # 충전기 찾아서 충전하기 반복
        # 갈 수 있는데 까지 가서 되돌아 오면서 찾기
        is_find = False
        for next in range(position+K, position, -1):
            if stations[next] == 1:  # 충전기 있니?
                count += 1  # 충전하고 다음 충전소 찾기
                position = next
                is_find = True
                break
        # 충전소 찾는 반복문에서 충전소 찾았니?
        if is_find == False:
            count = 0  # 목적지 도착 못할 경우 0출력
            break


        # position += K
        # if stations[position] == 1:  # 충전기 있니?
        #     count += 1  # 충전하고 다음 충전소 찾기
        # else:  # 없으면? # 뒤로 돌아가기

    print(f"#{test_case} {count}")