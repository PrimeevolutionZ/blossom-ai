"""
Blossom AI - Streaming Mixins
"""

import time
import asyncio
import json
from typing import Iterator, AsyncIterator, Optional
from abc import ABC, abstractmethod

import requests
import aiohttp

from blossom_ai.core.config import LIMITS
from blossom_ai.core.errors import StreamError, print_debug


# ============================================================================
# SSE PARSER (Unified for V1 and V2)
# ============================================================================

class SSEParser:
    """Parse Server-Sent Events (SSE) streams"""

    @staticmethod
    def parse_line(line: str) -> Optional[dict]:
        """
        Parse single SSE line

        Returns:
            dict with parsed data or None if invalid
        """
        if not line or not line.strip():
            return None

        if line.startswith('data: '):
            data_str = line[6:].strip()

            # Handle [DONE] marker
            if data_str == '[DONE]':
                return {'done': True}

            # Parse JSON
            try:
                return json.loads(data_str)
            except json.JSONDecodeError as e:
                print_debug(f"Invalid SSE JSON: {data_str[:100]} | Error: {e}")
                return None

        return None

    @staticmethod
    def extract_content(parsed_data: dict) -> Optional[str]:
        """
        Extract content from parsed SSE data (OpenAI format)

        Args:
            parsed_data: Parsed JSON object

        Returns:
            Extracted text content or None
        """
        if not parsed_data or parsed_data.get('done'):
            return None

        # OpenAI chat completion format
        if 'choices' in parsed_data and len(parsed_data['choices']) > 0:
            delta = parsed_data['choices'][0].get('delta', {})
            return delta.get('content', '')

        return None


# ============================================================================
# SYNC STREAMING MIXIN
# ============================================================================

class SyncStreamingMixin(ABC):
    """Mixin for synchronous streaming support"""

    def _stream_with_timeout(
            self,
            response: requests.Response,
            chunk_timeout: Optional[int] = None
    ) -> Iterator[str]:
        """
        Stream response lines with timeout between chunks

        Args:
            response: requests.Response object
            chunk_timeout: Timeout in seconds between chunks

        Yields:
            str: Individual lines from stream

        Raises:
            StreamError: On timeout or stream error
        """
        if chunk_timeout is None:
            chunk_timeout = LIMITS.STREAM_CHUNK_TIMEOUT

        last_data_time = time.time()

        try:
            for line in response.iter_lines(decode_unicode=True, chunk_size=1024):
                current_time = time.time()

                # Check timeout
                if current_time - last_data_time > chunk_timeout:
                    raise StreamError(
                        message=f"Stream timeout: no data received for {chunk_timeout}s",
                        suggestion="Check your connection or increase timeout"
                    )

                if line:
                    last_data_time = current_time
                    yield line

        finally:
            # Always close response
            if response and not response.raw.closed:
                try:
                    response.close()
                except Exception:
                    pass

    def _stream_sse_response(
            self,
            response: requests.Response,
            parser: SSEParser = None
    ) -> Iterator[str]:
        """
        Stream SSE response and extract content

        Args:
            response: requests.Response with SSE stream
            parser: SSEParser instance (uses default if None)

        Yields:
            str: Extracted content from SSE events

        Raises:
            StreamError: On stream errors
        """
        if parser is None:
            parser = SSEParser()

        try:
            for line in self._stream_with_timeout(response):
                parsed = parser.parse_line(line)

                if parsed is None:
                    continue

                if parsed.get('done'):
                    break

                content = parser.extract_content(parsed)
                if content:
                    yield content

        except StreamError:
            raise
        except Exception as e:
            raise StreamError(
                message=f"Error during streaming: {str(e)}",
                suggestion="Try non-streaming mode or check your connection",
                original_error=e
            )
        finally:
            if response and hasattr(response, 'close'):
                try:
                    response.close()
                except Exception:
                    pass

    def _stream_sse_chunked(
            self,
            response: requests.Response,
            parser: SSEParser = None
    ) -> Iterator[str]:
        """
        Stream SSE with chunk-based reading (better for V2 API)

        Args:
            response: requests.Response with SSE stream
            parser: SSEParser instance

        Yields:
            str: Extracted content
        """
        if parser is None:
            parser = SSEParser()

        buffer = ""
        last_data_time = time.time()

        try:
            for chunk in response.iter_content(chunk_size=None, decode_unicode=False):
                current_time = time.time()

                # Timeout check
                if current_time - last_data_time > LIMITS.STREAM_CHUNK_TIMEOUT:
                    raise StreamError(
                        message=f"Stream timeout: no data for {LIMITS.STREAM_CHUNK_TIMEOUT}s",
                        suggestion="Check connection or increase timeout"
                    )

                if not chunk:
                    continue

                last_data_time = current_time

                # Decode chunk
                try:
                    chunk_str = chunk.decode('utf-8')
                except UnicodeDecodeError:
                    chunk_str = chunk.decode('utf-8', errors='ignore')

                buffer += chunk_str

                # Process complete lines
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.strip()

                    if not line:
                        continue

                    parsed = parser.parse_line(line)
                    if parsed is None:
                        continue

                    if parsed.get('done'):
                        return

                    content = parser.extract_content(parsed)
                    if content:
                        yield content

        except StreamError:
            raise
        except Exception as e:
            raise StreamError(
                message=f"Error during streaming: {str(e)}",
                suggestion="Try non-streaming mode or check your connection",
                original_error=e
            )
        finally:
            if response and hasattr(response, 'close'):
                try:
                    response.close()
                except Exception:
                    pass


