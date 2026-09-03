"""국가법령정보센터 PDF 로더 (섹션 15~16).

``data/regulations/`` 디렉토리의 PDF 파일들을 페이지 단위 텍스트로
추출한다. 법령명/페이지 등 출처 정보를 최대한 보존한다.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader

from utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class PdfPage:
    file_name: str
    page_number: int  # 1-based
    text: str


def find_regulation_pdfs(pdf_dir: str | Path) -> list[Path]:
    directory = Path(pdf_dir)
    if not directory.exists():
        return []
    return sorted(directory.glob("*.pdf"))


def load_pdf_pages(pdf_path: str | Path) -> list[PdfPage]:
    """PDF 1개를 페이지 단위 텍스트로 추출한다.

    텍스트 추출이 실패한 페이지(스캔 이미지 등)는 건너뛰고 경고 로그를
    남긴다 - 프로토타입 범위에서는 OCR 기반 PDF 재처리를 지원하지 않는다.
    """

    path = Path(pdf_path)
    pages: list[PdfPage] = []
    try:
        reader = PdfReader(str(path))
    except Exception:
        logger.exception("PDF 열기 실패: %s", path)
        return pages

    for idx, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception:
            logger.warning("PDF 페이지 텍스트 추출 실패: %s (page=%d)", path.name, idx)
            continue
        text = text.strip()
        if text:
            pages.append(PdfPage(file_name=path.name, page_number=idx, text=text))
    return pages


def load_all_regulation_pdfs(pdf_dir: str | Path) -> list[PdfPage]:
    pages: list[PdfPage] = []
    for pdf_path in find_regulation_pdfs(pdf_dir):
        pages.extend(load_pdf_pages(pdf_path))
    logger.info("PDF %d건에서 총 %d개 페이지 텍스트 추출", len(find_regulation_pdfs(pdf_dir)), len(pages))
    return pages
