from langchain_openai import ChatOpenAI

from mini_agent import GraphState, SourceType, get_sources

from .prompts import PLAN_COLLECTION_PROMPT
from .schema import CollectionPlan


def plan_collection(state: GraphState) -> GraphState:
    """수집 계획 생성 노드"""

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(
        CollectionPlan, method="function_calling"
    )

    plan_chain = PLAN_COLLECTION_PROMPT | llm

    # 피드백 섹션 준비
    feedback_section = _build_feedback_section(state)

    # 사용 가능한 소스 정보 가져오기
    available_sources = get_sources(state["tech"])

    # 가져온 소스 정보 -> 프롬프트용 문자열 변환
    sources_info = _format_available_sources(available_sources)

    current_attempt = state.get("attempt", 0)

    # LLM 호출
    result = plan_chain.invoke(
        {
            "tech": state["tech"],
            "today": state.get("today", ""),
            "attempt": current_attempt + 1,
            "max_attempts": state.get("max_attempts", 3),
            "feedback_section": feedback_section,
            "available_sources": sources_info,
        }
    )

    # attempt 증가 및 collection_plan 업데이트
    # Pydantic 모델을 dict로 변환
    plans_as_dicts = [plan.model_dump() for plan in result.plans]

    return GraphState(
        collection_plan=plans_as_dicts,
        attempt=current_attempt + 1,
    )


def _format_available_sources(sources: dict) -> str:
    """사용 가능한 소스 정보를 프롬프트용 문자열로 포맷팅"""
    lines = ["사용 가능한 소스 정보:"]

    github_repos = sources.get(SourceType.GITHUB_RELEASES, [])
    if github_repos:
        lines.append("\nGitHub Releases:")
        for repo in github_repos:
            lines.append(f"  - {repo}")

    rss_urls = sources.get(SourceType.RSS, [])
    if rss_urls:
        lines.append("\nRSS Feeds:")
        for url in rss_urls:
            lines.append(f"  - {url}")

    lines.append("\n웹 검색 (Tavily): 다른 소스로 충분하지 않을 경우에만 사용")

    return "\n".join(lines)


def _build_feedback_section(state: GraphState) -> str:
    """평가 피드백이 있으면 포맷팅, 없으면 기본 메시지"""
    evaluation = state.get("evaluation")

    if evaluation and evaluation.get("feedback"):
        return f"""평가자 피드백:
            {evaluation["feedback"]}

            위 피드백을 반영하여 수집 계획을 수정해주세요."""

    return "첫 번째 수집 시도입니다. 기본 소스(GitHub Releases, RSS)를 활용하세요."
