# 외국환거래 필요서류 RAG 프로젝트 통합 정리

- 작성일: 2026-09-03
- 최종 기능 기준: 국가법령정보 공동활용 API 기반 RAG V6
- 최종 배포 통합본: `foreign-exchange-ai-for-regtech-deploy-rag-api-v7.zip`
- 배포 구조: Netlify 정적 프런트엔드 + Render FastAPI 백엔드

## 1. 문서 목적

이 문서는 프로젝트 진행 중 요청된 요구사항, 버전별 수정 내용, 최종 구조, 로컬 실행 방법, Render·Netlify 배포 방법 및 현재 한계를 한곳에 정리한다.

핵심 목표는 특정 테스트 사례인 해외 법인 설립에만 맞춘 프로그램이 아니라, 해외부동산 취득·해외증권 투자·차입·대여·상환·청산·회수 등 다양한 외국환거래에서 거래 당사자가 제출해야 하는 서류와 근거 조문을 범용적으로 검색하는 것이다.

## 2. 최초 문제와 핵심 요구사항

### 2.1 최초 문제

초기 프로그램은 법령 PDF를 고정 길이로 나누고 질문과 가까운 Chunk를 반환했다. `신고`, `제출`, `서류` 같은 표현이 여러 조문에 반복되면서 다음 문제가 발생했다.

- 질문과 유사도가 비슷한 Child가 지나치게 많이 검색됨
- 거래 당사자 제출 의무와 기관의 보고 의무가 섞임
- 제출서류 목록이 여러 Child에 걸리면 일부만 표시됨
- 해외직접투자 질의에 역외금융회사·사후관리 등 특수 조문이 함께 표시됨
- 왼쪽 필요서류는 CSV, 오른쪽 관련 법령은 RAG를 사용해 서로 연결되지 않음
- 지급절차 근거조문도 유사도 검색에 의존해 관련 없는 조문이 표시됨

### 2.2 요청된 원칙

- Streamlit과 배포 프런트엔드의 화면 구성과 사용자 동선은 최대한 유지한다.
- 제9-5조나 해외직접투자 전용 `if`문을 하드코딩하지 않는다.
- 사유코드의 이름·분류·설명·키워드와 실제 거래목적을 검색에 활용한다.
- 거래 단계가 청산·회수라면 해당 표현을 감점하지 않고 거래문맥과 일치하는지 판단한다.
- 거래 당사자의 제출 의무와 금융기관·공공기관의 보고 의무를 구분한다.
- 검색된 Child가 제출서류 목록의 시작이면 같은 Parent의 연결된 Sibling까지 확장한다.
- 법령에서 추출한 제출서류를 체크리스트의 우선 데이터로 사용한다.
- 법령 추출 실패 시 기존 CSV 필요서류를 테스트용 Fallback으로 유지한다.
- PDF 기반 구조를 먼저 검증한 뒤 국가법령정보 공동활용 API로 입력원을 전환한다.
- 최종적으로 모든 외국환거래 사유코드에 동일한 범용 Retrieval 흐름을 적용한다.
- `.env` 전체를 교체하지 않고 필요한 API 설정만 추가할 수 있게 한다.
- 실제 `.env`, API 키, 로컬 DB 및 캐시는 배포 ZIP에 포함하지 않는다.

## 3. 전체 수정 과정: 6단계

## 3.1 1단계 — Mock V1: Parent–Child 계층 청킹

### 목표

페이지별 고정 길이 Chunk 대신 법령의 조문 구조를 보존한다.

### 주요 수정

- 법령의 `조 → 항 → 호 → 목` 구조를 파싱한다.
- 조문 전체를 Parent로, 검색 가능한 작은 단위를 Child로 저장한다.
- 긴 구조만 문단·줄·문장 순으로 재귀 분할한다.
- Child만 임베딩하고 Parent는 별도 JSON에 한 번 저장한다.
- 검색 결과는 Parent 전체가 아니라 관련 Child 중심으로 반환한다.

### 주요 파일

- `rag/chunker.py`
- `rag/retriever.py`
- `tests/test_rag.py`

### 결과

조문 구조와 페이지를 넘어가는 문맥을 보존하는 기반을 만들었다. 다만 검색 순위는 여전히 일반 유사도 중심이었고 필요서류 전용 판단은 부족했다.

## 3.2 2단계 — Retrieval Fix: 제출서류 Child 우선 검색

