# 통합 RAG 폴더

이 폴더는 팀원 프로젝트의 기존 `rag/` 구조를 유지하면서 다음 기능을 추가한 버전입니다.

- 기존 PDF / Mock RAG 유지
- 기존 `RagRetriever` 인터페이스 유지
- 기존 `ChunkEmbedder` 유지 (`bge-m3` Ollama 우선, 실패 시 hash fallback)
- 국가법령정보 공동활용 API 연동 (`law_api.py`)
- API 법령의 `조 → 항/호/목` 구조를 고려한 Parent-Child 인덱싱 (`indexer.py`)
- `service.py` 없음

## 1. 폴더 교체

기존 프로젝트 최상위의 `rag/` 폴더를 이 폴더로 교체합니다.

기존 프론트엔드 코드는 계속 다음과 같이 사용할 수 있습니다.

```python
from rag.retriever import RagRetriever

retriever = RagRetriever()
matches = retriever.search("해외부동산 취득 신고", top_k=3)
```

## 2. 법령 API Key

프로젝트 최상위 `.env`에 추가합니다.

```env
LAW_API_KEY=""
```

`""` 안에 본인의 국가법령정보 공동활용 OC 값을 넣으면 됩니다.

현재 팀 프로젝트의 `config/settings.py`에는 `LAW_API_KEY` 필드가 없기 때문에,
`law_api.py`가 RAG 폴더만 교체해도 동작하도록 루트 `.env`에서 이 값만 fallback으로 읽습니다.

## 3. 법령 검색 / ID 확인

```python
from rag.law_api import LawAPIClient

client = LawAPIClient()
result = client.search_laws("외국환거래법")
print(result)
```

검색 결과에서 사용할 법령 ID를 확인합니다.

## 4. API 법령 색인

```python
from rag.retriever import RagRetriever

retriever = RagRetriever()
retriever.build_index_from_law_api(
    law_ids=["법령ID1", "법령ID2"],
    force=True,
)
```

처리 흐름은 다음과 같습니다.

```text
국가법령정보 API
  → 본문 정규화
  → 조문 Parent 파싱
  → 항/호/목 중심 Child 청킹
  → 기존 ChunkEmbedder
  → 기존 ChromaDB
```

검색 시에는 작은 Child를 기준으로 유사 문서를 찾고, 최종 반환은 해당 Child가 속한
Parent 조문 전체를 사용합니다.

## 5. 기존 PDF / Mock 모드

기존 방식은 그대로입니다.

```python
retriever = RagRetriever()
retriever.build_index(force=True)
```

`.env`의 `RAG_MODE=mock`이면 샘플 규정, `RAG_MODE=pdf`이면 기존
`data/regulations/` PDF를 사용합니다.

> API 색인은 `RAG_MODE`와 별개로 `build_index_from_law_api()`를 명시적으로 호출합니다.
