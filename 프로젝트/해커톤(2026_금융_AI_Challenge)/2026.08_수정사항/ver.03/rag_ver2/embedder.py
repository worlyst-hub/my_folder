"""RAG 청크 Embedding.

사유코드 검색과 동일한 ``EmbeddingClient`` (Ollama 우선, 실패 시 경량 해시
임베딩으로 폴백)를 재사용하여 임베딩 방식을 프로젝트 전체에서 일관되게
유지한다.
"""

from __future__ import annotations

from services.embedding_client import EmbeddingClient


class ChunkEmbedder:
    def __init__(self) -> None:
        self._client = EmbeddingClient()

    @property
    def backend_name(self) -> str:
        return self._client.backend_name

    def embed(self, texts: list[str]) -> list[list[float]]:
        return self._client.embed(texts)
