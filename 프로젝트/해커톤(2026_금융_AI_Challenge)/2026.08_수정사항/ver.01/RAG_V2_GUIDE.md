# RAG V2 이해 및 적용 가이드

## 1. 이번 파일의 위치와 목적

`rag_v2.py`는 기존 `rag.py`를 수정하지 않고 새로 작성한 파일입니다. 기존 프로젝트의 코드 양식과 `RegulationRAG`, `load_documents()`, `search()` 이름을 최대한 유지했습니다.

현재 단계에서는 `app` 폴더에 복사한 뒤 파일명을 그대로 사용할 수 있습니다. 기존 `main.py`에서 시험하려면 import만 다음처럼 바꾸면 되지만, 이번 산출물은 원본 프로젝트를 직접 수정하지 않았습니다.

```python
from rag_v2 import RegulationRAG
```

## 2. 책임 분리

`rag_v2.py`가 담당하는 기능은 다음과 같습니다.

- 테스트 TXT 또는 정규화된 법령 레코드 입력
- 조 단위 Parent 생성
- 항·호·목 중심 Child 생성
- 무료 로컬 임베딩 생성
- ChromaDB 저장
- Child 검색 후 Parent 조문 반환

다음 기능은 의도적으로 넣지 않았습니다.

- `.env` 로딩과 국가법령정보 API 호출
- OCR
- 신고 대상 또는 필요 서류 최종 판정
- Ollama와 최종 답변 생성

API 수집 파일은 API 응답을 아래 형태로 바꿔 `load_records()`에 전달하면 됩니다.

```python
records = [
    {
        "text": "법령 원문",
        "source": "API 문서 ID",
        "law_name": "외국환거래법",
        "document_type": "law",
        "promulgation_number": "법률 제00000호",
        "effective_date": "2026-01-01",
        "revision_date": "2025-12-01",
        "source_url": "원문 URL"
    }
]

rag.load_records(records)
```

## 3. 새 import의 역할

### `re`

장·절·조·항·호·목 형태를 찾습니다. 법령의 구조를 먼저 보존하고 길이 기준 청킹은 필요한 경우에만 적용하기 위해 필요합니다.

### `json`

조 전체 Parent를 별도 JSON 파일에 저장합니다. 긴 Parent를 모든 Child metadata에 반복 저장하지 않으므로 DB 중복을 줄일 수 있습니다.

### `hashlib`

출처·조문·내용으로부터 안정적인 ID를 만듭니다. 같은 문서를 다시 적재하면 같은 ID가 나오기 때문에 `upsert`가 가능해집니다.

### `SentenceTransformer`

`intfloat/multilingual-e5-base` 모델을 로컬에서 실행하여 한국어 법령과 질문을 벡터로 바꿉니다. 유료 임베딩 API를 사용하지 않습니다. 최초 실행에서는 모델을 다운로드하기 위한 인터넷 연결과 저장 공간이 필요하고, 그 이후에는 내려받은 모델을 로컬에서 사용할 수 있습니다.

## 4. 임베딩 모델을 명시한 이유

기존 코드는 ChromaDB의 기본 임베딩을 암묵적으로 사용했습니다. 새 코드는 다음 모델을 명시합니다.

```python
embedding_model_name="intfloat/multilingual-e5-base"
```

선택 이유는 다음과 같습니다.

- 한국어를 포함한 다국어 검색 모델입니다.
- 로컬 실행이 가능하여 호출당 API 비용이 없습니다.
- 모델과 코드의 라이선스를 확인해 프로젝트에서 관리할 수 있습니다.
- 문서에는 `passage:`, 질문에는 `query:` 접두사를 사용하는 검색 전용 학습 방식을 지원합니다.

이 선택이 최종 정답이라는 의미는 아닙니다. 실제 외환 법령 질문과 정답 조문으로 평가셋을 만든 뒤 다른 무료 모델과 Recall@k를 비교해야 합니다.

## 5. Child 상한을 450토큰으로 바꾼 이유

처음 제안한 Child 300~600토큰은 일반적인 시작 범위로는 괜찮습니다. 하지만 `multilingual-e5-base`는 긴 입력을 최대 약 512토큰에서 잘라냅니다. 600토큰 Child를 넣으면 뒤쪽 법령 내용이 임베딩에 반영되지 않을 수 있습니다.

따라서 새 기본값은 다음과 같습니다.

```python
child_min_tokens=250
child_max_tokens=450
child_overlap_tokens=80
```

450토큰은 `query:` 또는 `passage:` 접두사, 법령명·조문 문맥과 특수 토큰을 위한 여유를 둔 값입니다. 최소 250토큰은 강제값이 아니라 가능한 경우에 맞추는 목표입니다. 짧은 항을 억지로 다음 조문과 합치지 않기 위해 구조 경계를 더 우선합니다.

## 6. Parent-Child 청킹 흐름

