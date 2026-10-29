# N장의 카드를 받음
# 동일한 카드를 받은 것 중에 가장 많이 받은 카드가 무엇인지 확인

T = int(input())
for test_case in range(1, T + 1):
    N = int(input())
    cards = list(map(int, input()))

    cnt = [0] * 10
    # cnt에 각 숫자에 해당하는 인덱스에 1씩 추가
    for i in range(N):
        num = cards[i]
        cnt[num] += 1

    max_card = 0  # 가장 큰 숫자
    max_card_cnt = 0  # 가장 큰 숫자의 개수
    # 카드 번호에 따른 개수 하나씩 가져오기
    for j in range(len(cnt)):
        # 카드 개수가 저장되어있는 가장 큰 숫자의 개수보다 크다면 재할당하고 카드의 숫자를 재할당
        if cnt[j] >= max_card_cnt:
            max_card_cnt = cnt[j]
            max_card = j

    print(f"#{test_case} {max_card} {max_card_cnt}")


