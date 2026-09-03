"""RAG 문서 Chunking (섹션 16).

페이지 텍스트를 검색에 적합한 크기로 분할하면서, 가능하면 조문 번호
(예: "제5-11조")를 함께 태깅하여 출처 표시에 사용한다.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_ARTICLE_RE = re.compile(r"제\s*\d+(?:-\d+)?\s*조(?:의\s*\d+)?")

_DEFAULT_MAX_CHARS = 600
_DEFAULT_OVERLAP = 100


@dataclass
class Chunk:
    content: str
    page_number: int | None
    article: str | None


def _detect_article(text: str) -> str | None:
    match = _ARTICLE_RE.search(text)
    return match.group(0) if match else None


def chunk_text(
    text: str,
    page_number: int | None = None,
    max_chars: int = _DEFAULT_MAX_CHARS,
    overlap: int = _DEFAULT_OVERLAP,
) -> list[Chunk]:
    """단순 슬라이딩 윈도우 Chunking.

    법령 원문은 문단 구조가 일정하지 않은 경우가 많아, 프로토타입에서는
    문자 수 기준의 고정 윈도우 + Overlap 방식을 사용한다.
    """

    text = text.strip()
    if not text:
        return []
    if len(text) <= max_chars:
        return [Chunk(content=text, page_number=page_number, article=_detect_article(text))]

    chunks: list[Chunk] = []
    start = 0
    step = max(max_chars - overlap, 1)
    while start < len(text):
        piece = text[start : start + max_chars].strip()
        if piece:
            chunks.append(Chunk(content=piece, page_number=page_number, article=_detect_article(piece)))
        start += step
    return chunks
