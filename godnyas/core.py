from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Any, Protocol, Sequence


class Part(Protocol):
    def invoke(self, task: Any) -> Any: ...


class Composer(Protocol):
    def compose(self, task: Any, *, parts: Sequence[Part]) -> Any: ...


@dataclass(frozen=True)
class Receipt:
    part_count: int
    latency_ms: float


@dataclass(frozen=True)
class GodNyasResult:
    value: Any
    receipt: Receipt


class GodNyasSet:
    """Minimal public composition shell.

    Part identities, roles, and production topology are intentionally opaque.
    This class is a reference contract, not the production architecture.
    """

    def __init__(self, *, parts: Sequence[Part], composer: Composer):
        self.parts = tuple(parts)
        self.composer = composer

    def run(self, task: Any) -> GodNyasResult:
        started = perf_counter()
        value = self.composer.compose(task, parts=self.parts)
        return GodNyasResult(
            value=value,
            receipt=Receipt(
                part_count=len(self.parts),
                latency_ms=(perf_counter() - started) * 1000,
            ),
        )
