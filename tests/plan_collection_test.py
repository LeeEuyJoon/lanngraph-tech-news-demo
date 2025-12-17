from datetime import datetime

from dotenv import load_dotenv

from mini_agent import GraphState, Tech
from mini_agent.node.plan_collection import plan_collection

load_dotenv()


def test_plan_collection_node():
    print("test_plan_collection_node 실행")
    initial_state = GraphState(
        tech=Tech.SPRING,
        attempt=0,
        max_attempts=3,
        today=datetime.now().strftime("%Y-%m-%d"),
    )

    result = plan_collection(initial_state)

    print("Collection Plan 결과:")
    for idx, plan in enumerate(result["collection_plan"]):
        print(f"Plan {idx + 1}: {plan}")


def test_plan_collection_node_with_feedback():
    """평가자 피드백을 반영한 재계획 테스트"""
    print("test_plan_collection_node_with_feedback 실행")

    # 첫 번째 시도에서 수집한 이벤트들이 있다고 가정
    initial_state = GraphState(
        tech=Tech.NEXTJS,
        attempt=1,
        max_attempts=3,
        today=datetime.now().strftime("%Y-%m-%d"),
        # 이미 수집된 이벤트들 (첫 시도 결과)
        events=[
            {
                "source": "github_releases",
                "title": "Next.js 15.1.0 Released",
                "url": "https://github.com/vercel/next.js/releases/tag/v15.1.0",
                "published_at": "2025-12-10T00:00:00Z",
                "content": "Bug fixes and performance improvements",
            },
        ],
        # 평가자가 준 피드백
        evaluation={
            "pass_": False,
            "feedback": "릴리즈 정보는 있지만 블로그 포스트나 커뮤니티 논의가 부족합니다. 더 다양한 출처에서 정보를 수집해주세요.",
        },
    )

    result = plan_collection(initial_state)

    print("\n=== Collection Plan 결과 (피드백 반영) ===")
    print(f"Attempt: {result.get('attempt')}")
    print(f"\n계획된 수집 소스 ({len(result['collection_plan'])}개):")
    for idx, plan in enumerate(result["collection_plan"]):
        print(f"\nPlan {idx + 1}:")
        print(f"  Source: {plan.get('source')}")
        if plan.get("rss_urls"):
            print(f"  RSS URLs: {plan['rss_urls']}")
        if plan.get("github_repos"):
            print(f"  GitHub Repos: {plan['github_repos']}")
        if plan.get("web_search_queries"):
            print(f"  Search Queries: {plan['web_search_queries']}")


if __name__ == "__main__":
    test_plan_collection_node()
