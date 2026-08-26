"""국가법령정보 API 데이터용 Parent-Child 인덱서.

기존 팀 프로젝트의 PDF/Mock 색인 방식은 ``RagRetriever.build_index``에 그대로
남겨 두고, API에서 받은 법령만 이 인덱서를 통해 다음 순서로 처리한다.

정규화 → 조문(Parent) 파싱 → 항/호/목 단위 Child 청킹 → 기존 ChunkEmbedder
(Ollama bge-m3 우선 / hash fallback) → 기존 ChromaDB 컬렉션 저장.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from database.connection import get_session
from database.models import RagChunk, RagDocument

from rag.law_api import LawAPIClient


class RagIndexer:
    CHAPTER_PATTERN = re.compile(r"^제\s*\d+\s*장(?:\s+.*)?$")
    SECTION_PATTERN = re.compile(r"^제\s*\d+\s*절(?:\s+.*)?$")
    ARTICLE_PATTERN = re.compile(
        r"^(제\s*\d+(?:-\d+)?\s*조(?:의\s*\d+)?)(?:\s*\(([^)]*)\))?"
    )
    STRUCTURE_PATTERN = re.compile(
        r"^(?:[①-⑳]|제\s*\d+\s*항|\d+\s*[.)]|[가-하]\s*[.)])"
    )

    def __init__(
        self,
        collection,
        embedder,
        parent_store_path: str | Path,
        child_min_chars: int = 250,
        child_max_chars: int = 1200,
        child_overlap_chars: int = 120,
        parent_soft_max_chars: int = 5000,
    ) -> None:
        self.collection = collection
        self.embedder = embedder
        self.parent_store_path = Path(parent_store_path)
        self.child_min_chars = child_min_chars
        self.child_max_chars = child_max_chars
        self.child_overlap_chars = child_overlap_chars
        self.parent_soft_max_chars = parent_soft_max_chars
        self.parents = self._load_parent_store()

    # ------------------------------------------------------------------
    # 공통 유틸
    # ------------------------------------------------------------------

    @staticmethod
    def _normalize_text(text: Any) -> str:
        value = str(text if text is not None else "")
        value = value.replace("\r\n", "\n").replace("\r", "\n").replace("\x00", "")
        lines = [re.sub(r"[ \t]+", " ", line).rstrip() for line in value.splitlines()]
        return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()

    @staticmethod
    def _stable_id(*values: Any) -> str:
        raw = "|".join(str(v) for v in values)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def _load_parent_store(self) -> dict[str, dict[str, Any]]:
        if not self.parent_store_path.is_file():
            return {}
        try:
            data = json.loads(self.parent_store_path.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

    def _save_parent_store(self) -> None:
        self.parent_store_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self.parent_store_path.with_suffix(self.parent_store_path.suffix + ".tmp")
        tmp_path.write_text(
            json.dumps(self.parents, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        tmp_path.replace(self.parent_store_path)

    def clear_parent_store(self) -> None:
        self.parents = {}
        if self.parent_store_path.exists():
            self.parent_store_path.unlink()

    # ------------------------------------------------------------------
    # Parent 파싱
    # ------------------------------------------------------------------

    def _make_legal_parent(
        self,
        lines: list[str],
        chapter: str,
        section: str,
        metadata: dict[str, Any],
    ) -> dict[str, Any]:
        body = self._normalize_text("\n".join(lines))
        match = self.ARTICLE_PATTERN.match(lines[0].strip())
        article = match.group(1) if match else "조문 번호 없음"
        article_title = match.group(2) if match and match.group(2) else ""
        law_name = metadata.get("law_name") or metadata.get("source") or "법령명 없음"

        header = [f"[법령명] {law_name}"]
        if chapter:
            header.append(f"[장] {chapter}")
        if section:
            header.append(f"[절] {section}")
        content = "\n".join(header + [body])
        parent_id = self._stable_id(metadata.get("source", ""), article, body)

        return {
            "parent_id": parent_id,
            "source": metadata.get("source", "출처 없음"),
            "law_name": law_name,
            "document_type": metadata.get("document_type", "law_api"),
            "chapter": chapter,
            "section": section,
            "article": article,
            "article_title": article_title,
            "body": body,
            "content": content,
            "document_metadata": metadata,
        }

    def _make_generic_parents(
        self,
        text: str,
        metadata: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """조문 번호가 없는 응답도 검색 가능하도록 큰 문서 조각으로 보존."""

        parts: list[str] = []
        start = 0
        while start < len(text):
            end = min(start + self.parent_soft_max_chars, len(text))
            part = text[start:end].strip()
            if part:
                parts.append(part)
            if end >= len(text):
                break
            start = end

        source = metadata.get("source", "출처 없음")
        law_name = metadata.get("law_name") or source
        parents: list[dict[str, Any]] = []
        for index, body in enumerate(parts):
            parent_id = self._stable_id(source, "generic", index, body)
            parents.append(
                {
                    "parent_id": parent_id,
                    "source": source,
                    "law_name": law_name,
                    "document_type": metadata.get("document_type", "law_api"),
                    "chapter": "",
                    "section": "",
                    "article": f"문서 조각 {index + 1}",
                    "article_title": "",
                    "body": body,
                    "content": f"[법령명] {law_name}\n{body}",
                    "document_metadata": metadata,
                }
            )
        return parents

    def _build_parents(self, text: str, metadata: dict[str, Any]) -> list[dict[str, Any]]:
        lines = text.splitlines()
        parents: list[dict[str, Any]] = []
        current_article_lines: list[str] = []
        current_chapter = ""
        current_section = ""

        def flush() -> None:
            nonlocal current_article_lines
            if current_article_lines:
                parents.append(
                    self._make_legal_parent(
                        current_article_lines,
                        current_chapter,
                        current_section,
                        metadata,
                    )
                )
                current_article_lines = []

        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                if current_article_lines:
                    current_article_lines.append("")
                continue
            if self.CHAPTER_PATTERN.match(line):
                flush()
                current_chapter = line
                current_section = ""
                continue
            if self.SECTION_PATTERN.match(line):
                flush()
                current_section = line
                continue
            if self.ARTICLE_PATTERN.match(line):
                flush()
                current_article_lines = [line]
                continue
            if current_article_lines:
                current_article_lines.append(line)

        flush()
        return parents or self._make_generic_parents(text, metadata)

    # ------------------------------------------------------------------
    # Child 청킹
    # ------------------------------------------------------------------

    def _split_long_unit(self, text: str, max_chars: int) -> list[str]:
        if len(text) <= max_chars:
            return [text]
        overlap = min(self.child_overlap_chars, max(0, max_chars // 4))
        step = max(1, max_chars - overlap)
        chunks: list[str] = []
        start = 0
        while start < len(text):
            piece = text[start : start + max_chars].strip()
            if piece:
                chunks.append(piece)
            if start + max_chars >= len(text):
                break
            start += step
        return chunks

    def _build_children(self, parent: dict[str, Any]) -> list[dict[str, Any]]:
        header_lines = [f"[법령명] {parent['law_name']}"]
        if parent.get("chapter"):
            header_lines.append(f"[장] {parent['chapter']}")
        if parent.get("section"):
            header_lines.append(f"[절] {parent['section']}")
        header_lines.append(f"[조문] {parent['article']}")
        if parent.get("article_title"):
            header_lines.append(f"[조문 제목] {parent['article_title']}")
        header = "\n".join(header_lines)

        body_max = max(120, self.child_max_chars - len(header) - 1)
        body_min = max(80, self.child_min_chars - len(header) - 1)

        lines = [line.strip() for line in parent["body"].splitlines() if line.strip()]
        structural_units: list[str] = []
        current: list[str] = []
        for line in lines:
            if self.STRUCTURE_PATTERN.match(line) and current:
                structural_units.append("\n".join(current))
                current = [line]
            else:
                current.append(line)
        if current:
            structural_units.append("\n".join(current))

        split_units: list[str] = []
        for unit in structural_units or [parent["body"]]:
            split_units.extend(self._split_long_unit(unit, body_max))

        body_chunks: list[str] = []
        current_parts: list[str] = []
        for unit in split_units:
            candidate = "\n".join(current_parts + [unit])
            if len(candidate) <= body_max:
                current_parts.append(unit)
                continue
            if current_parts:
                body_chunks.append("\n".join(current_parts))
            current_parts = [unit]
        if current_parts:
            body_chunks.append("\n".join(current_parts))

        if len(body_chunks) >= 2 and len(body_chunks[-1]) < body_min:
            combined = body_chunks[-2] + "\n" + body_chunks[-1]
            if len(combined) <= body_max:
                body_chunks[-2] = combined
                body_chunks.pop()

        children: list[dict[str, Any]] = []
        for child_index, body in enumerate(body_chunks):
            content = f"{header}\n{body}"
            children.append(
                {
                    "child_index": child_index,
                    "content": content,
                    "child_id": self._stable_id(parent["parent_id"], child_index, content),
                }
            )
        return children

    # ------------------------------------------------------------------
    # Chroma / SQL 저장
    # ------------------------------------------------------------------

    def index_records(self, records: list[dict[str, Any]], force: bool = True) -> int:
        """법령 API 레코드를 현재 RAG Chroma 컬렉션에 적재한다.

        ``force=True``가 기본인 이유는 PDF/Mock/API가 동일 컬렉션과 SQL 원문
        테이블을 공유하기 때문이다. API 법령 세트를 갱신할 때 한 벌 전체를 다시
        만드는 방식이 가장 예측 가능하다.
        """

        if not records:
            return 0

        if force:
            existing_ids = self.collection.get()["ids"] if self.collection.count() else []
            if existing_ids:
                self.collection.delete(ids=existing_ids)
            with get_session() as session:
                session.execute(RagChunk.__table__.delete())
                session.execute(RagDocument.__table__.delete())
            self.clear_parent_store()

        rows: list[dict[str, Any]] = []

        with get_session() as session:
            for record_index, record in enumerate(records):
                text = self._normalize_text(record.get("text", ""))
                if not text:
                    continue

                metadata = {k: v for k, v in record.items() if k != "text"}
                source = str(metadata.get("source") or f"law_api_record_{record_index}")
                law_name = str(metadata.get("law_name") or source)
                law_id = str(metadata.get("law_id") or "")
                source_url = str(metadata.get("source_url") or "")
                file_name = f"law_api_{law_id}.json" if law_id else f"{law_name}.json"

                doc = RagDocument(
                    file_name=file_name,
                    title=law_name,
                    source_path=source_url or source,
                    is_sample=False,
                )
                session.add(doc)
                session.flush()

                parents = self._build_parents(text, metadata)
                chunk_index = 0
                for parent in parents:
                    self.parents[parent["parent_id"]] = {
                        "parent_id": parent["parent_id"],
                        "source": parent["source"],
                        "law_name": parent["law_name"],
                        "article": parent["article"],
                        "article_title": parent["article_title"],
                        "chapter": parent["chapter"],
                        "section": parent["section"],
                        "content": parent["content"],
                        "source_url": source_url,
                        "effective_date": str(metadata.get("effective_date") or ""),
                        "revision_date": str(metadata.get("revision_date") or ""),
                    }

                    for child in self._build_children(parent):
                        db_row = RagChunk(
                            document_id=doc.id,
                            chunk_index=chunk_index,
                            page_number=None,
                            article=parent["article"],
                            content=child["content"],
                        )
                        session.add(db_row)
                        session.flush()
                        chunk_index += 1

                        rows.append(
                            {
                                "chunk_id": db_row.id,
                                "content": child["content"],
                                "law_name": law_name,
                                "article": parent["article"],
                                "file_name": file_name,
                                "is_sample": False,
                                "parent_id": parent["parent_id"],
                                "source": source,
                                "source_url": source_url,
                                "effective_date": str(metadata.get("effective_date") or ""),
                                "revision_date": str(metadata.get("revision_date") or ""),
                            }
                        )

        if not rows:
            return 0

        texts = [row["content"] for row in rows]
        embeddings = self.embedder.embed(texts)
        self.collection.add(
            ids=[str(row["chunk_id"]) for row in rows],
            embeddings=embeddings,
            documents=texts,
            metadatas=[
                {
                    "law_name": row["law_name"],
                    "article": row["article"],
                    "file_name": row["file_name"],
                    "page_number": 0,
                    "is_sample": False,
                    "regulation_tags": "",
                    "parent_id": row["parent_id"],
                    "source": row["source"],
                    "source_type": "law_api",
                    "source_url": row["source_url"],
                    "effective_date": row["effective_date"],
                    "revision_date": row["revision_date"],
                }
                for row in rows
            ],
        )
        self._save_parent_store()
        return len(rows)

    def index_law_ids(
        self,
        law_ids: list[str | int],
        force: bool = True,
        api_key: str | None = None,
    ) -> int:
        client = LawAPIClient(api_key=api_key)
        records = client.fetch_rag_records(law_ids)
        return self.index_records(records, force=force)