### 목표

해외직접투자 질의에서 단순 주제 유사 조문보다 실제 제출 의무와 서류 목록이 있는 조문을 우선한다.

### 주요 수정

- `신고서`, `신청서`, `첨부`, `제출`, `별지`, `다음 각 호의 서류` 표현에 가중치를 부여한다.
- 필요서류 검색일 때만 전용 검색 의도를 사용한다.
- 후보를 넓게 검색한 뒤 제출서류 관련성을 기준으로 재정렬한다.
- 일반 법령 검색과 지급절차 검색에는 기존 동작을 유지한다.

### 주요 파일

- `frontend/regulation.py`
- `rag/retriever.py`
- `RAG_REQUIRED_DOCUMENT_RETRIEVAL_FIX.md`

### 결과

해외직접투자 법인설립에서 제9-5조가 우선될 가능성이 높아졌다. 다만 사후관리·청산 표현을 일괄 감점하는 초기 규칙은 다른 거래유형으로 확장하기에 부족했다.

## 3.3 3단계 — PDF V3: 거래유형 범용화와 필요서류 추출

### 목표

법인설립뿐 아니라 해외부동산·증권·차입·대여·상환·청산·회수 등 다양한 거래에 하나의 검색 로직을 적용한다.

### 주요 수정

- 사유코드 `name`, `category`, `description`, `keywords`와 LLM·OCR 거래목적을 합쳐 동적 Query를 만든다.
- 현재 거래 행위와 후보 조문의 취득·처분·설립·회수·청산 단계가 일치하는지 평가한다.
- 거래 당사자 주체는 가점하고 기관장·은행장 자체 보고 의무는 감점한다.
- 해외 거래에 국내 부동산 조문이 섞이는 등의 방향성 오탐을 줄인다.
- 필요서류 Anchor가 있는 Child를 찾은 뒤 연결된 Sibling만 확장한다.
- 첫 번째 핵심 제출 조문에서 신고서와 번호형 첨부서류를 추출한다.
- 왼쪽 체크리스트를 법령 RAG 결과와 연결하고 실패 시 CSV로 Fallback한다.

### 주요 파일

- `frontend/regulation.py`
- `rag/retriever.py`
- `services/reason_code/mapper.py`
- `schemas/analysis.py`
- `tests/test_rag.py`
- `tests/test_reason_code.py`

### 결과

PDF 입력을 유지하면서 검색·검증·확장·서류 추출 흐름을 범용화했다. UI는 유지되고 체크박스의 데이터 출처만 법령 우선 방식으로 바뀌었다.

## 3.4 4단계 — API V4: 국가법령정보 API 전환

### 목표

PDF 대신 국가법령정보 공동활용 API에서 최신 법령을 받아 기존 범용 Retrieval 로직에 연결한다.

### 주요 수정

- `RAG_MODE=api`를 추가한다.
- 외국환거래법·시행령·외국환거래규정과 참조 서식을 API로 동기화한다.
- API 응답을 로컬 Last-good Snapshot에 저장하고 매 검색마다 재호출하지 않는다.
- 외국환거래규정 조문만 필요서류 Semantic 검색 후보로 사용한다.
- 상위법과 시행령은 정확한 근거 확인용으로 분리한다.
- 별표·별지·서식은 Semantic 검색에서 제외하고 참조번호 Exact Lookup 저장소로 분리한다.
- Parent 원문으로 적용대상·거래 주체·행위·방향성을 재검증한다.
- 지급절차는 이미 알고 있는 조문번호를 유사도 검색하지 않고 Exact Lookup한다.
- 추출 결과 상태를 `COMPLETE`, `PARTIAL`, `AMBIGUOUS`, `FAILED`로 구조화한다.
- `기타 신고기관의 장이 필요하다고 인정하는 서류`는 `(요구 시)` 조건부로 표시한다.

### 주요 파일

- 신규 `rag/law_api.py`
- `config/settings.py`
- `.env.example`
- `.gitignore`
- `rag/retriever.py`
- `services/payment_procedure.py`
- `services/reason_code/mapper.py`
- `schemas/analysis.py`
- `tests/test_law_api.py`

### 결과

입력원이 PDF에서 API Snapshot으로 바뀌었지만 Query·Reranking·Parent 검증·Sibling 확장·서류 추출 구조는 재사용됐다. API 신청 범위가 넓어도 모든 문서를 유사도 후보로 넣지 않아 과도한 검색을 방지했다.

