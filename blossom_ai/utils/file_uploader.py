"""
Blossom AI - File Content Reader Utility
Reads file content and validates it fits within API prompt limits
"""

import os
from pathlib import Path
from typing import Optional, Union, List
from dataclasses import dataclass

from blossom_ai.core.errors import ValidationError, FileTooLargeError

# ============================================================================
# CONFIGURATION
# ============================================================================

# API total limit (file + prompt combined)
# Updated: Increased from 10,000 to 90,000 characters (v0.5.0)
API_MAX_TOTAL_LENGTH = 90000

# Default max file content length (leaves space for prompt)
# Increased proportionally: 8,000 → 72,000 (80% of total)
DEFAULT_MAX_FILE_LENGTH = 72000

# Recommended prompt space reservation
# Increased proportionally: 2,000 → 18,000 (20% of total)
DEFAULT_PROMPT_SPACE = 18000

# Maximum file size to read (safety limit)
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

# Supported text file extensions
SUPPORTED_TEXT_EXTENSIONS = {
    '.txt', '.md', '.markdown', '.json', '.yaml', '.yml',
    '.csv', '.log', '.xml', '.html', '.css', '.js',
    '.py', '.java', '.cpp', '.c', '.h', '.go', '.rs',
    '.sh', '.bat', '.sql', '.conf', '.ini', '.env'
}

# Default encoding
DEFAULT_ENCODING = 'utf-8'


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class FileContent:
    """Container for file content with metadata"""
    content: str
    filename: str
    file_path: str
    char_count: int
    line_count: int
    encoding: str

    def __str__(self) -> str:
        return (
            f"File: {self.filename}\n"
            f"Characters: {self.char_count:,}\n"
            f"Lines: {self.line_count:,}\n"
            f"Encoding: {self.encoding}"
        )


# ============================================================================
# FILE READER
# ============================================================================