```text
법령 원문
  ↓
장·절 정보 추적
  ↓
조 전체를 Parent로 생성
  ↓
항·호·목 줄을 구조 단위로 구분
  ↓
서로 인접한 짧은 구조 단위를 450토큰 안에서 결합
  ↓
너무 긴 단위만 문단→줄→문장→공백 순으로 재귀 분할
  ↓
끝까지 나눌 수 없는 긴 문장만 80토큰 overlap 적용
```

Parent는 하나의 조 전체를 보존합니다. 1,800토큰은 강제 분할선이 아니라 긴 Parent를 표시하는 기준입니다. 검색 임베딩은 최대 450토큰 Child에만 만들기 때문에 Parent가 1,800토큰보다 길어도 임베딩 모델에서 잘리지 않습니다.

검색할 때는 가장 가까운 Child 후보를 찾은 다음 `parent_id`로 조 전체를 복원합니다. 같은 조의 여러 Child가 검색되어도 Parent 하나로 중복 제거합니다.

## 7. TXT와 API의 연결

`load_documents()`는 기존 프로젝트와의 호환 및 테스트를 위해 남겨두었습니다.

```python
rag = RegulationRAG()
rag.load_documents()
```

나중에 국가법령정보 API를 연결할 때는 RAG 파일 안에서 API를 호출하지 않습니다. 새로운 API 수집 파일에서 `.env`를 읽고 XML 또는 JSON을 정규화한 뒤 다음처럼 전달합니다.

```python
rag = RegulationRAG()
rag.load_records(normalized_records)
```

이렇게 분리하면 API 주소나 인증 방식이 바뀌어도 청킹과 검색 코드를 함께 수정할 필요가 없습니다.

## 8. 검색 반환 형식

기존 `report.py`와의 호환을 위해 다음 필드를 그대로 제공합니다.

- `source`
- `chunk`
- `content`

`content`에는 일치한 Child만이 아니라 연결된 Parent 조문 전체가 들어갑니다. 추가로 근거 추적을 위한 다음 필드도 반환합니다.

- `parent_id`
- `article`, `article_title`
- `effective_date`, `source_url`
- `matched_child`
- `distance`

`distance`는 ChromaDB의 cosine distance이므로 일반적으로 작을수록 질문과 가깝습니다. 고정된 합격 기준을 바로 만들기보다 평가셋의 정답·오답 분포를 확인한 뒤 기준을 정해야 합니다.

## 9. 설치와 첫 실행

새로운 가상환경에서 다음 명령을 실행합니다.

```bash
pip install -r requirements_rag_v2.txt
```

최초 `RegulationRAG()` 생성 시 임베딩 모델 다운로드 때문에 시간이 걸릴 수 있습니다. 개발 환경에서 미리 한 번 다운로드하면 이후 실행은 로컬 캐시를 사용합니다.

## 10. 기존 DB와 분리한 이유

기존 ChromaDB는 기본 임베딩 모델로 만들어졌을 가능성이 큽니다. 서로 다른 모델의 벡터는 차원이나 의미 공간이 다르므로 한 collection에 섞으면 안 됩니다.

새 기본 이름은 다음과 같습니다.

```python
collection_name="financial_regulations_v2"
```

따라서 기존 `financial_regulations` collection을 삭제하지 않고 나란히 시험할 수 있습니다.

## 11. 아직 구현하지 않은 개선

이번 버전은 한 단계씩 이해하기 위해 계층적 dense retrieval에 집중했습니다. 다음 단계 후보는 다음과 같습니다.

1. 국가법령정보 API 수집·정규화 파일
2. 법령 시행일을 거래일과 비교하는 버전 필터
3. BM25 키워드 검색과 벡터 검색을 결합한 하이브리드 검색
4. 무료 로컬 reranker를 이용한 후보 재정렬
5. 실제 조문 정답 평가셋과 Recall@k 평가 스크립트
6. OCR 결과 정규화 및 신뢰도 metadata 연결

이 기능들을 한꺼번에 넣기보다 평가셋을 만든 뒤 한 기능씩 추가하고 정확도 변화를 측정하는 편이 원인을 이해하고 발표하기 쉽습니다.

## 12. 주의점

- 법령 TXT의 줄바꿈이 조·항·호 구조를 보존할수록 파싱 정확도가 좋아집니다.
- 국가법령정보 API XML/JSON의 구조 필드를 사용할 수 있다면 정규표현식보다 그 구조 필드를 우선해야 합니다.
- Parent JSON과 ChromaDB는 같은 `chroma_db` 폴더에서 함께 관리해야 합니다.
- 임베딩 모델을 바꾸면 새 collection 이름을 사용하고 전체 문서를 다시 인덱싱해야 합니다.
- 최종 신고·서류 판정은 검색 결과만으로 확정하지 말고 근거 조문과 시행일 검증 단계를 거쳐야 합니다.

## 참고한 공식 문서

- ChromaDB Embedding Functions: https://docs.trychroma.com/docs/embeddings/embedding-functions
- ChromaDB Collection Query: https://docs.trychroma.com/reference/python/collection
- Sentence Transformers Usage: https://sbert.net/docs/sentence_transformer/usage/usage.html
- multilingual-e5-base Model Card: https://huggingface.co/intfloat/multilingual-e5-base
