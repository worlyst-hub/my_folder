# 문제 10. [서술형] HTTP Request Method (10점)

DRF로 CRUD API를 구현할 때 사용하는 HTTP Request Method 4가지를 쓰고, 각 Method가 어떤 목적으로 사용되는지 작성하시오.

## 답안 작성

- HTTP Request Method는 'GET', 'POST', 'PUT', 'DELETE'가 있고
'GET'은 조회할 때, 'POST'는 생성할 때, 'PUT'은 수정할 때, 'DELETE'는 삭제할 때 사용한다.



---

# 문제 11. [서술형] many=True 옵션 (10점)

Serializer의 many=True 옵션은 어떤 경우에 사용하는지 설명하시오.

## 답안 작성

- 직력화는 기본적으로 단일 객체를 직렬화하도록 되어있는데, 여러 객체를 직렬화하는 경우, many=True를 사용하여 각각 하나씩 불러와 직렬화를 한다.

