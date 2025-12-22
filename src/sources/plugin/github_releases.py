import os
from datetime import datetime, timezone
from typing import List, Optional

import requests  # type: ignore

from src import Tech
from src.domain import SourceType
from src.sources import get_sources
from src.state.sub_state import RawEvent


class GithubReleasesSource:
    key = SourceType.GITHUB_RELEASES

    def fetch(self, *, tech: Tech, today: str) -> List[RawEvent]:
        # tech_sources.py에서 GitHub 레포 정보 가져오기
        sources = get_sources(tech)
        repos = sources.get(SourceType.GITHUB_RELEASES, [])

        if not repos:
            return []

        token: Optional[str] = os.getenv("GITHUB_TOKEN")
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "mini-agent",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"

        fetched_at = datetime.now(timezone.utc).isoformat()
        out: List[RawEvent] = []

        # 레포당 최대 5개의 릴리즈 가져오기
        per_repo_limit = 5

        for repo in repos:
            url = f"https://api.github.com/repos/{repo}/releases?per_page={per_repo_limit}"
            r = requests.get(url, headers=headers, timeout=20)
            if r.status_code != 200:
                out.append(
                    RawEvent(
                        source=self.key,
                        fetched_at=fetched_at,
                        payload={
                            "repo": repo,
                            "status_code": r.status_code,
                            "error": r.text[:1000],
                        },
                    )
                )
                continue

            # 필요한 필드만 추출하여 payload 크기 최소화
            releases = r.json()
            simplified_releases = [
                {
                    "tag_name": rel.get("tag_name"),
                    "name": rel.get("name"),
                    "html_url": rel.get("html_url"),
                    "published_at": rel.get("published_at"),
                    "prerelease": rel.get("prerelease", False),
                    "body": rel.get("body", ""),
                }
                for rel in releases
            ]

            out.append(
                RawEvent(
                    source=self.key,
                    fetched_at=fetched_at,
                    payload={"repo": repo, "releases": simplified_releases},
                )
            )

        return out
