"""RAG 검색 Pipeline 오케스트레이션 (섹션 15~17).

국가법령정보센터 PDF(``RAG_MODE=pdf``) 또는 샘플 규정 데이터
(``RAG_MODE=mock``)를 읽어 Chunking → Embedding → Vector DB 색인을 수행하고,
질의에 대해 관련 법령/조문을 검색한다.

RAG 결과는 은행원의 업무 참고 정보이며 법률적 최종 판단으로 표현하지 않는다.
"""

from __future__ import annotations

import chromadb
from pathlib import Path
from sqlalchemy import select

from config.settings import get_settings
from database.connection import get_session
from database.models import RagChunk, RagDocument
from schemas.analysis import RegulationMatch
from rag.chunker import chunk_text
from rag.document_loader import load_all_regulation_pdfs
from rag.embedder import ChunkEmbedder
from rag.indexer import RagIndexer
from rag.sample_regulations import SAMPLE_FILE_NAME, SAMPLE_REGULATIONS
from utils.logging import get_logger

logger = get_logger(__name__)


class RagRetriever:
    def __init__(self) -> None:
        settings = get_settings()
        self._settings = settings
        self._embedder = ChunkEmbedder()
        chroma_client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
        collection_name = f"rag_chunks_{self._embedder.backend_name}"
        self._collection = chroma_client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        self._indexer = RagIndexer(
            collection=self._collection,
            embedder=self._embedder,
            parent_store_path=(
                Path(settings.chroma_persist_dir) / f"{collection_name}_parents.json"
            ),
        )

    @property
    def embedding_backend(self) -> str:
        """실제 사용 중인 임베딩 백엔드("ollama"/"hash"). services/reason_code/mapper.py의
        동일 프로퍼티 참고 - Ollama 연결 실패 시 조용히 해시 임베딩으로 폴백하는 것을
        화면에 노출하기 위함이다."""

        return self._embedder.backend_name

    # ------------------------------------------------------------------
    # 색인
    # ------------------------------------------------------------------

    def build_index(self, force: bool = False) -> int:
        if self._collection.count() > 0:
            if not force:
                logger.info("RAG 인덱스가 이미 존재합니다 (force=True로 재생성 가능)")
                return self._collection.count()
            existing_ids = self._collection.get()["ids"]
            if existing_ids:
                self._collection.delete(ids=existing_ids)
            # API Parent-Child 색인을 사용한 뒤 PDF/Mock으로 재색인하는 경우
            # 이전 Parent 저장소가 남지 않도록 함께 초기화한다.
            self._indexer.clear_parent_store()

        # SQL의 rag_documents/rag_chunks는 "가장 최근에 색인한 한 벌"만 원문 출처로
        # 보존한다. 임베딩 백엔드(Mock 해시 ↔ Ollama)를 변경해 컬렉션 이름이
        # 바뀌면 이전 컬렉션의 벡터는 그대로 남지만 SQL 원문은 새로 색인한
        # 데이터로 교체된다 - 프로토타입 범위에서는 이 제약을 감수한다.
        with get_session() as session:
            session.execute(RagChunk.__table__.delete())
            session.execute(RagDocument.__table__.delete())

        chunk_rows = self._build_source_chunks()
        if not chunk_rows:
            logger.warning("색인할 RAG 문서가 없습니다.")
            return 0

        texts = [row["content"] for row in chunk_rows]
        embeddings = self._embedder.embed(texts)

        self._collection.add(
            ids=[str(row["chunk_id"]) for row in chunk_rows],
            embeddings=embeddings,
            documents=texts,
            metadatas=[
                {
                    "law_name": row["law_name"],
                    "article": row["article"] or "",
                    "file_name": row["file_name"],
                    "page_number": row["page_number"] or 0,
                    "is_sample": row["is_sample"],
                    "regulation_tags": "|".join(row.get("regulation_tags") or []),
                }
                for row in chunk_rows
            ],
        )
        logger.info(
            "RAG 청크 %d건 인덱싱 완료 (embedding backend=%s)",
            len(chunk_rows),
            self._embedder.backend_name,
        )
        return len(chunk_rows)

    def _build_source_chunks(self) -> list[dict]:
        """PDF(있으면) 또는 샘플 규정 데이터를 SQL(RagDocument/RagChunk)에 저장하고,
        Chroma 색인에 필요한 정보를 함께 반환한다."""

        if self._settings.rag_mode == "pdf":
            pages = load_all_regulation_pdfs(self._settings.regulation_pdf_dir)
            if pages:
                return self._store_pdf_chunks(pages)
            logger.warning(
                "RAG_MODE=pdf 이지만 data/regulations/ 에 PDF가 없어 샘플 규정으로 대체합니다."
            )

        return self._store_sample_chunks()

    def _store_pdf_chunks(self, pages) -> list[dict]:
        rows: list[dict] = []
        with get_session() as session:
            doc_by_file: dict[str, RagDocument] = {}
            # 긴 조문이 여러 청크로 쪼개지면 뒤쪽 청크에는 "제O조" 표시가 그
            # 청크 안에 없을 수 있다. 문서별로 마지막으로 발견한 조문 번호를
            # 기억해두었다가, 자체적으로 못 찾은 청크에 이어서 적용한다
            # (페이지가 넘어가도 조문은 이어질 수 있어 문서 단위로 유지한다).
            last_article_by_file: dict[str, str | None] = {}
            for page in pages:
                doc = doc_by_file.get(page.file_name)
                if doc is None:
                    doc = RagDocument(file_name=page.file_name, title=page.file_name, is_sample=False)
                    session.add(doc)
                    session.flush()
                    doc_by_file[page.file_name] = doc
                    last_article_by_file[page.file_name] = None

                for i, chunk in enumerate(chunk_text(page.text, page_number=page.page_number)):
                    article = chunk.article or last_article_by_file[page.file_name]
                    if chunk.article:
                        last_article_by_file[page.file_name] = chunk.article

                    row = RagChunk(
                        document_id=doc.id,
                        chunk_index=i,
                        page_number=chunk.page_number,
                        article=article,
                        content=chunk.content,
                    )
                    session.add(row)
                    session.flush()
                    rows.append(
                        {
                            "chunk_id": row.id,
                            "content": row.content,
                            "law_name": doc.title or doc.file_name,
                            "article": row.article,
                            "file_name": doc.file_name,
                            "page_number": row.page_number,
                            "is_sample": False,
                            "regulation_tags": [],  # 실제 PDF는 조문별 태깅 정보가 없음
                        }
                    )
        return rows

    def _store_sample_chunks(self) -> list[dict]:
        rows: list[dict] = []
        with get_session() as session:
            doc = RagDocument(file_name=SAMPLE_FILE_NAME, title="외국환거래규정 (샘플)", is_sample=True)
            session.add(doc)
            session.flush()

            for i, sample in enumerate(SAMPLE_REGULATIONS):
                row = RagChunk(
                    document_id=doc.id,
                    chunk_index=i,
                    page_number=None,
                    article=sample.article,
                    content=sample.content,
                )
                session.add(row)
                session.flush()
                rows.append(
                    {
                        "chunk_id": row.id,
                        "content": row.content,
                        "law_name": sample.law_name,
                        "article": row.article,
                        "file_name": doc.file_name,
                        "page_number": None,
                        "is_sample": True,
                        "regulation_tags": sample.regulation_tags,
                    }
                )
        return rows

    def build_index_from_law_api(
        self,
        law_ids: list[str | int],
        force: bool = True,
        api_key: str | None = None,
    ) -> int:
        """국가법령정보 API 법령을 Parent-Child 구조로 색인한다.

        기존 ``search()`` 인터페이스는 바뀌지 않는다. API Key를 생략하면
        프로젝트 루트 ``.env``의 ``LAW_API_KEY``를 사용한다.
        """

        return self._indexer.index_law_ids(
            law_ids=law_ids,
            force=force,
            api_key=api_key,
        )

    # ------------------------------------------------------------------
    # 검색
    # ------------------------------------------------------------------

    def search(
        self,
        query_text: str,
        top_k: int = 5,
        regulation_tags: list[str] | None = None,
    ) -> list[RegulationMatch]:
        """관련 법령/조문을 검색한다.

        ``regulation_tags`` 를 전달하면(예: 확정된 사유코드의 regulation_tags)
        해당 태그와 겹치는 문서만으로 범위를 좁힌 뒤 그 안에서 임베딩
        유사도로 정렬한다 - 임의의 가중치를 섞는 것이 아니라 명확한 필터
        조건이다. 겹치는 문서가 하나도 없으면 필터 없이 전체 결과를 반환한다.
        """

        if self._collection.count() == 0:
            self.build_index()
        if self._collection.count() == 0:
            return []

        query_embedding = self._embedder.embed([query_text])[0]
        # 태그 필터를 적용할 수 있도록 전체 후보를 유사도 순으로 가져온다
        # (색인 규모가 프로토타입 수준으로 작아 비용이 크지 않다).
        result = self._collection.query(
            query_embeddings=[query_embedding], n_results=self._collection.count()
        )

        all_matches: list[RegulationMatch] = []
        match_tags: list[set[str]] = []
        seen_parent_ids: set[str] = set()
        for distance, metadata, document in zip(
            result["distances"][0], result["metadatas"][0], result["documents"][0]
        ):
            metadata = metadata or {}
            parent_id = str(metadata.get("parent_id") or "")

            # API 색인은 작은 Child를 검색하고, 같은 Parent(조문)가 여러 번
            # 검색되더라도 가장 높은 순위 1건만 남긴 뒤 조문 전체를 반환한다.
            if parent_id:
                if parent_id in seen_parent_ids:
                    continue
                seen_parent_ids.add(parent_id)
                parent = self._indexer.parents.get(parent_id, {})
                display_content = parent.get("content") or document
            else:
                display_content = document

            score = max(0.0, min(1.0, 1.0 - distance))
            all_matches.append(
                RegulationMatch(
                    law_name=metadata.get("law_name") or "",
                    article=metadata.get("article") or None,
                    content=display_content,
                    file_name=metadata.get("file_name") or "",
                    page_number=(metadata.get("page_number") or None),
                    is_sample=bool(metadata.get("is_sample")),
                    score=round(score, 4),
                )
            )
            match_tags.append(set((metadata.get("regulation_tags") or "").split("|")))

        if regulation_tags:
            tag_set = set(regulation_tags)
            filtered = [
                (m, len(tag_set & tags)) for m, tags in zip(all_matches, match_tags) if tag_set & tags
            ]
            if filtered:
                # 겹치는 태그 개수를 1순위로, 임베딩 유사도를 2순위(동점자 처리)로 정렬한다.
                # 임의의 숫자 가중치를 섞는 점수식이 아니라 명확한 정렬 기준이다.
                filtered.sort(key=lambda pair: (pair[1], pair[0].score), reverse=True)
                return [m for m, _ in filtered[:top_k]]

        return all_matches[:top_k]