## 3.5 5단계 — API V5: 실제 행정규칙 JSON 파싱 수정

### 목표

국가법령정보 API가 외국환거래규정 전체 본문을 줄바꿈 없는 긴 문자열로 반환하는 실제 형식에 대응한다.

### 주요 수정

- 전체 규정이 하나의 제1-1조 Parent로 저장되던 문제를 수정한다.
- 줄바꿈이 없어도 `제9-5조(해외직접투자의 신고 등)` 형태를 조문 Heading으로 분리한다.
- 본문 안에서 인용된 다른 조문번호를 새로운 Heading으로 오인하지 않는다.
- 항·호·목 경계를 복원해 기존 Parent–Child Chunker를 재사용한다.
- 삭제된 빈 호 번호가 앞 문서명에 붙는 현상을 줄인다.
- 검색 실패 안내가 실제 `RAG_MODE`를 표시하도록 수정한다.
- 파싱 방식 변경에 맞춰 Snapshot과 Chroma 인덱스 버전을 분리한다.

### 주요 파일

- `rag/law_api.py`
- `rag/retriever.py`
- `frontend/regulation.py`
- `tests/test_law_api.py`

### 결과

실제 API 응답에서 외국환거래법 43개, 시행령 71개, 외국환거래규정 206개 조문으로 분리되는 것을 검증했다. 법인설립 질의에서는 제9-5조와 필수서류 4건, 조건부 서류 1건을 추출했다.

## 3.6 6단계 — API V6: 삭제 항목과 법령 번호 표시 보존

### 목표

법령 원문의 삭제된 항·호가 빈 번호로 보이거나 다음 유효 항목과 붙어 보이는 문제를 해결한다.

### 주요 수정

- API 원문의 `<삭제>`와 `<삭 제>`를 제거하지 않고 `삭제`로 보존한다.
- 삭제된 호를 `2. 삭제`, `3. 삭제`처럼 표시한다.
- 삭제된 항을 `④ 삭제`, `⑥ 삭제`처럼 표시한다.
- 유효한 제5항이 앞 제출서류 목록에 붙지 않도록 구조 경계를 보존한다.
- Streamlit Markdown이 번호를 임의로 연속 재정렬하지 않도록 표시 문자열을 보정한다.
- 삭제 항목은 오른쪽 법령 원문에만 표시하고 필요서류 체크리스트에는 포함하지 않는다.
- 거래문맥과 RAG 인덱스 버전을 화면 캐시 키에 포함한다.

### 주요 파일

- `rag/law_api.py`
- `rag/retriever.py`
- `frontend/regulation.py`
- `tests/test_law_api.py`
- `tests/test_regulation_display.py`

### 결과

제9-5조의 삭제된 항·호와 유효한 항목이 원문 구조에 맞게 구분되어 표시된다. UI 배치와 사용자 동선은 변경하지 않았다.

## 4. 최종 배포 V7 통합

V7은 새로운 RAG 알고리즘 단계가 아니라, API V6 기능을 팀원의 Netlify·Render 배포 구조에 연결한 통합본이다.

### 4.1 비교 결과

팀원의 배포 ZIP은 기존 Streamlit 코드와 핵심 기능이 같고 다음 배포 파일이 추가된 형태였다.

- `render_api.py`
- `render.yaml`
- `requirements-render.txt`
- `.env.render.example`
- `netlify/index.html`
- `netlify/config.js`
- `netlify/js/api.js`
- `netlify/js/app.js`
- `netlify/css/style.css`
- Netlify 폰트와 헤더·리다이렉트 설정

따라서 팀원의 배포 UI와 배포 구조를 기준으로 유지하면서 V6 백엔드 RAG를 이식했다.

### 4.2 배포 API 수정

`render_api.py`의 법령 검색 엔드포인트를 다음 흐름으로 변경했다.

```text
사유코드 + 키워드 + LLM 분석 + OCR 거래목적
→ 범용 필요서류 Query
→ search_intent=required_documents
→ V6 Reranking·Parent 검증·Sibling 확장
→ 법령 필요서류 추출
→ Netlify UI 응답
```

지급절차는 판정 결과의 `citation_articles`를 이용해 정확한 조문 원문을 조회하도록 연결했다.

