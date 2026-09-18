def f(t):
    global cnt
    if t <= N:
        f(t * 2)
        # print(t, end=' ')
        cnt += 1
        tree[t] = cnt
        f(t * 2 + 1)



N = int(input())

tree = [0] * (N + 1)  # 노드번호를 인덱스로 사용해서 저장
cnt = 0
f(1)  # 완전이진트리 루트부터 중위순회
print(tree)