class FileContentReader:
    """
    Reads text file content and validates it fits within API limits

    IMPORTANT: The Pollinations API has a total limit of 90,000 characters
    for the combined prompt + file content. By default, this reader limits
    file content to 72,000 characters to leave space for your prompt.

    Example:
        reader = FileContentReader()
        content = reader.read_file("data.txt")  # Max 72,000 chars by default

        # Combine with prompt
        full_prompt = f"Analyze this file:\\n\\n{content.content}"
        # Total should be <= 90,000 characters
    """

    def __init__(
            self,
            max_file_length: int = DEFAULT_MAX_FILE_LENGTH,
            prompt_space: int = DEFAULT_PROMPT_SPACE,
            encoding: str = DEFAULT_ENCODING,
            fallback_encodings: Optional[List[str]] = None
    ):
        """
        Initialize file content reader

        Args:
            max_file_length: Maximum allowed file content length (default: 72,000)
            prompt_space: Space reserved for prompt text (default: 18,000)
            encoding: Default encoding to try first
            fallback_encodings: List of encodings to try if default fails
        """
        self.max_file_length = max_file_length
        self.prompt_space = prompt_space
        self.encoding = encoding
        self.fallback_encodings = fallback_encodings or ['utf-8', 'latin-1', 'cp1252']

        # Validate configuration
        if self.max_file_length + self.prompt_space > API_MAX_TOTAL_LENGTH:
            raise ValidationError(
                message=f"Configuration error: max_file_length ({max_file_length:,}) + prompt_space ({prompt_space:,}) exceeds API limit ({API_MAX_TOTAL_LENGTH:,})",
                suggestion=f"Reduce max_file_length or prompt_space so their sum is <= {API_MAX_TOTAL_LENGTH:,}"
            )

    def read_file(
            self,
            file_path: Union[str, Path],
            max_chars: Optional[int] = None,
            strip_whitespace: bool = True
    ) -> FileContent:
        """
        Read file content with automatic validation

        IMPORTANT: By default, this limits file content to 72,000 characters
        to leave space for your prompt (API total limit is 90,000 characters).

        Args:
            file_path: Path to text file
            max_chars: Optional custom limit (uses self.max_file_length if None)
            strip_whitespace: Whether to strip leading/trailing whitespace

        Returns:
            FileContent object with file data

        Raises:
            FileTooLargeError: If file exceeds the limit
            ValidationError: If file is invalid
        """
        path = self._validate_file_path(file_path)
        self._validate_file_size(path)
        self._validate_file_extension(path)

        content, used_encoding = self._read_with_encoding(path)

        if strip_whitespace:
            content = content.strip()

        char_count = len(content)
        line_count = content.count('\n') + 1 if content else 0

        # Validate length
        limit = max_chars or self.max_file_length
        if char_count > limit:
            raise FileTooLargeError(
                message=f"File content too large: {char_count:,} characters (limit: {limit:,})",
                suggestion=(
                    f"File '{path.name}' has {char_count:,} characters but the limit is {limit:,}.\n"
                    f"API total limit: {API_MAX_TOTAL_LENGTH:,} characters (file + prompt combined)\n"
                    f"Current file limit: {limit:,} characters (leaves {self.prompt_space:,} for prompt)\n\n"
                    f"Solutions:\n"
                    f"  1. Use read_file_truncated() to automatically truncate to {limit:,} chars\n"
                    f"  2. Split the file into smaller parts\n"
                    f"  3. Summarize the content first\n"
                    f"  4. Increase max_file_length (but remember: file + prompt <= {API_MAX_TOTAL_LENGTH:,})"
                )
            )

        return FileContent(
            content=content,
            filename=path.name,
            file_path=str(path),
            char_count=char_count,
            line_count=line_count,
            encoding=used_encoding
        )

    def read_file_truncated(
            self,
            file_path: Union[str, Path],
            max_chars: Optional[int] = None,
            add_truncation_note: bool = True
    ) -> FileContent:
        """
        Read file and truncate if necessary

        Args:
            file_path: Path to text file
            max_chars: Maximum characters to read (uses self.max_file_length if None)
            add_truncation_note: Add note if content was truncated

        Returns:
            FileContent with potentially truncated content
        """
        path = self._validate_file_path(file_path)
        self._validate_file_size(path)
        self._validate_file_extension(path)

        content, used_encoding = self._read_with_encoding(path)
        content = content.strip()

        limit = max_chars or self.max_file_length
        original_length = len(content)

        if original_length > limit:
            content = content[:limit]
            if add_truncation_note:
                content += f"\n\n[... truncated, showing {limit:,} of {original_length:,} characters ...]"

        char_count = len(content)
        line_count = content.count('\n') + 1 if content else 0

        return FileContent(
            content=content,
            filename=path.name,
            file_path=str(path),
            char_count=char_count,
            line_count=line_count,
            encoding=used_encoding
        )

    def read_multiple_files(
            self,
            file_paths: List[Union[str, Path]],
            separator: str = "\n\n---\n\n",
            max_total_chars: Optional[int] = None
    ) -> FileContent:
        """
        Read multiple files and combine them

        Args:
            file_paths: List of file paths
            separator: String to insert between files
            max_total_chars: Maximum total characters (uses self.max_file_length if None)

        Returns:
            Combined FileContent

        Raises:
            FileTooLargeError: If combined content exceeds limit
        """
        if not file_paths:
            raise ValidationError(
                message="No files provided",
                suggestion="Provide at least one file path"
            )

        contents = []
        total_chars = 0
        filenames = []

        limit = max_total_chars or self.max_file_length

        for file_path in file_paths:
            # Read each file without the automatic limit check
            path = self._validate_file_path(file_path)
            self._validate_file_size(path)
            self._validate_file_extension(path)

            content, encoding = self._read_with_encoding(path)
            content = content.strip()

            file_content = FileContent(
                content=content,
                filename=path.name,
                file_path=str(path),
                char_count=len(content),
                line_count=content.count('\n') + 1,
                encoding=encoding
            )

            header = f"=== {file_content.filename} ===\n"
            section = header + file_content.content

            total_chars += len(section)
            if len(contents) > 0:
                total_chars += len(separator)

            if total_chars > limit:
                raise FileTooLargeError(
                    message=f"Combined files too large: {total_chars:,} characters (limit: {limit:,})",
                    suggestion=(
                        f"Combined files exceed {limit:,} characters.\n"
                        f"Processed {len(contents)} of {len(file_paths)} files.\n"
                        f"API total limit: {API_MAX_TOTAL_LENGTH:,} characters (file + prompt combined)\n\n"
                        f"Solutions:\n"
                        f"  1. Reduce the number of files\n"
                        f"  2. Use read_file_truncated() for each file first\n"
                        f"  3. Process files in batches"
                    )
                )

            contents.append(section)
            filenames.append(file_content.filename)

        combined_content = separator.join(contents)

        return FileContent(
            content=combined_content,
            filename=f"combined_{len(filenames)}_files",
            file_path=", ".join(str(p) for p in file_paths),
            char_count=len(combined_content),
            line_count=combined_content.count('\n') + 1,
            encoding=self.encoding
        )

    def validate_prompt_length(
            self,
            prompt: str,
            file_content: Optional[FileContent] = None
    ) -> int:
        """
        Validate that prompt (+ optional file content) fits within API limits

        This is called automatically by read_file(), but you can also call it
        manually to check your final prompt before sending to API.

        Args:
            prompt: Your complete prompt text
            file_content: Optional FileContent to include in calculation

        Returns:
            Total character count

        Raises:
            ValidationError: If combined length exceeds API limit
        """
        prompt_length = len(prompt)
        file_length = file_content.char_count if file_content else 0
        total_chars = prompt_length + file_length

        if total_chars > API_MAX_TOTAL_LENGTH:
            raise ValidationError(
                message=f"Combined prompt + file too large: {total_chars:,} characters (API limit: {API_MAX_TOTAL_LENGTH:,})",
                suggestion=(
                    f"Prompt: {prompt_length:,} characters\n"
                    f"File: {file_length:,} characters\n"
                    f"Total: {total_chars:,} characters\n"
                    f"API limit: {API_MAX_TOTAL_LENGTH:,} characters\n\n"
                    f"Solutions:\n"
                    f"  1. Shorten your prompt text\n"
                    f"  2. Use read_file_truncated() with smaller max_chars\n"
                    f"  3. Process content in chunks"
                )
            )

        return total_chars

    def calculate_available_space(
            self,
            prompt_template: str
    ) -> int:
        """
        Calculate how many characters are available for file content
        given a prompt template

        Args:
            prompt_template: Your prompt template (may contain {content} placeholder)

        Returns:
            Available character count for file content
        """
        # Remove placeholder to get base prompt length
        prompt_length = len(prompt_template.replace("{content}", ""))
        available = API_MAX_TOTAL_LENGTH - prompt_length

        if available <= 0:
            raise ValidationError(
                message=f"No space available for file content (prompt is {prompt_length:,} characters, API limit is {API_MAX_TOTAL_LENGTH:,})",
                suggestion="Your prompt template is too long. Shorten it to leave space for file content."
            )

        return available

    # ========================================================================
    # PRIVATE METHODS
    # ========================================================================

    def _validate_file_path(self, file_path: Union[str, Path]) -> Path:
        """Validate file path exists and is readable"""
        path = Path(file_path)

        if not path.exists():
            raise ValidationError(
                message=f"File not found: {file_path}",
                suggestion="Check the file path and ensure the file exists"
            )

        if not path.is_file():
            raise ValidationError(
                message=f"Path is not a file: {file_path}",
                suggestion="Provide a valid file path, not a directory"
            )

        if not os.access(path, os.R_OK):
            raise ValidationError(
                message=f"File not readable: {file_path}",
                suggestion="Check file permissions"
            )

        return path

    def _validate_file_size(self, path: Path):
        """Validate file size isn't too large"""
        size = path.stat().st_size

        if size > MAX_FILE_SIZE_BYTES:
            size_mb = size / (1024 * 1024)
            max_mb = MAX_FILE_SIZE_BYTES / (1024 * 1024)
            raise ValidationError(
                message=f"File too large: {size_mb:.2f} MB (safety limit: {max_mb:.2f} MB)",
                suggestion="This safety limit prevents reading huge files into memory"
            )

        if size == 0:
            raise ValidationError(
                message="File is empty",
                suggestion="Provide a file with content"
            )

    def _validate_file_extension(self, path: Path):
        """Validate file has a supported text extension"""
        ext = path.suffix.lower()

        if ext not in SUPPORTED_TEXT_EXTENSIONS:
            raise ValidationError(
                message=f"Unsupported file type: {ext}",
                suggestion=(
                    f"Supported extensions: {', '.join(sorted(SUPPORTED_TEXT_EXTENSIONS))}\n"
                    f"If this is a text file, you can rename it to .txt"
                )
            )

    def _read_with_encoding(self, path: Path) -> tuple[str, str]:
        """
        Try reading file with multiple encodings

        Returns:
            Tuple of (content, used_encoding)
        """
        # Try default encoding first
        encodings_to_try = [self.encoding] + [
            enc for enc in self.fallback_encodings if enc != self.encoding
        ]

        last_error = None

        for encoding in encodings_to_try:
            try:
                with open(path, 'r', encoding=encoding) as f:
                    content = f.read()
                return content, encoding
            except (UnicodeDecodeError, LookupError) as e:
                last_error = e
                continue

        raise ValidationError(
            message=f"Could not decode file with any encoding: {path.name}",
            suggestion=(
                f"Tried encodings: {', '.join(encodings_to_try)}\n"
                f"Last error: {last_error}\n"
                f"The file might be binary or use an unsupported encoding"
            )
        )


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def read_file_for_prompt(
        file_path: Union[str, Path],
        max_length: int = DEFAULT_MAX_FILE_LENGTH,
        truncate_if_needed: bool = False
) -> str:
    """
    Quick function to read file content for use in prompts

    IMPORTANT: By default, limits file to 72,000 characters to leave space
    for your prompt. API total limit is 90,000 characters (file + prompt).

    Args:
        file_path: Path to file
        max_length: Maximum characters (default: 72,000)
        truncate_if_needed: If True, truncate instead of raising error

    Returns:
        File content as string

    Example:
        content = read_file_for_prompt("data.txt", max_length=50000)
        prompt = f"Analyze this data:\\n\\n{content}"
        # Ensure len(prompt) <= 90,000 characters total
    """
    # Calculate prompt space reservation
    prompt_space = API_MAX_TOTAL_LENGTH - max_length

    reader = FileContentReader(
        max_file_length=max_length,
        prompt_space=prompt_space
    )

    if truncate_if_needed:
        file_content = reader.read_file_truncated(file_path)
    else:
        file_content = reader.read_file(file_path)

    return file_content.content


def get_file_info(file_path: Union[str, Path]) -> dict:
    """
    Get file information without reading full content

    Returns:
        Dict with file metadata
    """
    path = Path(file_path)

    if not path.exists():
        raise ValidationError(
            message=f"File not found: {file_path}",
            suggestion="Check the file path"
        )

    stat = path.stat()

    return {
        'filename': path.name,
        'path': str(path.absolute()),
        'size_bytes': stat.st_size,
        'size_mb': stat.st_size / (1024 * 1024),
        'extension': path.suffix,
        'is_text': path.suffix.lower() in SUPPORTED_TEXT_EXTENSIONS
    }