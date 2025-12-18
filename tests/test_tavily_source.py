"""Tavily Source 플러그인 단위 테스트"""

import os
from datetime import datetime

import pytest
from dotenv import load_dotenv

from mini_agent import Tech
from mini_agent.sources.plugin.tavily import TavilySource
from mini_agent.types import SourceType

load_dotenv()


def test_tavily_search_spring():
    """Spring 관련 뉴스 검색 테스트"""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        pytest.skip("TAVILY_API_KEY가 설정되지 않았습니다")

    source = TavilySource()
    today = datetime.now().strftime("%Y-%m-%d")

    result = source.search(
        tech=Tech.SPRING, today=today, query="Spring Boot 3 latest updates"
    )

    # 결과 검증
    assert isinstance(result, list)
    assert len(result) == 1  # Tavily는 항상 1개의 RawEvent 반환

    # 첫 번째 이벤트 검증
    event = result[0]
    assert event["source"] == SourceType.TAVILY
    assert "fetched_at" in event
    assert "payload" in event

    # Payload 검증
    payload = event["payload"]
    assert "query" in payload
    assert payload["query"] == "Spring Boot 3 latest updates"
    assert "results" in payload

    # Results 검증
    results = payload["results"]
    print(f"쿼리: {payload['query']}")
    print(f"결과 타입: {type(results)}")

    # Tavily 결과 구조 확인
    if isinstance(results, dict):
        if "results" in results:
            search_results = results["results"]
            print(f"검색 결과 개수: {len(search_results)}")
            if search_results:
                first_result = search_results[0]
                print("\n🔍 첫 번째 검색 결과:")
                print(f"  - Title: {first_result.get('title', 'N/A')}")
                print(f"  - URL: {first_result.get('url', 'N/A')}")
                print(f"  - Content: {first_result.get('content', 'N/A')[:100]}...")


def test_tavily_search_different_queries():
    """다양한 쿼리로 검색 테스트"""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        pytest.skip("TAVILY_API_KEY가 설정되지 않았습니다")

    source = TavilySource()
    today = datetime.now().strftime("%Y-%m-%d")

    queries = [
        "Python 3.12 performance improvements",
        "React Server Components tutorial",
        "Docker security best practices",
    ]

    for query in queries:
        result = source.search(tech=Tech.PYTHON, today=today, query=query)

        assert len(result) == 1
        assert result[0]["payload"]["query"] == query

        print(f"쿼리: {query}")


def test_tavily_payload_structure():
    """Tavily 이벤트의 payload 구조 상세 검증"""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        pytest.skip("TAVILY_API_KEY가 설정되지 않았습니다")

    source = TavilySource()
    today = datetime.now().strftime("%Y-%m-%d")

    result = source.search(
        tech=Tech.LANGCHAIN, today=today, query="LangChain LangGraph updates 2025"
    )

    event = result[0]
    payload = event["payload"]
    results = payload["results"]

    print("\n🔍 Tavily 결과 구조:")
    print(f"  - Query: {payload['query']}")
    print(f"  - Results type: {type(results)}")

    if isinstance(results, dict):
        print(f"  - Keys: {list(results.keys())}")

        # Answer 확인 (include_answer=True로 요청)
        if "answer" in results:
            print("\n💡 AI Answer:")
            print(f"  {results['answer'][:200]}...")

        # Search results 확인
        if "results" in results:
            search_results = results["results"]
            print(f"\n📄 검색 결과: {len(search_results)}개")

            for i, result in enumerate(search_results[:3], 1):
                print(f"\n  [{i}] {result.get('title', 'N/A')}")
                print(f"      URL: {result.get('url', 'N/A')}")
                print(f"      Score: {result.get('score', 'N/A')}")

                # 각 검색 결과의 모든 키 확인
                print(f"      📋 사용 가능한 키: {list(result.keys())}")

                # Content 확인 (URL의 내용 요약)
                content = result.get("content", "")
                if content:
                    print("      📄 Content (내용 요약):")
                    print(f"          {content[:200]}...")
                raw_content = result.get("raw_content", "")
                if raw_content:
                    print("      📝 Raw Content (원문 일부):")
                    print(f"          {raw_content[:200]}...")
