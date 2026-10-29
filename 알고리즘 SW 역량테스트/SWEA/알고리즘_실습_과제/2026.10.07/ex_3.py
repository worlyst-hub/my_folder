arr = [i for i in range(5)]
N, M = map(int, input().split())  # 정점 // 간선 개수
lst = [list(map(int, input().split())) for _ in range(M)]  # 간선 정보를 입력

lst.sort(key=lambda x:x[2])  # 비용을 기준으로 sort

total = 0  # 비용 더하기
count = 0  # 연결된 간선 개수

def findboss(M):
    global arr
    if arr[M] == M:
        return M
    ret = findboss(arr[M])
    arr[M] = ret  # 경로 단축
    return ret

def union(a, b, i):
    global total, count
    fa, fb = findboss(a), findboss(b)  # 보스 찾기
    if fa == fb:  # 이미 같은 그룹을 연결하면 cycle 발생
        return
    total += lst[i][2]  # 연결하면서 비용 더하고
    count += 1  # 연결한 다리 개수 더하고
    arr[fb] = fa  # 연결하기

for i in range(M):
    if count == N - 1:  # 정점의 개수 -1개 만큼 합 구하기
        print(total)  # 합 출력하고 종료
        break
    union(lst[i][0], lst[i][1], i)