### 4.3 Netlify 프런트엔드 수정

- 법령에서 추출한 필요서류와 출처 안내를 표시한다.
- 관련 법령과 지급절차 정확 근거조문을 펼침 영역으로 표시한다.
- 법령 원문의 줄바꿈과 번호를 보존한다.
- 조건부 서류는 체크하지 않아도 다음 단계 진행을 막지 않는다.
- 최종 요약의 미확인 경고는 필수서류만 대상으로 한다.

### 4.4 배포 설정 수정

- `requirements-render.txt`에 `requests`를 추가했다.
- `render.yaml`의 RAG 기본값을 `api`로 변경했다.
- `LAW_API_KEY`, API 주소, Timeout, 캐시, 갱신주기, 서식 포함 설정을 추가했다.
- 실제 Secret은 코드나 ZIP에 포함하지 않았다.

### 4.5 검증 결과

- Python 문법 검사 통과
- Netlify JavaScript 문법 검사 통과
- 전체 테스트 `69 passed`
- ZIP 내부 필수 파일 검증 통과
- 실제 `.env`, API 키, DB, Chroma 캐시, 법령 API 캐시, Python 캐시 제외 확인

## 5. 최종 시스템 구조

```text
사용자 브라우저
  ↓
Netlify 정적 프런트엔드
  ↓ REST API
Render FastAPI 백엔드
  ├─ OCR Service: Mock 또는 Ollama Vision
  ├─ LLM Service: Mock 또는 Ollama
  ├─ Reason Code Mapper
  ├─ Payment Procedure Evaluator
  └─ RAG Retriever
       ├─ 국가법령정보 API Snapshot
       ├─ Parent–Child Chunker
       ├─ ChromaDB Child Index
       ├─ Parent 검증·Sibling 확장
       └─ 필요서류 추출·CSV Fallback
```

## 6. 실행 모드

| 기능 | 개발용 | 실제 기능 |
|---|---|---|
| LLM | `LLM_MODE=mock` | `LLM_MODE=live` |
| OCR | `OCR_MODE=mock` | `OCR_MODE=vision` |
| RAG | `RAG_MODE=mock` 또는 `pdf` | `RAG_MODE=api` |

세 모드는 독립적으로 설정할 수 있다. 예를 들어 OCR은 Mock, LLM은 Live, RAG는 API로 실행할 수 있다.

## 7. 로컬에서 실제 배포 구조로 실행

로컬에서도 Streamlit이 아니라 Netlify 역할의 정적 UI와 Render 역할의 FastAPI를 각각 실행한다.

### 7.1 준비사항

- Python 3.11 권장
- 국가법령정보 공동활용 API `OC` 값
- 실제 OCR을 사용할 경우 로컬 Ollama와 `qwen2.5vl`
- 실제 한국어 임베딩을 사용할 경우 로컬 Ollama와 `bge-m3`
- 실제 LLM을 사용할 경우 Ollama Cloud API Key 또는 로컬 LLM

로컬 Ollama 모델을 준비한다.

```powershell
ollama pull qwen2.5vl
ollama pull bge-m3
```

LLM도 로컬로 실행하려면 다음을 추가한다.

```powershell
ollama pull llama3.1
```

### 7.2 프로젝트와 가상환경

```powershell
cd "C:\Users\SSAFY\Desktop\foreign-exchange-ai-for-regtech-deploy-rag-api-v7"
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements-render.txt
.\.venv\Scripts\python.exe -m database.seed
```

### 7.3 `.env` 생성

```powershell
Copy-Item .env.example .env
notepad .env
```

권장 로컬 전체 기능 설정은 다음과 같다. LLM은 Ollama Cloud, OCR과 임베딩은 로컬 Ollama를 사용한다.

