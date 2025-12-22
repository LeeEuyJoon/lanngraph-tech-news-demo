"""Normalize Events 노드의 프롬프트"""

from typing import List

from src.state.sub_state import RawEvent


def get_system_prompt() -> str:
    return """당신은 다양한 소스에서 수집된 원시 이벤트 데이터를 정규화하는 데이터 처리 전문가입니다.

            원시 이벤트들은 서로 다른 형식과 구조를 가지고 있으며, 이를 통일된 형식으로 변환하는 것이 당신의 임무입니다.

            각 이벤트는 다음과 같은 통일된 형식(NormalizedEvent)으로 변환되어야 합니다:
            - source: 이벤트 출처 (RSS, GITHUB_RELEASES, TAVILY 중 하나)
            - title: 이벤트 제목 (원본 제목 그대로)
            - url: 이벤트 링크 (원본 소스 URL)
            - published_at: 발행 날짜 (ISO 8601 형식: YYYY-MM-DD)
            - content: 이벤트 내용 (원본 내용 전체, HTML 태그만 제거)

            가이드라인:
            1. **제목(title)**: 원본 제목을 그대로 사용
            2. **URL**: 유효한 원본 링크, 없으면 빈 문자열
            3. **발행일(published_at)**: 정확한 날짜를 ISO 형식(YYYY-MM-DD)으로 변환, 없으면 오늘 날짜 사용
            4. **내용(content)**: 원본 내용을 최대한 보존, 요약하지 말고 전체 내용 포함, HTML 태그만 제거

            소스별 매핑:
            - **RSS**: content 또는 summary 필드 → content (전체 내용)
            - **GITHUB_RELEASES**: body 필드 → content (전체 내용)
            - **TAVILY**: content 필드 → content (AI 추출 요약, 그대로 사용)

            중요: 내용을 요약하거나 축약하지 마세요. 원본 정보를 최대한 보존하세요!"""


def get_user_prompt(raw_events: List[RawEvent]) -> str:
    events_info = []
    for idx, event in enumerate(raw_events, 1):
        source = event["source"]
        payload = event["payload"]
        events_info.append(f"{idx}. [{source}]\n{payload}\n")

    events_text = "\n".join(events_info)

    return f"""다음 {len(raw_events)}개의 원시 이벤트를 정규화된 형식으로 변환하세요:

            {events_text}

            각 이벤트를 NormalizedEvents 형식으로 변환하여 JSON 배열로 반환하세요.
            모든 이벤트가 정확하게 변환되도록 주의하세요."""
