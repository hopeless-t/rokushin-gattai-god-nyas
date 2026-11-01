"""Toy demo of the opaque public composition contract.

The placeholder parts do not correspond to named production components.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from godnyas import GodNyasSet


class PlaceholderPart:
    def __init__(self, suffix: str):
        self.suffix = suffix

    def invoke(self, task):
        return f"{task}{self.suffix}"


class ToyComposer:
    def compose(self, task, *, parts):
        value = task
        for part in parts:
            value = part.invoke(value)
        return value


if __name__ == "__main__":
    system = GodNyasSet(
        parts=[PlaceholderPart("+nya"), PlaceholderPart("+nya")],
        composer=ToyComposer(),
    )
    result = system.run("0B")
    print(result.value)
    print(f"parts={result.receipt.part_count}")