```dotenv
LLM_MODE=live
OCR_MODE=vision
RAG_MODE=api
LOG_LEVEL=INFO

FRONTEND_ORIGINS=http://localhost:5500

OLLAMA_BASE_URL=https://ollama.com
OLLAMA_MODEL=gpt-oss:120b-cloud
OLLAMA_TIMEOUT=120
OLLAMA_API_KEY=본인의_Ollama_Cloud_API_Key

OLLAMA_VISION_MODEL=qwen2.5vl
OLLAMA_VISION_BASE_URL=http://localhost:11434
OLLAMA_VISION_API_KEY=

OLLAMA_EMBED_MODEL=bge-m3
OLLAMA_EMBED_BASE_URL=http://localhost:11434
OLLAMA_EMBED_API_KEY=

LAW_API_KEY=국가법령정보_OC값
LAW_API_BASE_URL=https://www.law.go.kr/DRF
LAW_API_TIMEOUT=30
LAW_API_CACHE_DIR=./data/law_api_cache
LAW_API_REFRESH_HOURS=24
LAW_API_INCLUDE_APPENDICES=true

DATABASE_URL=sqlite:///./data/fx_remittance.db
CHROMA_PERSIST_DIR=./data/chroma
REGULATION_PDF_DIR=./data/regulations
```

Ollama Cloud 없이 LLM도 로컬로 실행하려면 다음처럼 변경한다.

```dotenv
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1
OLLAMA_API_KEY=
```

### 7.4 첫 번째 PowerShell: FastAPI 백엔드

```powershell
.\.venv\Scripts\python.exe -m uvicorn render_api:app --host 127.0.0.1 --port 8000 --reload
```

다음 주소를 확인한다.

- `http://127.0.0.1:8000/api/health`
- `http://127.0.0.1:8000/api/config`
- `http://127.0.0.1:8000/docs`

`Application startup complete`가 표시되면 이 창은 백엔드가 점유하고 있으므로 명령을 더 입력하지 않는다.

### 7.5 두 번째 PowerShell: Netlify 프런트엔드

먼저 `netlify/config.js`를 연다.

```powershell
cd "C:\Users\SSAFY\Desktop\foreign-exchange-ai-for-regtech-deploy-rag-api-v7"
notepad netlify\config.js
```

로컬 API 주소로 변경하고 저장한다.

```javascript
window.FIXAR_API_BASE = "http://127.0.0.1:8000";
```

같은 두 번째 PowerShell에서 정적 서버를 실행한다.

```powershell
.\.venv\Scripts\python.exe -m http.server 5500 --directory netlify
```

브라우저에서 다음으로 접속한다.

```text
http://localhost:5500
```

### 7.6 로컬 기능 검증

#### OCR

- 실제 JPG·PNG·PDF를 업로드한다.
- 서로 다른 신청서가 서로 다른 결과를 반환하는지 확인한다.
- 이름·금액·국가·SWIFT·송금목적을 원본과 대조한다.
- PDF는 현재 첫 페이지만 OCR한다.
- Vision 첫 호출은 모델 상태에 따라 오래 걸릴 수 있다.

#### LLM

다음처럼 서로 다른 목적을 입력해 결과가 달라지는지 확인한다.

```text
베트남 현지 법인을 설립하기 위한 자본금 송금
미국 주택 매입 계약금 지급
해외직접투자 법인 청산대금 회수
```

거래 유형·행위·성격·정규화 목적과 사유코드 후보가 입력에 맞게 달라져야 한다.

#### RAG

- 법인설립에서는 제9-5조와 제출서류가 우선되는지 확인한다.
- 해외부동산 질의에서 제9-5조가 고정 반환되지 않는지 확인한다.
- 청산·회수 질의에서 해당 단계 조문이 감점되지 않는지 확인한다.
- 출처가 `국가법령정보API_...json`인지 확인한다.
- 거래 당사자 제출 의무와 기관 보고 의무가 분리되는지 확인한다.
- `data/law_api_cache`와 `data/chroma`가 생성되는지 확인한다.
- API 응답의 `embedding_backend`가 Hash Fallback인지 실제 Ollama인지 확인한다.

#### 프런트엔드 전체 흐름

```text
신청서 업로드
→ OCR 결과 확인·수정
→ 거래 문맥 분석
→ 사유코드 확인
→ 지급절차 판정
→ 필요서류·관련 법령 확인
→ SWIFT 조회
→ 최종 처리 요약
```

브라우저 개발자 도구의 Network에서 주요 API가 `200`인지 확인한다.

### 7.7 파일 업로드가 작동하지 않을 때

1. `http://127.0.0.1:8000/api/health`가 `{"status":"ok"}`를 반환하는지 확인한다.
2. `http://localhost:5500/config.js`에 로컬 API 주소가 표시되는지 확인한다.
3. 브라우저에서 `Ctrl+F5`로 강력 새로고침한다.
4. 업로드 파일이 PDF·JPG·JPEG·PNG이고 20MB 이하인지 확인한다.
5. F12 Console에서 JavaScript 오류를 확인한다.
6. 프런트엔드 PowerShell에서 `/config.js`, `/js/app.js`, `/js/api.js` 요청이 `200`인지 확인한다.
7. 백엔드 PowerShell에서 `/api/config`, `/api/countries`, `/api/ocr` 요청이 들어오는지 확인한다.

