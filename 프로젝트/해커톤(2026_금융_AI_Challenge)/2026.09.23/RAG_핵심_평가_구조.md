# RAG 핵심 평가 구조

```text
[공통 평가 기반]
Gold Dataset
      ↓
────────────────────────────

[핵심 1] 법령 표현
API
→ 파싱
→ 계층적 청킹
→ 필요 시 재귀 청킹
→ Embedding / Vector DB
      ↓

[핵심 2] 정답 검색
Query
→ Retrieval
→ Top-K
→ Recall@K
      ↓

[핵심 3] 정답 선택
Legal Scope
→ Reranking
→ Top-1
→ Top-1 Accuracy / MRR
      ↓

[핵심 4] 근거 추출
정답 조문
→ 필요한 항/호/목 선택
→ 필요서류 추출
→ Precision / Recall / F1
      ↓

────────────────────────────
[전체 검증]
End-to-End Accuracy

[운영 기반]
최신 법령 유지 / 인덱스 갱신
```
