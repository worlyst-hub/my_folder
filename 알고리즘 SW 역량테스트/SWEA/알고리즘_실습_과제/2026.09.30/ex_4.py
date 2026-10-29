### 그리디
# 동전 교환 문제!!
coin = [500, 50, 100, 10]
target = 1110
coin.sort(reverse=True)  # [500, 100, 50, 10]

count = 0  # 사용한 동전 개수
for i in range(4):
    temp = target // coin[i]  # 
    count += temp
    target = target - (temp * coin[i])

print(count)

# 화장실 문제
poo = [15, 30, 50, 10]
poo.sort()  # [10, 15, 30, 50]
Sum = 0
for i in range(3, 0, -1):  # 대기 인원 ,, 화장실 사용 시간 아님
    Sum += (i * poo[3 - i])  # 대기 인원 * 화장실 사용 시간

print(Sum)

# fractional Knapsack 문제
bag = 30
salt = [(5, 50), (10, 60), (20, 140)]  # (kg, price)
salt.sort(key = lambda x:x[1] // x[0], reverse=True)  # kg당 단가가 높은 순서로 sort
print(salt)  # [(20, 140), (10, 60), (5, 50)]
total_value = 0  # 가방의 총 가치
for weight, price in salt:
    # 다 담을 수 있다면
    if bag >= weight:
        bag -= weight  # 담은만큼 가방 무게 빼고
        total_value += price  # 가방의 가치를 업데이트

    # 다 담을 수 없다면 ,, 가방에 담을 수 있는 가치는 = 남은 가방 무게 * 담는 물건의 단위당 단가
    else:
        total_value += (bag * (price // weight))
        bag = 0
        break

price(total_value)