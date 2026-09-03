"""
외국환 법령 검색을 위한 RAG 인덱싱·검색 모듈입니다.

이 파일의 책임
1. TXT 또는 정규화된 API 레코드를 입력받습니다.
2. 법령을 조(Parent)와 세부 문맥(Child)으로 나눕니다.
3. Child를 무료 로컬 임베딩 모델로 벡터화하여 ChromaDB에 저장합니다.
4. 질문과 가까운 Child를 검색한 뒤 연결된 Parent 조문을 반환합니다.

이 파일에서 의도적으로 담당하지 않는 기능
- 국가법령정보 API 호출과 .env 로딩
- OCR 처리
- 신고 대상 및 필요 서류의 최종 판정
- Ollama 호출과 최종 답변 생성

위 기능은 역할이 다르므로 별도 파일에서 처리하고, 정규화한 법령 데이터만
load_records()에 전달하도록 구성했습니다.
"""


# os:
# 프로젝트 경로와 파일 경로를 운영체제에 맞게 만들 때 사용합니다.
# Python 표준 라이브러리이므로 별도의 설치가 필요하지 않습니다.
import os

# glob:
# 테스트용 data/regulations 폴더의 *.txt 파일 목록을 찾을 때 사용합니다.
# Python 표준 라이브러리이므로 별도의 설치가 필요하지 않습니다.
import glob

# re:
# 법령의 장·절·조·항·호·목 형태를 찾는 정규표현식에 사용합니다.
# Python 표준 라이브러리입니다.
import re

# json:
# Parent 조문을 디스크에 저장하고 다시 불러올 때 사용합니다.
# Child는 ChromaDB에 저장하고 Parent는 JSON에 한 번만 저장하여
# 같은 긴 조문이 모든 Child metadata에 반복 저장되는 것을 막습니다.
import json

# hashlib:
# 원문 내용으로부터 재현 가능한 고유 ID를 만들 때 사용합니다.
# 동일한 문서를 다시 적재해도 같은 ID가 생성되므로 upsert가 가능합니다.
import hashlib

# chromadb:
# Child 문서와 임베딩 벡터를 저장하고 유사도 검색을 수행하는 벡터 DB입니다.
# 로컬 디스크에서 실행할 수 있으므로 사용량에 따른 API 비용이 없습니다.
import chromadb

# SentenceTransformer:
# 한국어를 포함한 다국어 문장을 숫자 벡터로 변환하는 임베딩 모델을
# 로컬 컴퓨터에서 실행하기 위해 사용합니다.
# 현재 모델은 intfloat/multilingual-e5-base이며 유료 API를 호출하지 않습니다.
# 최초 실행 시 Hugging Face에서 모델 파일을 내려받기 위한 인터넷 연결은 필요합니다.
from sentence_transformers import SentenceTransformer


