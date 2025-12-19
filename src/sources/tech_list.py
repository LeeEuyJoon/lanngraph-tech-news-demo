from enum import Enum


class Tech(str, Enum):
    """지원하는 기술 목록"""

    # Backend Frameworks
    SPRING = "spring"
    DJANGO = "django"
    FASTAPI = "fastapi"
    NESTJS = "nestjs"

    # Frontend Frameworks
    REACT = "react"
    NEXTJS = "nextjs"
    VUE = "vue"
    ANGULAR = "angular"
    SVELTE = "svelte"

    # Programming Languages
    PYTHON = "python"
    RUST = "rust"
    GOLANG = "golang"
    NODEJS = "nodejs"
    TYPESCRIPT = "typescript"

    # AI/ML
    LANGCHAIN = "langchain"
    TENSORFLOW = "tensorflow"
    PYTORCH = "pytorch"

    # DevOps/Infrastructure
    KUBERNETES = "kubernetes"
    DOCKER = "docker"

    # CSS
    TAILWINDCSS = "tailwindcss"
