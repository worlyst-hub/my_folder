import sys
import os
sys.stdin = open(os.path.join(os.path.dirname(__file__), "sample_input.txt"), "r")

"""
문제 구상
컨테이너 N개를 M대의 트럭으로 운반 (A > B 편도로 한번 만 운행)
컨테이너의 무게와 트럭의 적재용량이 주어짐
옮겨진 화물의 전체 무게가 얼마인가 구하라
한 개도 옮길 수 없는 경우 0을 출력
<조건>
1. 트럭 당 한 개의 컨테이너를 운반 가능
2. 트럭의 적재용량을 초과하는 컨테이너는 운반 불가


로직 구상
1. 컨테이너의 무게를 큰 순서대로 정렬한다.
2. 트럭의 적재 용량도 큰 순서대로 정렬한다.
3. 적재 용량이 가장 큰 트럭부터 확인한다.
4. 현재 트럭에 실을 수 있는 컨테이너 중 가장 무거운 컨테이너를 찾는다.
5. 실을 수 있다면 해당 컨테이너의 무게를 result에 더하고,
    그 컨테이너는 이미 운반했으므로 다시 사용하지 않는다.
6. 모든 트럭에 대해 반복한다.
7. 실을 수 있는 컨테이너가 하나도 없다면 result는 그대로 0을 출력한다.
"""

# T = int(input())
# for test_case in range(1, T+1):
#     N, M = map(int, input().split())                   # 3 2      컨테이너 N, M대의 트럭
#     weights = list(map(int, input().split()))          # 1 5 3    각 화물의 무게
#     truck_volume = list(map(int, input().split()))     # 8 3      각 트럭의 적재 용량

#     # 1. 컨테이너의 무게를 큰 순서대로 정렬한다.
#     weights.sort(reverse=True)
#     # 2. 트럭의 적재 용량도 큰 순서대로 정렬한다.
#     truck_volume.sort(reverse=True)

#     # 5-1. 트럭에 실을 컨테이너의 무게 초기값 세팅
#     result = 0
#     # 3. 적재 용량이 가장 큰 트럭부터 확인한다.
#     for volume in truck_volume:
#         # 4. 현재 트럭에 실을 수 있는 컨테이너 중 가장 무거운 컨테이너를 찾는다.
#         for weight in weights:
#             # 5-2. 실을 수 있다면 해당 컨테이너의 무게를 result에 더하고
#             if volume >= weight:
#                 result += weight
#                 # 5-3. 그 컨테이너는 이미 운반했으므로 다시 사용하지 않는다.
#                 weights.remove(weight)
#                 break

#     print(f"#{test_case} {result}")

"""
문제 구상
컨테이너 N개를 M대의 트럭으로 운반 (A > B 편도로 한번 만 운행)
컨테이너의 무게와 트럭의 적재용량이 주어짐
옮겨진 화물의 전체 무게가 얼마인가 구하라
한 개도 옮길 수 없는 경우 0을 출력
<조건>
1. 트럭 당 한 개의 컨테이너를 운반 가능
2. 트럭의 적재용량을 초과하는 컨테이너는 운반 불가


로직 구상
1. 컨테이너의 무게를 큰 순서대로 정렬한다.
2. 트럭의 적재 용량도 큰 순서대로 정렬한다.
3. 적재 용량이 큰 트럭부터 하나씩 확인한다.
4. 각 트럭마다 무거운 컨테이너부터 순서대로 확인한다.
5. 사용하지 않은 트럭이면서 컨테이너의 무게가 적재 용량 이하라면
6. 운반할 수 있다고 보고 무게를 result에 다한다.
7. 사용한 트럭은 다시 사용할 수 없기 때문에 used_truck에 append한다.
"""

T = int(input())
for test_case in range(1, T+1):
    N, M = map(int, input().split())                   # 3 2      컨테이너 N, M대의 트럭
    weights = list(map(int, input().split()))          # 1 5 3    각 화물의 무게
    truck_volume = list(map(int, input().split()))     # 8 3      각 트럭의 적재 용량

    # 1. 컨테이너의 무게를 큰 순서대로 정렬한다.
    weights.sort(reverse=True)
    # 2. 트럭의 적재 용량도 큰 순서대로 정렬한다.
    truck_volume.sort(reverse=True)

    result = 0
    used_truck = []    

    # 3. 적재 용량이 큰 트럭부터 하나씩 확인한다.
    for volume in truck_volume:
        # 4. 각 트럭마다 무거운 컨테이너부터 순서대로 확인한다.
        for i in range(N):
            # 5. 사용하지 않은 트럭이면서 컨테이너의 무게가 적재 용량 이하라면
            if i not in used_truck and weights[i] <= volume:
                # 6. 운반할 수 있다고 보고 무게를 result에 다한다.
                result += weights[i]
                # 7. 사용한 트럭은 다시 사용할 수 없기 때문에 used_truck에 append한다.
                used_truck.append(i)
                break

    print(f"#{test_case} {result}")

