import os
from datetime import datetime, timezone
from typing import List, Optional

import requests  # type: ignore

from src import Tech
from src.sources import get_sources
from src.state.sub_state import RawEvent
from src.domain import SourceType


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

            out.append(
                RawEvent(
                    source=self.key,
                    fetched_at=fetched_at,
                    payload={"repo": repo, "releases": r.json()},
                )
            )

        return out
