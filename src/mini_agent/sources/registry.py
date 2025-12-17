from typing import Dict, Iterable, List, Optional, Protocol, Union

from mini_agent import Tech
from mini_agent.state.sub_state import RawEvent
from mini_agent.types import SourceType


class SourcePlugin(Protocol):
    """기본 소스 플러그인 (RSS, GitHub Releases 등)"""

    key: SourceType

    def fetch(self, *, tech: Tech, today: str) -> List[RawEvent]: ...


class SearchSourcePlugin(Protocol):
    """검색 소스 플러그인 (Tavily 등)"""

    key: SourceType

    def search(self, *, tech: Tech, today: str, query: str) -> List[RawEvent]: ...


class SourceRegistry:
    def __init__(self) -> None:
        self._plugins: Dict[SourceType, SourcePlugin] = {}
        self._search_plugins: Dict[SourceType, SearchSourcePlugin] = {}

    def register(self, plugin: Union[SourcePlugin, SearchSourcePlugin]) -> None:
        key = getattr(plugin, "key", None)
        if not key or not isinstance(key, SourceType):
            raise ValueError("Plugin must have a valid 'key' attribute of type SourceType.")

        # SearchSourcePlugin인지 확인 (search 메서드가 있는지)
        if hasattr(plugin, "search") and callable(getattr(plugin, "search")):
            if key in self._search_plugins:
                raise ValueError(f"Search plugin with key '{key}' is already registered.")
            self._search_plugins[key] = plugin  # type: ignore
        else:
            if key in self._plugins:
                raise ValueError(f"Plugin with key '{key}' is already registered.")
            self._plugins[key] = plugin  # type: ignore

    def get(self, key: SourceType) -> Optional[SourcePlugin]:
        return self._plugins.get(key)

    def get_search(self, key: SourceType) -> Optional[SearchSourcePlugin]:
        return self._search_plugins.get(key)

    def keys(self) -> List[SourceType]:
        all_keys = set(self._plugins.keys()) | set(self._search_plugins.keys())
        return sorted(all_keys, key=lambda x: x.value)

    def fetch(self, *, source: SourceType, tech: Tech, today: str) -> List[RawEvent]:
        """기본 소스에서 데이터 가져오기 (RSS, GitHub 등)"""
        plugin = self.get(source)
        if not plugin:
            raise ValueError(
                f"Unknown basic source: {source}. Available: {list(self._plugins.keys())}"
            )
        return plugin.fetch(tech=tech, today=today)

    def search(
        self, *, source: SourceType, tech: Tech, today: str, query: str
    ) -> List[RawEvent]:
        """검색 소스에서 데이터 가져오기 (Tavily 등)"""
        plugin = self.get_search(source)
        if not plugin:
            raise ValueError(
                f"Unknown search source: {source}. Available: {list(self._search_plugins.keys())}"
            )
        return plugin.search(tech=tech, today=today, query=query)


def build_default_registry(
    plugins: Iterable[Union[SourcePlugin, SearchSourcePlugin]]
) -> SourceRegistry:
    reg = SourceRegistry()
    for p in plugins:
        reg.register(p)
    return reg