# ============================================================================
# ASYNC STREAMING MIXIN
# ============================================================================

class AsyncStreamingMixin(ABC):
    """Mixin for asynchronous streaming support"""

    async def _stream_sse_response(
            self,
            response: aiohttp.ClientResponse,
            parser: SSEParser = None
    ) -> AsyncIterator[str]:
        """
        Async stream SSE response and extract content

        Args:
            response: aiohttp.ClientResponse with SSE stream
            parser: SSEParser instance

        Yields:
            str: Extracted content from SSE events

        Raises:
            StreamError: On stream errors
        """
        if parser is None:
            parser = SSEParser()

        last_data_time = asyncio.get_event_loop().time()

        try:
            async for line in response.content:
                current_time = asyncio.get_event_loop().time()

                # Timeout check
                if current_time - last_data_time > LIMITS.STREAM_CHUNK_TIMEOUT:
                    raise StreamError(
                        message=f"Stream timeout: no data for {LIMITS.STREAM_CHUNK_TIMEOUT}s",
                        suggestion="Check connection or increase timeout"
                    )

                line_str = line.decode('utf-8', errors='ignore').strip()

                if not line_str:
                    continue

                last_data_time = current_time

                parsed = parser.parse_line(line_str)
                if parsed is None:
                    continue

                if parsed.get('done'):
                    break

                content = parser.extract_content(parsed)
                if content:
                    yield content

        except StreamError:
            raise
        except Exception as e:
            raise StreamError(
                message=f"Error during async streaming: {str(e)}",
                suggestion="Try non-streaming mode or check your connection",
                original_error=e
            )
        finally:
            if response and not response.closed:
                try:
                    await response.close()
                except Exception:
                    pass

    async def _stream_sse_chunked(
            self,
            response: aiohttp.ClientResponse,
            parser: SSEParser = None
    ) -> AsyncIterator[str]:
        """
        Async stream with chunk-based buffering (better for V2 API)

        Args:
            response: aiohttp.ClientResponse
            parser: SSEParser instance

        Yields:
            str: Extracted content
        """
        if parser is None:
            parser = SSEParser()

        buffer = ""
        last_data_time = asyncio.get_event_loop().time()

        try:
            async for chunk in response.content.iter_any():
                # Check if task was cancelled (Ctrl-C)
                if asyncio.current_task().cancelled():
                    print_debug("Stream cancelled by user")
                    break

                current_time = asyncio.get_event_loop().time()

                if current_time - last_data_time > LIMITS.STREAM_CHUNK_TIMEOUT:
                    raise StreamError(
                        message=f"Stream timeout: no data for {LIMITS.STREAM_CHUNK_TIMEOUT}s",
                        suggestion="Check connection or increase timeout"
                    )

                if not chunk:
                    continue

                last_data_time = current_time

                # Decode chunk
                try:
                    chunk_str = chunk.decode('utf-8')
                except UnicodeDecodeError:
                    chunk_str = chunk.decode('utf-8', errors='ignore')

                buffer += chunk_str

                # Process complete lines
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.strip()

                    if not line:
                        continue

                    parsed = parser.parse_line(line)
                    if parsed is None:
                        continue

                    if parsed.get('done'):
                        return

                    content = parser.extract_content(parsed)
                    if content:
                        yield content

        except asyncio.CancelledError:
            print_debug("Stream cancelled via CancelledError")
            raise
        except StreamError:
            raise
        except Exception as e:
            raise StreamError(
                message=f"Error during async streaming: {str(e)}",
                suggestion="Try non-streaming mode or check your connection",
                original_error=e
            )
        finally:
            if response and not response.closed:
                try:
                    await response.close()
                except Exception:
                    pass