"""Offline-first assistant boundary for Kinetics.

This module deliberately does not bundle or download a language model. A local
backend (for example, a separately deployed Kinetics Ecosystem runtime) is injected through the small
`AssistantBackend` protocol. Keeping this boundary dependency-free allows the
scientific package to remain usable without an AI runtime.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, Sequence


@dataclass(frozen=True)
class AssistantMessage:
    """A single message in a bounded assistant conversation."""

    role: str
    content: str

    def __post_init__(self) -> None:
        if self.role not in {"system", "user", "assistant"}:
            raise ValueError("role must be system, user, or assistant")
        if not self.content.strip():
            raise ValueError("message content must not be empty")


@dataclass(frozen=True)
class AssistantRequest:
    """Input passed to a local assistant backend."""

    messages: Sequence[AssistantMessage]
    project_context: str = ""
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class AssistantResponse:
    """Backend output plus explicit provenance about the generating runtime."""

    content: str
    backend_name: str
    model_name: str | None = None
    offline: bool = True
    warnings: tuple[str, ...] = ()


class AssistantBackend(Protocol):
    """Adapter contract implemented by an explicitly configured local runtime."""

    def generate(self, request: AssistantRequest) -> AssistantResponse:
        """Generate a response without requiring Kinetics to know model internals."""
        ...


class KineticsAssistant:
    """Small orchestration facade for research-aware assistant interactions.

    The caller owns the backend lifecycle, model files, conversation storage,
    and any permissions for filesystem or repository actions. This class only
    packages the research context and forwards a request to the injected
    backend. It never executes generated code or grants the model tool access.
    """

    def __init__(
        self,
        backend: AssistantBackend,
        *,
        project_context: str = "",
        require_offline: bool = True,
    ) -> None:
        self._backend = backend
        self._project_context = project_context
        self._require_offline = require_offline

    def ask(
        self,
        question: str,
        *,
        history: Sequence[AssistantMessage] = (),
        metadata: dict[str, str] | None = None,
    ) -> AssistantResponse:
        """Ask a question while preserving the research-use and evidence rules."""
        if not question.strip():
            raise ValueError("question must not be empty")

        system_message = AssistantMessage(
            role="system",
            content=(
                "You are the Kinetics research assistant. Distinguish measured "
                "observations from model predictions. Never invent dataset "
                "provenance, citations, experimental results, validation, or "
                "software execution. State uncertainty and missing evidence. "
                "Do not claim a model is scientifically validated merely because "
                "software runs. Treat Km and kcat as independent observations "
                "unless a source explicitly links the measurements and assay "
                "context. Do not execute code or take external actions."
            ),
        )
        request = AssistantRequest(
            messages=(system_message, *history, AssistantMessage("user", question)),
            project_context=self._project_context,
            metadata=dict(metadata or {}),
        )
        response = self._backend.generate(request)
        if not response.content.strip():
            raise RuntimeError("assistant backend returned an empty response")
        if self._require_offline and not response.offline:
            raise RuntimeError(
                "Kinetics is configured for offline assistant use, but the backend "
                "reported that it is not offline"
            )
        return response
