"""국가법령정보 공동활용 API 연동.

프로젝트의 기존 PDF/Mock RAG는 그대로 두고, 필요할 때 법령 ID를 이용해
국가법령정보센터의 현행 법령 JSON을 받아 RAG 인덱싱용 레코드로 변환한다.

API Key는 프로젝트 루트 ``.env``의 ``LAW_API_KEY``를 사용한다. 향후
``config.settings.Settings``에 ``law_api_key`` 필드가 추가되면 그 값도 자동으로
우선 사용한다.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Iterable

import requests
from dotenv import dotenv_values

from config.settings import get_settings

LAW_SEARCH_URL = "https://www.law.go.kr/DRF/lawSearch.do"
LAW_SERVICE_URL = "https://www.law.go.kr/DRF/lawService.do"
LAW_API_RESPONSE_TYPE = "JSON"
PROJECT_ROOT = Path(__file__).resolve().parent.parent


class LawAPIError(RuntimeError):
    """국가법령정보 API 호출 또는 응답 변환 실패."""


def _load_law_api_key() -> str:
    """프로젝트 설정 또는 루트 .env에서 LAW_API_KEY를 읽는다.

    현재 팀 프로젝트의 Settings에는 LAW_API_KEY 필드가 아직 없으므로
    RAG 폴더만 교체해도 동작하도록 .env fallback을 둔다.
    """

    settings = get_settings()
    configured = getattr(settings, "law_api_key", None)
    if configured:
        return str(configured).strip()

    env_values = dotenv_values(PROJECT_ROOT / ".env")
    return str(env_values.get("LAW_API_KEY") or "").strip()


class LawAPIClient:
    def __init__(self, api_key: str | None = None, timeout: int = 30):
        self.api_key = (api_key if api_key is not None else _load_law_api_key()).strip()
        self.timeout = timeout

        if not self.api_key:
            raise ValueError(
                "LAW_API_KEY가 비어 있습니다. 프로젝트 루트 .env에 "
                'LAW_API_KEY="..." 값을 입력해주세요.'
            )

    def _get_json(self, url: str, params: dict[str, Any]) -> dict[str, Any]:
        request_params = {
            "OC": self.api_key,
            "type": LAW_API_RESPONSE_TYPE,
            **params,
        }
        response = requests.get(url, params=request_params, timeout=self.timeout)
        response.raise_for_status()

        try:
            payload = response.json()
        except ValueError as exc:
            raise LawAPIError("국가법령정보 API 응답을 JSON으로 해석하지 못했습니다.") from exc

        if not isinstance(payload, dict):
            raise LawAPIError("예상하지 못한 국가법령정보 API 응답 형식입니다.")
        return payload

    def search_laws(
        self,
        query: str,
        display: int = 20,
        page: int = 1,
        search: int = 1,
    ) -> dict[str, Any]:
        """법령명/본문 검색 결과 JSON을 반환한다."""

        return self._get_json(
            LAW_SEARCH_URL,
            {
                "target": "law",
                "query": query,
                "display": max(1, min(display, 100)),
                "page": max(1, page),
                "search": search,
            },
        )

    def fetch_law_json(
        self,
        law_id: str | int,
        article_code: str | None = None,
    ) -> dict[str, Any]:
        """법령 ID로 현행 법령 본문 JSON을 가져온다."""

        params: dict[str, Any] = {
            "target": "law",
            "ID": str(law_id),
        }
        if article_code:
            params["JO"] = article_code
        return self._get_json(LAW_SERVICE_URL, params)

    @staticmethod
    def _find_first_value(payload: Any, keys: Iterable[str]) -> str:
        wanted = set(keys)

        def walk(value: Any) -> str | None:
            if isinstance(value, dict):
                for key, child in value.items():
                    if key in wanted and child not in (None, "", [], {}):
                        return str(child).strip()
                for child in value.values():
                    found = walk(child)
                    if found:
                        return found
            elif isinstance(value, list):
                for child in value:
                    found = walk(child)
                    if found:
                        return found
            return None

        return walk(payload) or ""

    @staticmethod
    def _extract_legal_text(payload: Any) -> str:
        """JSON의 조/항/호/목 본문을 순서에 가깝게 텍스트로 정리한다."""

        content_keys = {
            "조문내용",
            "항내용",
            "호내용",
            "목내용",
            "부칙내용",
            "별표내용",
        }
        lines: list[str] = []

        def add_text(value: Any) -> None:
            if value is None:
                return
            text = str(value).replace("\r\n", "\n").replace("\r", "\n")
            for line in text.splitlines():
                cleaned = re.sub(r"[ \t]+", " ", line).strip()
                # 중첩 JSON 때문에 동일 내용이 연속으로 반복되는 경우만 제거한다.
                if cleaned and (not lines or lines[-1] != cleaned):
                    lines.append(cleaned)

        def walk(value: Any) -> None:
            if isinstance(value, dict):
                for key, child in value.items():
                    if key in content_keys:
                        add_text(child)
                    else:
                        walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)

        walk(payload)

        # API 구조가 달라져 본문 키를 못 찾았을 때의 최소 fallback.
        if not lines:
            def fallback(value: Any) -> None:
                if isinstance(value, dict):
                    for child in value.values():
                        fallback(child)
                elif isinstance(value, list):
                    for child in value:
                        fallback(child)
                elif isinstance(value, str) and len(value.strip()) >= 20:
                    add_text(value)

            fallback(payload)

        return "\n".join(lines).strip()

    def to_rag_record(
        self,
        payload: dict[str, Any],
        law_id: str | int | None = None,
    ) -> dict[str, Any]:
        """API JSON을 ``RagIndexer.index_records`` 입력 형식으로 변환한다."""

        law_name = self._find_first_value(
            payload,
            ("법령명_한글", "법령명한글", "법령명", "법령명칭"),
        ) or "법령명 없음"

        raw_id = law_id or self._find_first_value(payload, ("법령ID", "법령아이디"))
        resolved_id = str(raw_id).strip() if raw_id not in (None, "") else ""
        effective_date = self._find_first_value(payload, ("시행일자", "시행일"))
        revision_date = self._find_first_value(payload, ("공포일자", "개정일자"))
        promulgation_number = self._find_first_value(payload, ("공포번호",))
        text = self._extract_legal_text(payload)

        if not text:
            raise LawAPIError(f"{law_name} 본문에서 RAG용 텍스트를 추출하지 못했습니다.")

        source_url = ""
        if resolved_id:
            source_url = (
                f"{LAW_SERVICE_URL}?target=law&ID={resolved_id}&type={LAW_API_RESPONSE_TYPE}"
            )

        return {
            "text": text,
            "source": f"law_api:{resolved_id or law_name}",
            "law_name": law_name,
            "document_type": "law_api",
            "law_id": resolved_id,
            "effective_date": effective_date,
            "revision_date": revision_date,
            "promulgation_number": promulgation_number,
            "source_url": source_url,
        }

    def fetch_rag_record(self, law_id: str | int) -> dict[str, Any]:
        return self.to_rag_record(self.fetch_law_json(law_id), law_id=law_id)

    def fetch_rag_records(self, law_ids: Iterable[str | int]) -> list[dict[str, Any]]:
        return [self.fetch_rag_record(law_id) for law_id in law_ids]
