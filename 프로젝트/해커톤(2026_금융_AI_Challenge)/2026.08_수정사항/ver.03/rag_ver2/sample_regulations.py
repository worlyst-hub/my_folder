"""RAG Mock 모드용 샘플 규정 데이터.

``data/regulations/`` 에 실제 국가법령정보센터 PDF가 없을 때 RAG 파이프라인
(Chunking → Embedding → Vector DB → 검색)을 그대로 시연하기 위한 예시
텍스트다.

중요:
    아래 조문 번호/본문은 실제 외국환거래법령을 그대로 전재한 것이 아니라
    프로토타입 시연을 위해 구성한 **샘플 데이터**다. 실제 업무에는
    국가법령정보센터의 최신 원문을 사용해야 한다. 화면에는 반드시
    "샘플 데이터"임을 표시한다.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SampleRegulation:
    law_name: str
    article: str
    content: str
    regulation_tags: list[str] = field(default_factory=list)


SAMPLE_FILE_NAME = "샘플_외국환거래규정_요약.md"

SAMPLE_REGULATIONS: list[SampleRegulation] = [
    SampleRegulation(
        law_name="외국환거래규정 (샘플)",
        article="제9-39조",
        content=(
            "거주자가 외국에 있는 부동산을 취득하는 경우에는 취득 전에 외국환은행의 장 "
            "또는 한국은행총재에게 신고하여야 한다. 신고 시 부동산 매매계약서, 자금출처를 "
            "확인할 수 있는 서류 등을 제출하는 것을 원칙으로 한다."
        ),
        regulation_tags=["REAL_ESTATE", "CAPITAL_TRANSACTION"],
    ),
    SampleRegulation(
        law_name="외국환거래규정 (샘플)",
        article="제9-5조",
        content=(
            "거주자가 해외직접투자를 하고자 하는 경우 지정거래외국환은행의 장에게 신고하여야 "
            "하며, 투자업종 및 투자금액에 따라 한국은행 신고 대상이 될 수 있다. 신고 시 사업계획서, "
            "투자 상대방과의 계약서 등을 제출한다."
        ),
        regulation_tags=["FDI", "CAPITAL_TRANSACTION"],
    ),
    SampleRegulation(
        law_name="외국환거래규정 (샘플)",
        article="제7-31조",
        content=(
            "거주자가 외국에서 발행된 증권을 취득하는 경우, 취득 목적 및 규모에 따라 신고 또는 "
            "보고 대상 여부를 확인하여야 한다. 투자중개업자를 통한 거래인 경우 관련 매매내역서 "
            "등을 보관하여야 한다."
        ),
        regulation_tags=["SECURITIES_INVESTMENT", "CAPITAL_TRANSACTION"],
    ),
    SampleRegulation(
        law_name="외국환거래규정 (샘플)",
        article="제7-16조",
        content=(
            "거주자와 비거주자 간 금전대차계약을 체결하는 경우 계약 당사자, 금액, 상환조건 등을 "
            "명시한 금전소비대차계약서를 근거로 신고 여부를 판단하여야 한다. 계열사간 대여의 경우 "
            "별도 유의사항을 함께 확인한다."
        ),
        regulation_tags=["LOAN", "CAPITAL_TRANSACTION"],
    ),
    SampleRegulation(
        law_name="외국환거래규정 (샘플)",
        article="제5-4조",
        content=(
            "물품의 수출입에 따른 대금의 지급 및 영수는 계약서, 신용장, 선하증권 등 무역서류에 "
            "근거하여 이루어져야 하며, 일정 금액 이상의 거래는 외국환은행을 통한 확인 절차를 "
            "거치는 것을 원칙으로 한다."
        ),
        regulation_tags=["TRADE", "CURRENT_TRANSACTION"],
    ),
    SampleRegulation(
        law_name="외국환거래규정 (샘플)",
        article="제4-5조",
        content=(
            "유학경비, 해외체재비 등 경상거래에 따른 대가의 지급은 재학증명서, 등록금 고지서 등 "
            "지급 목적을 확인할 수 있는 서류를 제출하는 것을 원칙으로 한다."
        ),
        regulation_tags=["STUDY_ABROAD", "CURRENT_TRANSACTION"],
    ),
    SampleRegulation(
        law_name="외국환거래규정 (샘플)",
        article="제4-6조",
        content=(
            "해외이주자가 국내 재산을 국외로 반출하고자 하는 경우 해외이주자임을 확인할 수 있는 "
            "서류와 반출 재산의 자금출처를 확인할 수 있는 서류를 제출하여야 한다."
        ),
        regulation_tags=["IMMIGRATION", "CAPITAL_TRANSACTION"],
    ),
    SampleRegulation(
        law_name="외국환거래규정 (샘플)",
        article="제5-11조",
        content=(
            "특허권, 상표권, 저작권 등 지식재산권의 사용대가를 지급하는 경우 라이선스 계약서 등 "
            "권리관계 및 대가산정 근거를 확인할 수 있는 서류를 제출하는 것을 원칙으로 한다."
        ),
        regulation_tags=["IP_ROYALTY", "CURRENT_TRANSACTION"],
    ),
]
