from typing import Dict, Iterable, List, Optional, Protocol

from mini_agent import Tech
from mini_agent.state.sub_state import RawEvent


class SourcePlugin(Protocol):
    """
    소스 플러그인이 반드시 지켜야 하는 최소 계약(인터페이스).
    새 소스를 추가할 때 계약에 맞춰서 구현.
    """

    key: str

    def fetch(self, *, tech: Tech, config: dict) -> List[RawEvent]: ...


class SourceRegistry:
    def __init__(self) -> None:
        self._plugins: Dict[str, SourcePlugin] = {}

    def register(self, plugin: SourcePlugin) -> None:
        key = getattr(plugin, "key", None)
        if not key or not isinstance(key, str):
            raise ValueError("Plugin must have a valid 'key' attribute of type str.")

        if key in self._plugins:
            raise ValueError(f"Plugin with key '{key}' is already registered.")

        self._plugins[key] = plugin

    def get(self, key: str) -> Optional[SourcePlugin]:
        return self._plugins.get(key)

    def keys(self) -> List[str]:
        return sorted(self._plugins.keys())

    def fetch(
        self, *, source: str, tech: Tech, today: str, config: dict
    ) -> List[RawEvent]:
        plugin = self.get(source)
        if not plugin:
            raise ValueError(f"Unknown source: {source}. Available: {self.keys()}")

        return plugin.fetch(tech=tech, today=today, config=config)


def build_default_registry(plugins: Iterable[SourcePlugin]) -> SourceRegistry:
    """
    앱 시작 시점에 기본 플로그인들을 모아 registry를 구성할 때 사용.
    """
    reg = SourceRegistry()
    for p in plugins:
        reg.register(p)
    return reg
