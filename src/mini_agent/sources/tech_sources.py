"""기술별 GitHub Releases 및 RSS Feed 소스 정보"""

from ..types import SourceType
from .tech_list import Tech

TECH_SOURCES = {
    Tech.SPRING: {
        SourceType.GITHUB_RELEASES: [
            "spring-projects/spring-boot",
            "spring-projects/spring-framework",
            "spring-cloud/spring-cloud-release",
        ],
        SourceType.RSS: ["https://spring.io/blog.atom"],
    },
    Tech.NEXTJS: {
        SourceType.GITHUB_RELEASES: ["vercel/next.js"],
        SourceType.RSS: ["https://nextjs.org/feed.xml"],
    },
    Tech.REACT: {
        SourceType.GITHUB_RELEASES: ["facebook/react"],
        SourceType.RSS: ["https://react.dev/rss.xml"],
    },
    Tech.VUE: {
        SourceType.GITHUB_RELEASES: ["vuejs/core"],
        SourceType.RSS: ["https://blog.vuejs.org/feed.rss"],
    },
    Tech.KUBERNETES: {
        SourceType.GITHUB_RELEASES: ["kubernetes/kubernetes"],
        SourceType.RSS: ["https://kubernetes.io/feed.xml"],
    },
    Tech.DOCKER: {
        SourceType.GITHUB_RELEASES: ["docker/docker-ce", "moby/moby"],
        SourceType.RSS: ["https://www.docker.com/blog/feed/"],
    },
    Tech.PYTHON: {
        SourceType.GITHUB_RELEASES: ["python/cpython"],
        SourceType.RSS: ["https://www.python.org/dev/peps/peps.rss/"],
    },
    Tech.DJANGO: {
        SourceType.GITHUB_RELEASES: ["django/django"],
        SourceType.RSS: ["https://www.djangoproject.com/rss/weblog/"],
    },
    Tech.FASTAPI: {
        SourceType.GITHUB_RELEASES: ["tiangolo/fastapi"],
        SourceType.RSS: [],
    },
    Tech.LANGCHAIN: {
        SourceType.GITHUB_RELEASES: [
            "langchain-ai/langchain",
            "langchain-ai/langgraph",
        ],
        SourceType.RSS: ["https://blog.langchain.dev/rss/"],
    },
    Tech.TENSORFLOW: {
        SourceType.GITHUB_RELEASES: ["tensorflow/tensorflow"],
        SourceType.RSS: ["https://blog.tensorflow.org/feeds/posts/default"],
    },
    Tech.PYTORCH: {
        SourceType.GITHUB_RELEASES: ["pytorch/pytorch"],
        SourceType.RSS: ["https://pytorch.org/blog/feed.xml"],
    },
    Tech.RUST: {
        SourceType.GITHUB_RELEASES: ["rust-lang/rust"],
        SourceType.RSS: ["https://blog.rust-lang.org/feed.xml"],
    },
    Tech.GOLANG: {
        SourceType.GITHUB_RELEASES: ["golang/go"],
        SourceType.RSS: ["https://go.dev/blog/feed.atom"],
    },
    Tech.NODEJS: {
        SourceType.GITHUB_RELEASES: ["nodejs/node"],
        SourceType.RSS: ["https://nodejs.org/en/feed/blog.xml"],
    },
    Tech.TYPESCRIPT: {
        SourceType.GITHUB_RELEASES: ["microsoft/TypeScript"],
        SourceType.RSS: [],
    },
    Tech.ANGULAR: {
        SourceType.GITHUB_RELEASES: ["angular/angular"],
        SourceType.RSS: ["https://blog.angular.io/feed"],
    },
    Tech.NESTJS: {
        SourceType.GITHUB_RELEASES: ["nestjs/nest"],
        SourceType.RSS: [],
    },
    Tech.SVELTE: {
        SourceType.GITHUB_RELEASES: ["sveltejs/svelte"],
        SourceType.RSS: ["https://svelte.dev/blog/rss.xml"],
    },
    Tech.TAILWINDCSS: {
        SourceType.GITHUB_RELEASES: ["tailwindlabs/tailwindcss"],
        SourceType.RSS: ["https://tailwindcss.com/feeds/feed.xml"],
    },
}


def get_sources(topic: Tech) -> dict:
    """
    기술명으로 소스 정보 조회

    Args:
        topic: Tech Enum

    Returns:
        {SourceType.GITHUB_RELEASES: [...], SourceType.RSS: [...]} 형태의 dict
        없으면 빈 리스트들 반환
    """
    return TECH_SOURCES.get(
        topic,
        {
            SourceType.GITHUB_RELEASES: [],
            SourceType.RSS: [],
        },
    )