## 8. Render·Netlify 배포

## 8.1 Git 업로드

ZIP 자체가 아니라 압축을 푼 프로젝트 파일을 Git 저장소에 올린다. 다음은 커밋하지 않는다.

```text
.env
.venv/
data/fx_remittance.db
data/chroma/
data/law_api_cache/
data/uploads/
__pycache__/
```

## 8.2 Render 백엔드 배포

`render.yaml`을 이용해 Blueprint를 만들거나 다음 명령을 직접 설정한다.

```text
Build Command:
pip install -r requirements-render.txt && python -m database.seed

Start Command:
uvicorn render_api:app --host 0.0.0.0 --port $PORT

Health Check Path:
/api/health
```

RAG 필수 환경변수:

```dotenv
RAG_MODE=api
LAW_API_KEY=국가법령정보_OC값
LAW_API_BASE_URL=https://www.law.go.kr/DRF
LAW_API_TIMEOUT=30
LAW_API_CACHE_DIR=./data/law_api_cache
LAW_API_REFRESH_HOURS=24
LAW_API_INCLUDE_APPENDICES=true
```

실제 LLM을 사용할 경우:

```dotenv
LLM_MODE=live
OLLAMA_BASE_URL=https://ollama.com
OLLAMA_MODEL=gpt-oss:120b-cloud
OLLAMA_TIMEOUT=120
OLLAMA_API_KEY=본인의_Ollama_Cloud_API_Key
```

배포 후 확인한다.

- `https://RENDER-SERVICE.onrender.com/api/health`
- `https://RENDER-SERVICE.onrender.com/api/config`

## 8.3 Netlify 프런트엔드 배포

`netlify/config.js`를 실제 Render 주소로 변경한다.

```javascript
window.FIXAR_API_BASE = "https://RENDER-SERVICE.onrender.com";
```

Netlify 설정:

```text
Base directory: 비워둠
Build command: 비워둠
Publish directory: netlify
```

## 8.4 CORS 연결

Netlify 주소가 확정되면 Render의 환경변수에 등록하고 서비스를 다시 시작한다.

```dotenv
FRONTEND_ORIGINS=https://NETLIFY-SITE.netlify.app
```

끝의 `/`는 제외한다.

## 8.5 배포 검증

- Netlify 화면이 정상적으로 로드되는지 확인한다.
- 브라우저 Console에 CORS 오류가 없는지 확인한다.
- Network에서 각 API 응답이 `200`인지 확인한다.
- `/api/config`의 모드가 의도한 설정인지 확인한다.
- LLM 입력에 따라 분석 결과가 달라지는지 확인한다.
- RAG 출처가 국가법령정보 API JSON인지 확인한다.
- 서로 다른 거래유형에서 서로 다른 조문·서류가 검색되는지 확인한다.
- 지급절차 근거조문이 판정에 사용된 조문과 일치하는지 확인한다.

## 9. 로컬과 배포환경의 차이

현재 배포 기본값은 다음과 같다.

```dotenv
LLM_MODE=mock
OCR_MODE=mock
RAG_MODE=api
```

따라서 별도 인프라 없이 배포하면 프런트엔드와 법령 API RAG는 실제로 동작하지만 LLM과 OCR은 Mock이다.

### 9.1 실제 LLM

Render에서 Ollama Cloud 접속정보를 설정하면 `LLM_MODE=live`로 사용할 수 있다.

### 9.2 실제 OCR

`qwen2.5vl` 기본 주소는 `http://localhost:11434`다. Render 서버에는 현재 Ollama Vision이 설치되어 있지 않으므로 단순히 `OCR_MODE=vision`만 설정하면 동작하지 않는다.

Render에서 실제 OCR을 사용하려면 다음 중 하나가 필요하다.

- 외부에서 접근 가능한 Ollama Vision 서버
- GPU 서버에 배포한 `qwen2.5vl`
- 별도의 상용 Vision OCR API로 교체

외부 Vision 서버를 준비한 경우 Render에 다음을 설정한다.

