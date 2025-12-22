"""Tavily Source 플러그인 단위 테스트"""

import os
from datetime import datetime

import pytest
from dotenv import load_dotenv

from src import Tech
from src.domain import SourceType
from src.sources.plugin.tavily import TavilySource

load_dotenv()


def test_tavily_search_spring():
    """Spring 관련 뉴스 검색 테스트

    pytest tests/unit/sources/test_tavily_source.py -s -v
    """
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

    # results는 리스트
    assert isinstance(results, list), "results가 리스트여야 합니다"
    print(f"검색 결과 개수: {len(results)}")

    if results:
        first_result = results[0]
        print("\n🔍 첫 번째 검색 결과:")
        print(f"  - Title: {first_result.get('title', 'N/A')}")
        print(f"  - URL: {first_result.get('url', 'N/A')}")
        print(f"  - Content: {first_result.get('content', 'N/A')[:100]}...")
        print(f"  - Published: {first_result.get('published_date', 'N/A')}")


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

    # results는 리스트
    assert isinstance(results, list), "results는 리스트여야 합니다"
    print(f"\n📄 검색 결과: {len(results)}개")

    for i, search_result in enumerate(results[:3], 1):
        print(f"\n  [{i}] {search_result.get('title', 'N/A')}")
        print(f"      URL: {search_result.get('url', 'N/A')}")
        print(f"      Published: {search_result.get('published_date', 'N/A')}")

        # 필수 필드만 있는지 확인
        print(f"      📋 사용 가능한 키: {list(search_result.keys())}")

        # 필수 필드 검증
        assert "title" in search_result
        assert "url" in search_result
        assert "content" in search_result
        assert "published_date" in search_result

        # Content 확인 (AI가 추출한 요약)
        content = search_result.get("content", "")
        if content:
            print("      📄 Content (AI 추출 요약):")
            print(f"          {content[:200]}...")

        # 불필요한 필드가 제거되었는지 확인
        assert "score" not in search_result, "score는 제거되어야 합니다"
        assert "raw_content" not in search_result, "raw_content는 제거되어야 합니다"

    print("\n✅ 검증 완료: 필수 필드만 포함, 불필요한 필드 제거됨")
