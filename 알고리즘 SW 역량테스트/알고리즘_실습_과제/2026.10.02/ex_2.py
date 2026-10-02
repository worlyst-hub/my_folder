### 트리
class Node:
    def __init__(self, value):
        self.value = value  # 인스턴스에 저장될 값
        self.next = None    # 참조하고 있는 객체가 저장
                            # 나 다음에는 너야!! 라는 정보

a = Node(10)
b = Node(20)
c = Node(30)
a.next = b
b.next = c

head = a
while head:
    print(head.value)
    head = head.next

### 이진트리
            #             A
            #           /   \
            #         B       C
            #       /   \   /   \
            #      D     E F     G

# 전위 순회 : 들어가자 마자 출력 ABDECFG
# 중위 순회 : 왼쪽 자식 확인 후 출력 DBEAFCG
# 후위 순회 : 왼쪽, 오른쪽 다 확인 후 출력 DEBFGCA