class RegulationRAG:

    # ========================================================
    # 법령 구조 정규표현식
    # ========================================================

    # 예: 제1장 총칙
    CHAPTER_PATTERN = re.compile(
        r"^제\s*\d+\s*장(?:\s+.*)?$"
    )

    # 예: 제2절 지급과 영수
    SECTION_PATTERN = re.compile(
        r"^제\s*\d+\s*절(?:\s+.*)?$"
    )

    # 예: 제7조(신고 등), 제7조의2(예외)
    ARTICLE_PATTERN = re.compile(
        r"^(제\s*\d+\s*조(?:의\s*\d+)?)"
        r"(?:\s*\(([^)]*)\))?"
    )

    # 항·호·목으로 보이는 줄의 시작을 찾습니다.
    # 법령 원문의 줄바꿈이 보존되어 있을 때 구조 경계를 우선 사용할 수 있습니다.
    STRUCTURE_PATTERN = re.compile(
        r"^(?:"
        r"[①-⑳]"
        r"|제\s*\d+\s*항"
        r"|\d+\s*[.)]"
        r"|[가-하]\s*[.)]"
        r")"
    )


    def __init__(
        self,
        collection_name="financial_regulations_v2",
        embedding_model_name="intfloat/multilingual-e5-base",
        child_min_tokens=250,
        child_max_tokens=450,
        child_overlap_tokens=80,
        parent_soft_max_tokens=1800,
        embedding_batch_size=16
    ):

        # ====================================================
        # 프로젝트 루트
        # ====================================================

        # 기존 rag.py와 동일하게 이 파일이 app 폴더에 있다고 가정하고
        # 한 단계 위를 프로젝트 루트로 사용합니다.
        self.base_dir = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )


        # ====================================================
        # 청킹 설정
        # ====================================================

        # 최소 크기는 가능한 경우에 맞추는 목표값입니다.
        # 조·항 경계를 보존해야 하므로 모든 Child가 정확히 이 값 이상이 되지는 않습니다.
        self.child_min_tokens = child_min_tokens

        # overlap은 구조상 하나인 긴 항이나 긴 문장을 다시 나눌 때만 사용합니다.
        # 정상적인 조·항·호 경계 사이에는 불필요한 중복을 만들지 않습니다.
        self.child_overlap_tokens = child_overlap_tokens

        # Parent는 조 전체를 원칙으로 하므로 이 값은 강제 분할 기준이 아닙니다.
        # 지나치게 긴 조문을 metadata에서 표시하기 위한 권장 크기입니다.
        self.parent_soft_max_tokens = parent_soft_max_tokens

        # 한 번에 임베딩하는 Child 개수입니다.
        # 메모리가 부족하면 8, 여유가 있으면 32 등으로 조정할 수 있습니다.
        self.embedding_batch_size = embedding_batch_size


        # ====================================================
        # 무료 로컬 임베딩 모델
        # ====================================================

        self.embedding_model_name = embedding_model_name

        # 모델을 명시적으로 불러옵니다.
        # 기존 코드처럼 ChromaDB 기본 모델을 암묵적으로 사용하지 않기 때문에
        # 어떤 모델로 DB를 만들었는지 재현하고 관리할 수 있습니다.
        self.embedding_model = SentenceTransformer(
            embedding_model_name
        )

        # 같은 tokenizer를 청킹에도 사용합니다.
        # 따라서 이 파일에서 말하는 토큰은 글자 수가 아니라
        # 실제 임베딩 모델이 인식하는 토큰 수입니다.
        self.tokenizer = self.embedding_model.tokenizer

        model_max_tokens = int(
            getattr(
                self.embedding_model,
                "max_seq_length",
                512
            )
        )

        # E5 모델은 query:/passage: 접두사와 특수 토큰도 입력에 포함합니다.
        # 모델 최대 길이보다 16토큰 작은 값을 안전 상한으로 둡니다.
        safe_child_max_tokens = max(
            64,
            model_max_tokens - 16
        )

        self.child_max_tokens = min(
            child_max_tokens,
            safe_child_max_tokens
        )

        if child_max_tokens > safe_child_max_tokens:

            print(
                "요청한 Child 최대 토큰이 "
                "임베딩 모델의 안전 길이를 초과하여 "
                f"{self.child_max_tokens}토큰으로 조정했습니다."
            )

        if self.child_min_tokens > self.child_max_tokens:

            raise ValueError(
                "child_min_tokens는 "
                "child_max_tokens보다 클 수 없습니다."
            )

        if self.child_overlap_tokens >= self.child_max_tokens:

            raise ValueError(
                "child_overlap_tokens는 "
                "child_max_tokens보다 작아야 합니다."
            )


        # ====================================================
        # ChromaDB
        # ====================================================

        self.chroma_path = os.path.join(
            self.base_dir,
            "chroma_db"
        )

        self.client = chromadb.PersistentClient(
            path=self.chroma_path
        )

        # 기존 collection에는 다른 임베딩 차원의 벡터가 들어 있을 수 있습니다.
        # 이름에 v2를 사용하여 기존 DB와 섞이지 않도록 했습니다.
        # embedding_function=None인 이유는 임베딩을 아래에서 직접 계산하여
        # documents가 아닌 embeddings 인자로 ChromaDB에 전달하기 때문입니다.
        self.collection = (
            self.client.get_or_create_collection(
                name=collection_name,
                embedding_function=None,
                metadata={
                    "embedding_model":
                        self.embedding_model_name
                },
                # 최신 ChromaDB 공식 설정 형식으로 cosine 거리를 지정합니다.
                # E5 임베딩을 normalize한 뒤 cosine 기준으로 비교하기 위함입니다.
                configuration={
                    "hnsw": {
                        "space": "cosine"
                    }
                }
            )
        )

        stored_metadata = (
            self.collection.metadata
            if self.collection.metadata
            else {}
        )

        stored_model_name = stored_metadata.get(
            "embedding_model"
        )

        # 이미 만들어진 collection을 다른 임베딩 모델로 검색하면
        # 벡터 차원 또는 의미 공간이 달라질 수 있으므로 즉시 중단합니다.
        if (
            stored_model_name
            and stored_model_name
            != self.embedding_model_name
        ):

            raise ValueError(
                "기존 ChromaDB collection의 임베딩 모델과 "
                "현재 설정이 다릅니다. "
                f"기존={stored_model_name}, "
                f"현재={self.embedding_model_name}"
            )


        # ====================================================
        # Parent 저장소
        # ====================================================

        # 조 전체 Parent는 검색 벡터로 만들지 않고 JSON에 한 번만 저장합니다.
        # ChromaDB Child metadata에는 parent_id만 넣어 저장 공간 중복을 줄입니다.
        self.parent_store_path = os.path.join(
            self.chroma_path,
            f"{collection_name}_parents.json"
        )

        self.parents = self._load_parent_store()


    # ========================================================
    # 공통 보조 함수
    # ========================================================

    def _normalize_text(
        self,
        text
    ):

        text = str(
            text
            if text is not None
            else ""
        )

        text = text.replace(
            "\r\n",
            "\n"
        ).replace(
            "\r",
            "\n"
        ).replace(
            "\x00",
            ""
        )

        lines = [
            line.rstrip()
            for line in text.splitlines()
        ]

        text = "\n".join(
            lines
        ).strip()

        # 세 줄 이상의 빈 줄은 두 줄로 정리합니다.
        return re.sub(
            r"\n{3,}",
            "\n\n",
            text
        )


    def _count_tokens(
        self,
        text
    ):

        return len(
            self.tokenizer.encode(
                text,
                add_special_tokens=False
            )
        )


    def _stable_id(
        self,
        *values
    ):

        raw_value = "|".join(
            str(value)
            for value in values
        )

        return hashlib.sha256(
            raw_value.encode(
                "utf-8"
            )
        ).hexdigest()


    def _clean_metadata(
        self,
        metadata
    ):

        # ChromaDB metadata는 문자열, 숫자, bool과 같은 단순 값만 저장합니다.
        # None, list, dict는 그대로 넣지 않고 제거하거나 JSON 문자열로 변환합니다.
        cleaned = {}

        for key, value in metadata.items():

            if value is None:

                continue

            if isinstance(
                value,
                (
                    str,
                    int,
                    float,
                    bool
                )
            ):

                cleaned[str(key)] = value

            else:

                cleaned[str(key)] = json.dumps(
                    value,
                    ensure_ascii=False
                )

        return cleaned


    # ========================================================
    # Parent 저장소 읽기 / 쓰기
    # ========================================================

    def _load_parent_store(
        self
    ):

        if not os.path.isfile(
            self.parent_store_path
        ):

            return {}

        try:

            with open(
                self.parent_store_path,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(
                    f
                )

            if isinstance(
                data,
                dict
            ):

                return data

        except Exception as e:

            print(
                "Parent 저장소를 읽지 못했습니다."
            )

            print(e)

        return {}


    def _save_parent_store(
        self
    ):

        os.makedirs(
            os.path.dirname(
                self.parent_store_path
            ),
            exist_ok=True
        )

        temporary_path = (
            self.parent_store_path
            + ".tmp"
        )

        # 임시 파일을 완성한 뒤 os.replace로 교체하면
        # 저장 도중 프로그램이 종료될 때 기존 JSON이 손상될 가능성을 줄일 수 있습니다.
        with open(
            temporary_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.parents,
                f,
                ensure_ascii=False,
                indent=2
            )

        os.replace(
            temporary_path,
            self.parent_store_path
        )


    # ========================================================
    # 임베딩
    # ========================================================

    def _embed_documents(
        self,
        texts
    ):

        # multilingual-e5는 검색 문서 앞에 passage: 접두사를 붙여야 합니다.
        # 한국어 문장이어도 접두사는 학습 방식에 맞춰 영문 그대로 사용합니다.
        passages = [
            f"passage: {text}"
            for text in texts
        ]

        return self.embedding_model.encode(
            passages,
            batch_size=self.embedding_batch_size,
            show_progress_bar=(len(passages) > self.embedding_batch_size),
            normalize_embeddings=True,
            convert_to_numpy=True
        )


    def _embed_query(
        self,
        query
    ):

        # 검색 질문에는 passage:가 아니라 query: 접두사를 사용합니다.
        embedding = self.embedding_model.encode(
            [
                f"query: {query}"
            ],
            batch_size=1,
            show_progress_bar=False,
            normalize_embeddings=True,
            convert_to_numpy=True
        )

        return embedding[0]


    # ========================================================
    # 긴 문장의 재귀 청킹
    # ========================================================

    def _token_window_split(
        self,
        text,
        max_tokens,
        overlap_tokens
    ):

        token_ids = self.tokenizer.encode(
            text,
            add_special_tokens=False
        )

        if len(token_ids) <= max_tokens:

            return [
                text.strip()
            ]

        step = max_tokens - overlap_tokens

        chunks = []

        for start in range(
            0,
            len(token_ids),
            step
        ):

            chunk_token_ids = token_ids[
                start:start + max_tokens
            ]

            chunk = self.tokenizer.decode(
                chunk_token_ids,
                skip_special_tokens=True
            ).strip()

            if chunk:

                chunks.append(
                    chunk
                )

            if start + max_tokens >= len(token_ids):

                break

        return chunks


    def _recursive_split(
        self,
        text,
        max_tokens,
        separators=None
    ):

        text = text.strip()

        if not text:

            return []

        if self._count_tokens(text) <= max_tokens:

            return [
                text
            ]

        # 큰 구조에서 작은 구조 순서로 나눕니다.
        # 문단 → 줄 → 문장 → 공백 순서이며, 모두 실패하면 토큰 창을 사용합니다.
        if separators is None:

            separators = [
                "\n\n",
                "\n",
                ". ",
                " "
            ]

        if not separators:

            return self._token_window_split(
                text,
                max_tokens,
                self.child_overlap_tokens
            )

        separator = separators[0]

        parts = text.split(
            separator
        )

        if len(parts) == 1:

            return self._recursive_split(
                text,
                max_tokens,
                separators[1:]
            )

        chunks = []
        current_parts = []

        for part in parts:

            part = part.strip()

            if not part:

                continue

            candidate_parts = (
                current_parts
                + [part]
            )

            candidate = separator.join(
                candidate_parts
            )

            if self._count_tokens(candidate) <= max_tokens:

                current_parts = candidate_parts

                continue

            if current_parts:

                chunks.append(
                    separator.join(
                        current_parts
                    ).strip()
                )

                current_parts = []

            if self._count_tokens(part) > max_tokens:

                chunks.extend(
                    self._recursive_split(
                        part,
                        max_tokens,
                        separators[1:]
                    )
                )

            else:

                current_parts = [
                    part
                ]

        if current_parts:

            chunks.append(
                separator.join(
                    current_parts
                ).strip()
            )

        return chunks


    # ========================================================
    # Parent 생성
    # ========================================================

    def _create_legal_parent(
        self,
        lines,
        chapter,
        section,
        document_metadata
    ):

        raw_article = self._normalize_text(
            "\n".join(
                lines
            )
        )

        article_match = self.ARTICLE_PATTERN.match(
            lines[0].strip()
        )

        article_number = (
            article_match.group(1)
            if article_match
            else "조문 번호 없음"
        )

        article_title = (
            article_match.group(2)
            if (
                article_match
                and article_match.group(2)
            )
            else ""
        )

        law_name = document_metadata.get(
            "law_name",
            document_metadata.get(
                "source",
                "법령명 없음"
            )
        )

        context_lines = [
            f"[법령명] {law_name}"
        ]

        if chapter:

            context_lines.append(
                f"[장] {chapter}"
            )

        if section:

            context_lines.append(
                f"[절] {section}"
            )

        context_lines.append(
            raw_article
        )

        parent_text = "\n".join(
            context_lines
        )

        parent_id = self._stable_id(
            document_metadata.get(
                "source",
                ""
            ),
            article_number,
            raw_article
        )

        parent_tokens = self._count_tokens(
            parent_text
        )

        return {
            "parent_id": parent_id,
            "source": document_metadata.get(
                "source",
                "출처 없음"
            ),
            "law_name": law_name,
            "document_type": document_metadata.get(
                "document_type",
                "law"
            ),
            "chapter": chapter,
            "section": section,
            "article": article_number,
            "article_title": article_title,
            "body": raw_article,
            "content": parent_text,
            "parent_tokens": parent_tokens,
            "parent_is_long": (
                parent_tokens
                > self.parent_soft_max_tokens
            ),
            "document_metadata": document_metadata
        }


    def _create_generic_parents(
        self,
        text,
        document_metadata
    ):

        # 발표자료·서식·OCR 문서처럼 조문 구조가 없는 자료를 위한 예비 처리입니다.
        # 법령 구조를 찾지 못했을 때만 Parent 크기로 나눕니다.
        parent_chunks = self._recursive_split(
            text,
            self.parent_soft_max_tokens,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " "
            ]
        )

        parents = []

        for index, parent_body in enumerate(
            parent_chunks
        ):

            source = document_metadata.get(
                "source",
                "출처 없음"
            )

            law_name = document_metadata.get(
                "law_name",
                source
            )

            parent_text = (
                f"[문서명] {law_name}\n"
                f"{parent_body}"
            )

            parent_id = self._stable_id(
                source,
                "generic",
                index,
                parent_body
            )

            parents.append({
                "parent_id": parent_id,
                "source": source,
                "law_name": law_name,
                "document_type": document_metadata.get(
                    "document_type",
                    "generic"
                ),
                "chapter": "",
                "section": "",
                "article": f"문서 조각 {index + 1}",
                "article_title": "",
                "body": parent_body,
                "content": parent_text,
                "parent_tokens": self._count_tokens(
                    parent_text
                ),
                "parent_is_long": False,
                "document_metadata": document_metadata
            })

        return parents


    def _build_parents(
        self,
        text,
        document_metadata
    ):

        lines = text.splitlines()

        parents = []
        current_article_lines = []
        current_chapter = ""
        current_section = ""

        def flush_current_article():

            nonlocal current_article_lines

            if not current_article_lines:

                return

            parents.append(
                self._create_legal_parent(
                    current_article_lines,
                    current_chapter,
                    current_section,
                    document_metadata
                )
            )

            current_article_lines = []

        for raw_line in lines:

            line = raw_line.strip()

            if not line:

                if current_article_lines:

                    current_article_lines.append(
                        ""
                    )

                continue

            if self.CHAPTER_PATTERN.match(line):

                flush_current_article()

                current_chapter = line
                current_section = ""

                continue

            if self.SECTION_PATTERN.match(line):

                flush_current_article()

                current_section = line

                continue

            if self.ARTICLE_PATTERN.match(line):

                flush_current_article()

                current_article_lines = [
                    line
                ]

                continue

            if current_article_lines:

                current_article_lines.append(
                    line
                )

        flush_current_article()

        # 조문 형태가 전혀 없으면 일반 문서 청킹으로 전환합니다.
        if not parents:

            return self._create_generic_parents(
                text,
                document_metadata
            )

        return parents


    # ========================================================
    # Child 생성
    # ========================================================

    def _build_children(
        self,
        parent
    ):

        header_lines = [
            f"[법령명] {parent['law_name']}"
        ]

        if parent.get(
            "chapter"
        ):

            header_lines.append(
                f"[장] {parent['chapter']}"
            )

        if parent.get(
            "section"
        ):

            header_lines.append(
                f"[절] {parent['section']}"
            )

        header_lines.append(
            f"[조문] {parent['article']}"
        )

        if parent.get(
            "article_title"
        ):

            header_lines.append(
                f"[조문 제목] {parent['article_title']}"
            )

        header = "\n".join(
            header_lines
        )

        header_tokens = self._count_tokens(
            header
        )

        body_max_tokens = max(
            32,
            self.child_max_tokens
            - header_tokens
        )

        body_min_tokens = max(
            16,
            self.child_min_tokens
            - header_tokens
        )

        # 줄바꿈이 보존된 법령은 항·호·목 단위를 우선합니다.
        # 구조 표시가 없는 긴 줄만 재귀 청킹합니다.
        lines = [
            line.strip()
            for line in parent["body"].splitlines()
            if line.strip()
        ]

        structural_units = []
        current_unit = []

        for line in lines:

            if (
                self.STRUCTURE_PATTERN.match(line)
                and current_unit
            ):

                structural_units.append(
                    "\n".join(
                        current_unit
                    )
                )

                current_unit = [
                    line
                ]

            else:

                current_unit.append(
                    line
                )

        if current_unit:

            structural_units.append(
                "\n".join(
                    current_unit
                )
            )

        split_units = []

        for unit in structural_units:

            split_units.extend(
                self._recursive_split(
                    unit,
                    body_max_tokens
                )
            )

        body_chunks = []
        current_parts = []

        for unit in split_units:

            candidate = "\n".join(
                current_parts
                + [unit]
            )

            if self._count_tokens(candidate) <= body_max_tokens:

                current_parts.append(
                    unit
                )

                continue

            if current_parts:

                body_chunks.append(
                    "\n".join(
                        current_parts
                    )
                )

            current_parts = [
                unit
            ]

        if current_parts:

            body_chunks.append(
                "\n".join(
                    current_parts
                )
            )

        # 마지막 조각이 너무 짧고 바로 앞 조각과 합쳐도 최대치를 넘지 않으면 합칩니다.
        # 구조 보존을 우선하므로 합칠 수 없는 짧은 조각은 그대로 둡니다.
        if len(body_chunks) >= 2:

            last_chunk = body_chunks[-1]
            previous_chunk = body_chunks[-2]

            if self._count_tokens(last_chunk) < body_min_tokens:

                combined = (
                    previous_chunk
                    + "\n"
                    + last_chunk
                )

                if self._count_tokens(combined) <= body_max_tokens:

                    body_chunks[-2] = combined
                    body_chunks.pop()

        children = []

        for child_index, body_chunk in enumerate(
            body_chunks
        ):

            child_text = (
                f"{header}\n"
                f"{body_chunk}"
            )

            child_id = self._stable_id(
                parent["parent_id"],
                child_index,
                child_text
            )

            children.append({
                "child_id": child_id,
                "child_index": child_index,
                "content": child_text,
                "child_tokens": self._count_tokens(
                    child_text
                )
            })

        return children


    # ========================================================
    # TXT 파일 읽기
    # ========================================================

    def _read_text_file(
        self,
        file_path
    ):

        # 국가법령정보 데이터는 UTF-8 사용을 권장하지만,
        # 기존 테스트 파일이 CP949일 가능성도 있어 순서대로 시도합니다.
        encodings = [
            "utf-8-sig",
            "utf-8",
            "cp949"
        ]

        last_error = None

        for encoding in encodings:

            try:

                with open(
                    file_path,
                    "r",
                    encoding=encoding
                ) as f:

                    return f.read()

            except UnicodeDecodeError as e:

                last_error = e

        if last_error:

            raise last_error

        return ""


    # ========================================================
    # 정규화된 문서 적재
    # ========================================================

    def load_records(
        self,
        records,
        replace_sources=True
    ):

        """
        TXT와 국가법령정보 API가 공통으로 사용하는 적재 입구입니다.

        records의 각 dictionary 권장 형식:

        {
            "text": "법령 원문",
            "source": "파일명 또는 API 문서 ID",
            "law_name": "외국환거래법",
            "document_type": "law",
            "promulgation_number": "법률 제00000호",
            "effective_date": "2026-01-01",
            "revision_date": "2025-12-01",
            "source_url": "국가법령정보 원문 URL"
        }

        API 호출 파일은 XML/JSON 응답을 위 형식으로 정규화한 뒤
        이 함수에 넘기면 됩니다.
        """

        if not records:

            print(
                "적재할 법령 레코드가 없습니다."
            )

            return {
                "records": 0,
                "parents": 0,
                "children": 0
            }

        normalized_records = []

        for index, record in enumerate(
            records
        ):

            if not isinstance(
                record,
                dict
            ):

                raise TypeError(
                    f"records[{index}]는 dictionary여야 합니다."
                )

            text = self._normalize_text(
                record.get(
                    "text",
                    ""
                )
            )

            if not text:

                print(
                    f"빈 문서를 건너뜁니다: records[{index}]"
                )

                continue

            source = str(
                record.get(
                    "source",
                    f"record_{index}"
                )
            )

            metadata = dict(
                record
            )

            metadata.pop(
                "text",
                None
            )

            metadata["source"] = source

            if not metadata.get(
                "law_name"
            ):

                metadata["law_name"] = source

            normalized_records.append({
                "text": text,
                "metadata": metadata
            })

        if not normalized_records:

            return {
                "records": 0,
                "parents": 0,
                "children": 0
            }

        sources = sorted({
            item["metadata"]["source"]
            for item in normalized_records
        })

        if replace_sources:

            for source in sources:

                # 같은 출처를 다시 적재할 때 삭제 후 재생성하여
                # 개정으로 줄어든 조문에서 오래된 Child가 남는 문제를 막습니다.
                try:

                    self.collection.delete(
                        where={
                            "source": source
                        }
                    )

                except Exception:

                    # 해당 source가 아직 없으면 삭제할 항목도 없으므로 계속 진행합니다.
                    pass

            self.parents = {
                parent_id: parent
                for parent_id, parent in self.parents.items()
                if parent.get(
                    "source"
                ) not in sources
            }

        all_children = []
        new_parent_count = 0

        for item in normalized_records:

            document_metadata = item[
                "metadata"
            ]

            parents = self._build_parents(
                item["text"],
                document_metadata
            )

            for parent in parents:

                parent_id = parent[
                    "parent_id"
                ]

                self.parents[parent_id] = parent
                new_parent_count += 1

                children = self._build_children(
                    parent
                )

                child_count = len(
                    children
                )

                for child in children:

                    metadata = self._clean_metadata({
                        "source": parent["source"],
                        "law_name": parent["law_name"],
                        "document_type": parent["document_type"],
                        "chapter": parent["chapter"],
                        "section": parent["section"],
                        "article": parent["article"],
                        "article_title": parent["article_title"],
                        "parent_id": parent_id,
                        "parent_tokens": parent["parent_tokens"],
                        "parent_is_long": parent["parent_is_long"],
                        "child_index": child["child_index"],
                        "child_count": child_count,
                        "child_tokens": child["child_tokens"],
                        "effective_date": document_metadata.get(
                            "effective_date"
                        ),
                        "revision_date": document_metadata.get(
                            "revision_date"
                        ),
                        "promulgation_number": document_metadata.get(
                            "promulgation_number"
                        ),
                        "source_url": document_metadata.get(
                            "source_url"
                        )
                    })

                    all_children.append({
                        "id": child["child_id"],
                        "document": child["content"],
                        "metadata": metadata
                    })

        # 임베딩과 DB 저장을 batch로 나눠 메모리 사용량을 조절합니다.
        for start in range(
            0,
            len(all_children),
            self.embedding_batch_size
        ):

            batch = all_children[
                start:start + self.embedding_batch_size
            ]

            batch_documents = [
                item["document"]
                for item in batch
            ]

            batch_embeddings = self._embed_documents(
                batch_documents
            )

            self.collection.upsert(
                ids=[
                    item["id"]
                    for item in batch
                ],
                documents=batch_documents,
                embeddings=batch_embeddings.tolist(),
                metadatas=[
                    item["metadata"]
                    for item in batch
                ]
            )

        self._save_parent_store()

        result = {
            "records": len(
                normalized_records
            ),
            "parents": new_parent_count,
            "children": len(
                all_children
            )
        }

        print(
            f"{result['records']}개 문서에서 "
            f"Parent {result['parents']}개, "
            f"Child {result['children']}개를 저장했습니다."
        )

        return result


    # ========================================================
    # 테스트용 TXT 문서 로드
    # ========================================================

    def load_documents(
        self,
        directory=None
    ):

        # 기존 main.py와의 호환성을 위해 메서드 이름과 기본 경로를 유지합니다.
        # 국가법령정보 API가 연결된 뒤에도 이 함수는 개발·테스트에 사용할 수 있습니다.
        if directory is None:

            directory = os.path.join(
                self.base_dir,
                "data",
                "regulations"
            )

        if not os.path.isdir(
            directory
        ):

            print(
                f"RAG 문서 폴더가 없습니다:\n"
                f"{directory}"
            )

            return {
                "records": 0,
                "parents": 0,
                "children": 0
            }

        files = sorted(
            glob.glob(
                os.path.join(
                    directory,
                    "*.txt"
                )
            )
        )

        print(
            f"RAG 테스트 문서 파일: {len(files)}개"
        )

        records = []

        for file_path in files:

            try:

                text = self._read_text_file(
                    file_path
                )

            except Exception as e:

                print(
                    f"문서 읽기 실패: {file_path}"
                )

                print(e)

                continue

            file_name = os.path.basename(
                file_path
            )

            records.append({
                "text": text,
                "source": file_name,
                "law_name": os.path.splitext(
                    file_name
                )[0],
                "document_type": "test_txt"
            })

        return self.load_records(
            records,
            replace_sources=True
        )


    # ========================================================
    # 검색
    # ========================================================

    def search(
        self,
        query,
        n_results=5,
        where=None
    ):

        query = str(
            query
        ).strip()

        if not query:

            print(
                "검색어가 비어 있습니다."
            )

            return []

        count = self.collection.count()

        if count == 0:

            print(
                "RAG DB에 저장된 Child 문서가 없습니다."
            )

            return []

        n_results = max(
            1,
            min(
                n_results,
                count
            )
        )

        # 같은 Parent에 속한 Child가 여러 개 상위에 나올 수 있으므로
        # 최종 결과보다 넉넉한 후보를 검색한 뒤 Parent 기준으로 중복을 제거합니다.
        candidate_count = min(
            count,
            max(
                n_results * 4,
                n_results
            )
        )

        query_embedding = self._embed_query(
            query
        )

        query_arguments = {
            "query_embeddings": [
                query_embedding.tolist()
            ],
            "n_results": candidate_count,
            "include": [
                "documents",
                "metadatas",
                "distances"
            ]
        }

        # 예: where={"effective_date": "2026-01-01"}
        # API 데이터에 시행일 metadata가 들어오면 검색 범위를 제한할 수 있습니다.
        if where:

            query_arguments["where"] = where

        result = self.collection.query(
            **query_arguments
        )

        documents = result.get(
            "documents",
            [[]]
        )[0]

        metadatas = result.get(
            "metadatas",
            [[]]
        )[0]

        distances = result.get(
            "distances",
            [[]]
        )[0]

        formatted_documents = []
        seen_parent_ids = set()

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):

            metadata = (
                metadata
                if metadata
                else {}
            )

            parent_id = metadata.get(
                "parent_id",
                ""
            )

            if parent_id in seen_parent_ids:

                continue

            seen_parent_ids.add(
                parent_id
            )

            parent = self.parents.get(
                parent_id,
                {}
            )

            # Parent JSON이 없거나 손상된 경우에도 검색 결과를 완전히 버리지 않고
            # 일치한 Child 내용을 fallback으로 반환합니다.
            parent_content = parent.get(
                "content",
                document
            )

            formatted_documents.append({
                # 기존 report.py와 호환되는 필드입니다.
                "source": metadata.get(
                    "source",
                    "출처 없음"
                ),
                "chunk": metadata.get(
                    "child_index",
                    "-"
                ),
                "content": parent_content,

                # 아래 필드는 근거 추적과 향후 화면 표시를 위해 추가했습니다.
                "parent_id": parent_id,
                "article": metadata.get(
                    "article",
                    ""
                ),
                "article_title": metadata.get(
                    "article_title",
                    ""
                ),
                "effective_date": metadata.get(
                    "effective_date",
                    ""
                ),
                "source_url": metadata.get(
                    "source_url",
                    ""
                ),
                "matched_child": document,
                "distance": float(
                    distance
                )
            })

            if len(formatted_documents) >= n_results:

                break

        return formatted_documents
