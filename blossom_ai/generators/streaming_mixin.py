"""
Blossom AI – Streaming Mixin (v0.5.4)
Single generic mixin for sync/async SSE parsing.
"""

from __future__ import annotations

import asyncio
import json
from abc import ABC
from typing import (
    AsyncIterator, Iterator, Iterable, AsyncIterable, Optional, Union, TypeVar,
)

from blossom_ai.core.config import LIMITS
from blossom_ai.core.errors import StreamError, print_debug

T = TypeVar("T", bound=Iterable[str] | AsyncIterable[bytes])

# --------------------------------------------------------------------------- #
# SSE parser
# --------------------------------------------------------------------------- #

class SSEParser:
    @staticmethod
    def parse_line(line: str) -> Optional[dict]:
        if not line or not line.strip():
            return None
        if line.startswith("data: "):
            data_str = line[6:].strip()
            if data_str == "[DONE]":
                return {"done": True}
            try:
                return json.loads(data_str)
            except json.JSONDecodeError as e:
                print_debug(f"Invalid SSE JSON: {data_str[:100]} | Error: {e}")
                return None
        return None

    @staticmethod
    def extract_content(parsed: dict) -> Optional[str]:
        if not parsed or parsed.get("done"):
            return None
        if "choices" in parsed and len(parsed["choices"]) > 0:
            return parsed["choices"][0].get("delta", {}).get("content", "")
        return None

# --------------------------------------------------------------------------- #
# Universal streaming mixin
# --------------------------------------------------------------------------- #

class StreamingMixin(ABC):
    def stream_sse(self, source: Iterator[str]) -> Iterator[str]:
        """Sync SSE stream."""
        for line in source:
            parsed = SSEParser.parse_line(line)
            if parsed is None:
                continue
            if parsed.get("done"):
                break
            content = SSEParser.extract_content(parsed)
            if content:
                yield content

    async def astream_sse(self, source: AsyncIterable[bytes]) -> AsyncIterator[str]:
        """Async SSE stream."""
        async for chunk in source:
            line = chunk.decode("utf-8", errors="ignore").strip()
            parsed = SSEParser.parse_line(line)
            if parsed is None:
                continue
            if parsed.get("done"):
                break
            content = SSEParser.extract_content(parsed)
            if content:
                yield content