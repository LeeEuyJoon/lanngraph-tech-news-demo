"""GitHub Releases Source 플러그인 단위 테스트"""

from datetime import datetime

from dotenv import load_dotenv

from src import Tech
from src.sources.plugin.github_releases import GithubReleasesSource
from src.domain import SourceType

load_dotenv()


def test_github_releases_fetch_spring():
    """Spring GitHub Releases 가져오기 테스트"""
    source = GithubReleasesSource()
    today = datetime.now().strftime("%Y-%m-%d")

    result = source.fetch(tech=Tech.SPRING, today=today)

    # 결과 검증
    assert isinstance(result, list)
    assert len(result) > 0

    # 첫 번째 이벤트 검증
    first_event = result[0]
    assert first_event["source"] == SourceType.GITHUB_RELEASES
    assert "fetched_at" in first_event
    assert "payload" in first_event

    # Payload 검증
    payload = first_event["payload"]
    assert "repo" in payload

    # 성공적인 응답인 경우
    if "releases" in payload:
        releases = payload["releases"]
        assert isinstance(releases, list)
        print(f"레포지토리: {payload['repo']}")
        print(f"릴리즈 개수: {len(releases)}")
        if releases:
            print(f"최신 릴리즈: {releases[0].get('name', 'N/A')}")
    # 에러 응답인 경우
    elif "error" in payload:
        print(f"레포지토리: {payload['repo']}")
        print(f"상태 코드: {payload.get('status_code', 'N/A')}")
        print(f"에러: {payload['error'][:200]}")


def test_github_releases_fetch_nextjs():
    """Next.js GitHub Releases 가져오기 테스트"""
    source = GithubReleasesSource()
    today = datetime.now().strftime("%Y-%m-%d")

    result = source.fetch(tech=Tech.NEXTJS, today=today)

    assert isinstance(result, list)
    assert len(result) > 0

    print(f"\nNext.js GitHub Releases: {len(result)}개 레포지토리")


def test_github_releases_payload_structure():
    """GitHub Releases 이벤트의 payload 구조 상세 검증"""
    source = GithubReleasesSource()
    today = datetime.now().strftime("%Y-%m-%d")

    result = source.fetch(tech=Tech.REACT, today=today)

    # 성공 케이스 찾기
    success_event = None
    for event in result:
        if "releases" in event["payload"]:
            success_event = event
            break

    if success_event:
        payload = success_event["payload"]
        releases = payload["releases"]

        print("\n📦 GitHub Releases 구조:")
        print(f"  - 레포지토리: {payload['repo']}")
        print(f"  - 릴리즈 개수: {len(releases)}")

        if releases:
            latest = releases[0]
            print("\n🚀 최신 릴리즈:")
            print(f"  - Name: {latest.get('name', 'N/A')}")
            print(f"  - Tag: {latest.get('tag_name', 'N/A')}")
            print(f"  - Published: {latest.get('published_at', 'N/A')}")
            print(f"  - URL: {latest.get('html_url', 'N/A')}")

            # 모든 사용 가능한 키 출력
            print(f"\n  📋 Release 객체의 모든 키 ({len(latest.keys())}개):")
            for key in sorted(latest.keys()):
                value = latest[key]
                # 값이 너무 길면 축약
                if isinstance(value, str) and len(value) > 100:
                    print(f"      - {key}: {value[:100]}...")
                elif isinstance(value, list):
                    print(f"      - {key}: [리스트, {len(value)}개 항목]")
                elif isinstance(value, dict):
                    print(f"      - {key}: {{딕셔너리, {len(value)}개 키}}")
                else:
                    print(f"      - {key}: {value}")

            # Body 확인 (릴리즈 노트)
            if "body" in latest and latest["body"]:
                print("\n  📝 Release Body (릴리즈 노트):")
                print(f"  {latest['body'][:300]}...")

            assert "name" in latest or "tag_name" in latest
            assert "published_at" in latest
            assert "html_url" in latest
    else:
        print("\n⚠️ 모든 요청이 실패했습니다. GitHub API 상태를 확인하세요.")