```dotenv
OCR_MODE=vision
OLLAMA_VISION_BASE_URL=https://EXTERNAL-VISION-ENDPOINT
OLLAMA_VISION_MODEL=qwen2.5vl
OLLAMA_VISION_API_KEY=필요한_경우_키
```

### 9.3 실제 임베딩

`bge-m3`도 기본적으로 로컬 Ollama를 사용한다. Render에서 외부 임베딩 서버를 설정하지 않으면 연결 실패 시 경량 Hash 임베딩으로 Fallback한다. 검색 파이프라인은 계속 작동하지만 정확도는 낮아질 수 있다.

완전한 배포용 의미 임베딩을 사용하려면 다음을 설정한다.

```dotenv
OLLAMA_EMBED_BASE_URL=https://EXTERNAL-EMBED-ENDPOINT
OLLAMA_EMBED_MODEL=bge-m3
OLLAMA_EMBED_API_KEY=필요한_경우_키
```

## 10. 법령 화면의 의미

### 관련 조문 원문 확인

지급절차 판정에 실제로 사용한 근거조문을 정확한 조문번호로 조회해 보여주는 영역이다.

### 관련 법령

거래 당사자가 제출해야 하는 신고서·신청서·첨부서류를 찾기 위해 검색하고 검증한 핵심 조문 영역이다.

두 영역의 목적이 다르므로 서로 다른 조문이 표시될 수 있다.

## 11. 필요서류 표시 기준

### 필수서류

법령에서 거래 당사자가 신고 시 제출해야 한다고 명시한 신고서와 첨부서류다. 다음 단계 진행을 위해 확인해야 한다.

### 조건부서류

`기타 신고기관의 장이 필요하다고 인정하는 서류`처럼 특정 요구가 있을 때만 제출하는 문서다. 화면에는 `(요구 시)`로 표시하고 체크하지 않아도 다음 단계 진행을 막지 않는다.

### CSV Fallback

법령에서 문서명을 추출하지 못했을 때만 `reason_codes.csv.required_documents`를 테스트용 목록으로 사용한다.

## 12. 현재 남은 한계

### 12.1 은행 실무서류 자동 병합 미구현

현재는 다음 구조다.

```text
법령 추출 성공 → 법령 추출 서류만 표시
법령 추출 실패 → CSV 서류 표시
```

최종적으로 필요한 다음 구조는 아직 구현되지 않았다.

```text
법령상 핵심서류
+ 은행 공통서류
+ 거래조건별 추가서류
```

### 12.2 OCR 기반 조건부서류 판정 미구현

현재 OCR은 합작투자·1년 이상 대부투자·현물출자·가액 차이·신규 지정은행 여부를 구조화하지 않는다. 조건부서류가 표시되지 않는 것은 OCR이 조건 불일치로 판정했기 때문이 아니라, 해당 조건 입력과 규칙이 아직 구현되지 않았기 때문이다.

### 12.3 법률 표현과 실무 문서명 정규화 미구현

예를 들어 다음 대응표가 아직 없다.

```text
조세체납이 없음을 입증하는 서류
→ 국세납세증명서

종합신용정보집중기관에 등록되어 있지 않음을 입증하는 서류
→ 신용정보조회표 또는 관련 조회·동의서
```

따라서 법률 문장 전체가 체크박스명으로 표시될 수 있다.

### 12.4 복수 핵심 조문 병합 미구현

서로 다른 거래단계의 서류가 섞이지 않도록 현재는 첫 번째 핵심 제출 조문 한 건에서만 필요서류를 만든다. 동시에 적용되는 여러 조문을 병합하려면 적용관계 판단 로직이 추가로 필요하다.

### 12.5 서식 저장소와 체크리스트 보강 미완성

별지·서식은 API로 조회하고 별도 저장하지만, 조문에서 발견한 참조번호로 서식의 정식 명칭과 내용을 체크리스트에 자동 보강하는 전체 호출 경로는 아직 완성되지 않았다.

### 12.6 `COMPLETE` 상태의 제한

`COMPLETE`는 제출 Anchor와 번호 목록을 함께 추출했다는 의미다. 실제 은행 접수에 필요한 모든 필수·조건부 서류가 완성됐다는 의미는 아니다.

### 12.7 배포 저장소의 지속성

