# `rag_v2_ordered.py` 코드 순서 안내

이 파일은 첨부한 `rag_v2.py`의 실행 기능을 바꾸지 않고, 사람이 데이터 흐름을 따라 읽기 쉽도록 메서드 위치와 구역 제목만 정리한 버전입니다.

## 코드 배치 순서

```text
초기 설정
   ↓
0. 입력 준비
   ↓
1. 파싱
   ↓
2. 청킹
   ↓
3. 임베딩
   ↓
4. 벡터 DB 저장
   ↓
5. 검색
```

### 초기 설정

`__init__()`에서 프로젝트 경로, 청킹 크기, 임베딩 모델, ChromaDB와 Parent 저장소를 준비합니다. 이는 데이터 인젝션을 실행하는 단계가 아니라 각 단계가 사용할 도구와 설정을 준비하는 부분입니다.

### 0. 입력 준비

`_read_text_file()`과 `load_documents()`가 테스트용 TXT를 읽습니다. 향후 국가법령정보 API 데이터는 별도 API 파일에서 정규화한 뒤 `load_records()`로 전달합니다.

### 1. 파싱

`_create_legal_parent()`, `_create_generic_parents()`, `_build_parents()`가 원문에서 장·절·조 구조를 찾고 조 전체를 Parent로 만듭니다.

### 2. 청킹

`_token_window_split()`, `_recursive_split()`, `_build_children()`가 Parent 안의 항·호·목을 검색용 Child로 나눕니다. 구조 단위가 지나치게 긴 경우에만 재귀 분할과 overlap을 사용합니다.

### 3. 임베딩

`_embed_documents()`는 Child에 `passage:`를 붙여 벡터로 만들고, `_embed_query()`는 검색 질문에 `query:`를 붙여 벡터로 만듭니다.

### 4. 벡터 DB 저장

Parent 저장소 함수와 `load_records()`가 다음 순서로 실제 데이터 인젝션을 실행합니다.

```text
레코드 정규화
→ Parent 파싱
→ Child 청킹
→ Child 임베딩
→ ChromaDB upsert
→ Parent JSON 저장
```

`load_records()` 내부에도 각 처리 단계 바로 위에 번호와 설명 주석을 추가했습니다.

### 5. 검색

`search()`가 질문을 임베딩하고 가까운 Child를 찾은 뒤 `parent_id`를 이용해 조 전체 Parent를 반환합니다.

## 기능이 바뀌지 않은 이유

Python 클래스에서는 메서드가 파일 안에서 어느 순서로 정의되었는지와 관계없이 `self.메서드명()`으로 호출할 수 있습니다. 따라서 이번 변경은 메서드 배치와 설명 주석만 바꾸며, 함수 내부 실행 코드와 반환 형식은 유지합니다.

원본 `C:/Users/82104/Desktop/해커톤/rag_v2.py`는 수정하지 않았습니다.
