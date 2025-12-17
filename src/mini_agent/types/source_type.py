from enum import Enum


class SourceType(str, Enum):
    """정보 수집 소스 타입"""

    GITHUB_RELEASES = "github_releases"
    RSS = "rss"
    TAVILY = "tavily"