현재 SQLite DB와 법령·Chroma 캐시는 로컬 파일 기반이다. Render 인스턴스 재배포나 파일시스템 초기화 시 거래 기록과 캐시가 유지되지 않을 수 있으므로 운영환경에서는 관리형 DB와 영속 스토리지 검토가 필요하다.

## 13. 보안 및 배포 주의사항

- `.env`를 Git에 커밋하지 않는다.
- `LAW_API_KEY`, `OLLAMA_API_KEY`는 Render Secret 환경변수로 등록한다.
- 로그에 API 키를 출력하지 않는다.
- `data/uploads`의 신청서는 개인정보를 포함할 수 있으므로 보존정책과 삭제정책이 필요하다.
- 법령 RAG 결과는 업무 참고정보이며 최종 법률 판단과 승인 여부는 은행원이 확인한다.
- 국가법령정보 API Snapshot의 갱신일과 인덱스 버전을 운영 중 확인한다.

## 14. 다음 개발 우선순위

1. 은행 공통서류 데이터 구조와 법령 서류의 병합 규칙
2. 필수·조건부 서류를 구분할 거래조건 스키마
3. OCR·은행 시스템·은행원 입력값을 이용한 조건 판정
4. 법률 문구를 실제 은행 접수 문서명으로 정규화하는 대응표
5. 복수 적용 조문의 충돌 없는 병합
6. 별지·서식 Exact Store와 체크리스트 연결
7. 외부 Vision·Embedding 서비스 연결
8. 관리형 DB·영속 캐시 적용
9. 법인설립 외 해외부동산·증권·대여·차입·청산·회수 평가세트 구축
10. 정답 조문 Hit@K, 불필요 조문 비율, 필요서류 Precision·Recall 기반 평가

## 15. 주요 수정 파일 요약

| 파일 | 역할 |
|---|---|
| `.env.example` | Mock·PDF·API 모드와 Ollama·법령 API 설정 예시 |
| `.env.render.example` | Render용 환경변수 예시 |
| `config/settings.py` | 전체 실행 모드와 API 설정 로드 |
| `rag/chunker.py` | 조·항·호·목 Parent–Child 청킹 |
| `rag/law_api.py` | 국가법령정보 API 조회·파싱·Snapshot 관리 |
| `rag/retriever.py` | 범용 Query, Reranking, Parent 검증, Sibling 확장, Exact Lookup |
| `services/reason_code/mapper.py` | 법령 원문에서 필요서류 추출 및 CSV Fallback |
| `services/payment_procedure.py` | 지급절차 판정과 정확한 근거 조문번호 제공 |
| `schemas/analysis.py` | 출처·조건부·조문·서식참조·추출상태 필드 |
| `frontend/regulation.py` | Streamlit 화면에 V6 검색·서류 결과 연결 |
| `render_api.py` | V6 RAG와 배포 REST API 연결 |
| `netlify/js/app.js` | 배포 UI의 법령·서류·근거조문·조건부 진행 처리 |
| `netlify/js/api.js` | Netlify와 Render API 통신 |
| `netlify/config.js` | Render API Base URL 설정 |
| `render.yaml` | Render 빌드·실행·환경변수 설정 |
| `requirements-render.txt` | Render 백엔드 의존성 |
| `tests/test_law_api.py` | 법령·행정규칙 JSON 파싱 테스트 |
| `tests/test_rag.py` | 계층 검색·확장·Exact Lookup 테스트 |
| `tests/test_reason_code.py` | 거래 당사자 서류 추출과 기관 의무 제외 테스트 |
| `tests/test_regulation_display.py` | 삭제 문구와 번호 표시 테스트 |
| `tests/test_render_api_rag.py` | 배포 API와 V6 RAG 연결 테스트 |

## 16. 최종 산출물

- 파일명: `foreign-exchange-ai-for-regtech-deploy-rag-api-v7.zip`
- SHA-256: `72E9F864F6B0EA4A4D7C1DEF3839A35D644AE3F74081F4196C21F51E177B6DC8`
- 최종 테스트: `69 passed`

이 통합본은 국가법령정보 API 기반 법령 검색과 법령상 제출서류 추출을 Netlify·Render 배포 구조에 연결한 버전이다. 실제 은행 접수서류 전체 자동완성 단계가 아니라, 법령 근거 검색과 제출서류 후보 추출 정확도를 높인 기반 버전으로 보는 것이 정확하다.
