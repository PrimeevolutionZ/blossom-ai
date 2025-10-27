"""
Tests for File Content Reader Utility

Tests all functionality:
- File reading with size limits
- Auto-truncation
- Multiple file handling
- Encoding detection
- Error handling
- API limit validation
"""

import pytest
import tempfile
import os
from pathlib import Path

from blossom_ai.utils import (
    FileContentReader,
    FileContent,
    read_file_for_prompt,
    get_file_info,
    API_MAX_TOTAL_LENGTH,
    DEFAULT_MAX_FILE_LENGTH,
    DEFAULT_PROMPT_SPACE,
    SUPPORTED_TEXT_EXTENSIONS,
)

from blossom_ai.core import (
    ValidationError,
    FileTooLargeError,
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def temp_dir():
    """Create temporary directory for test files"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def small_file(temp_dir):
    """Create small test file (100 chars)"""
    file_path = temp_dir / "small.txt"
    content = "A" * 100
    file_path.write_text(content, encoding='utf-8')
    return file_path


@pytest.fixture
def medium_file(temp_dir):
    """Create medium test file (5000 chars)"""
    file_path = temp_dir / "medium.txt"
    content = "B" * 5000
    file_path.write_text(content, encoding='utf-8')
    return file_path


@pytest.fixture
def large_file(temp_dir):
    """Create large test file (9000 chars - exceeds default limit)"""
    file_path = temp_dir / "large.txt"
    content = "C" * 9000
    file_path.write_text(content, encoding='utf-8')
    return file_path


@pytest.fixture
def huge_file(temp_dir):
    """Create huge test file (15000 chars)"""
    file_path = temp_dir / "huge.txt"
    content = "D" * 15000
    file_path.write_text(content, encoding='utf-8')
    return file_path


@pytest.fixture
def empty_file(temp_dir):
    """Create empty file"""
    file_path = temp_dir / "empty.txt"
    file_path.write_text("", encoding='utf-8')
    return file_path


@pytest.fixture
def multiline_file(temp_dir):
    """Create file with multiple lines"""
    file_path = temp_dir / "multiline.txt"
    content = "Line 1\nLine 2\nLine 3\nLine 4\nLine 5"
    file_path.write_text(content, encoding='utf-8')
    return file_path


@pytest.fixture
def utf8_file(temp_dir):
    """Create file with UTF-8 special characters"""
    file_path = temp_dir / "utf8.txt"
    content = "Hello 世界 🌸 Привет"
    file_path.write_text(content, encoding='utf-8')
    return file_path


@pytest.fixture
def latin1_file(temp_dir):
    """Create file with Latin-1 encoding"""
    file_path = temp_dir / "latin1.txt"
    content = "Café résumé naïve"
    file_path.write_bytes(content.encode('latin-1'))
    return file_path


# ============================================================================
# BASIC FUNCTIONALITY TESTS
# ============================================================================

class TestBasicFileReading:
    """Test basic file reading functionality"""

    def test_read_small_file(self, small_file):
        """Test reading small file"""
        reader = FileContentReader()
        file_content = reader.read_file(small_file)

        assert isinstance(file_content, FileContent)
        assert file_content.char_count == 100
        assert file_content.content == "A" * 100
        assert file_content.filename == "small.txt"
        assert file_content.encoding == "utf-8"
        assert file_content.line_count == 1  # Single line file

    def test_read_medium_file(self, medium_file):
        """Test reading medium file (within limits)"""
        reader = FileContentReader()
        file_content = reader.read_file(medium_file)

        assert file_content.char_count == 5000
        assert file_content.content == "B" * 5000

    def test_file_content_metadata(self, multiline_file):
        """Test FileContent metadata"""
        reader = FileContentReader()
        file_content = reader.read_file(multiline_file)

        assert file_content.line_count == 5
        assert file_content.filename == "multiline.txt"
        assert str(multiline_file) in file_content.file_path

    def test_strip_whitespace(self, temp_dir):
        """Test whitespace stripping"""
        file_path = temp_dir / "whitespace.txt"
        file_path.write_text("  \n  Content  \n  ", encoding='utf-8')

        reader = FileContentReader()

        # With stripping (default)
        content = reader.read_file(file_path, strip_whitespace=True)
        assert content.content == "Content"

        # Without stripping
        content = reader.read_file(file_path, strip_whitespace=False)
        assert content.content == "  \n  Content  \n  "


# ============================================================================
# SIZE LIMIT TESTS
# ============================================================================

class TestSizeLimits:
    """Test file size limit enforcement"""

    def test_default_file_limit(self):
        """Test default limits are set correctly"""
        reader = FileContentReader()
        assert reader.max_file_length == DEFAULT_MAX_FILE_LENGTH
        assert reader.prompt_space == DEFAULT_PROMPT_SPACE
        assert DEFAULT_MAX_FILE_LENGTH == 8000
        assert DEFAULT_PROMPT_SPACE == 2000
        assert API_MAX_TOTAL_LENGTH == 10000

    def test_file_exceeds_default_limit(self, large_file):
        """Test FileTooLargeError when file exceeds 8000 chars"""
        reader = FileContentReader()

        with pytest.raises(FileTooLargeError) as exc_info:
            reader.read_file(large_file)

        error = exc_info.value
        assert "9,000" in error.message or "9000" in error.message
        assert "8,000" in error.message or "8000" in error.message
        assert "read_file_truncated" in error.suggestion

    def test_custom_file_limit(self, medium_file):
        """Test custom file limit"""
        reader = FileContentReader(max_file_length=3000, prompt_space=7000)

        # Should fail with 5000 chars when limit is 3000
        with pytest.raises(FileTooLargeError):
            reader.read_file(medium_file)

    def test_file_within_custom_limit(self, medium_file):
        """Test file within custom limit passes"""
        reader = FileContentReader(max_file_length=6000, prompt_space=4000)

        # Should succeed with 5000 chars when limit is 6000
        file_content = reader.read_file(medium_file)
        assert file_content.char_count == 5000

    def test_invalid_config(self):
        """Test invalid configuration (exceeds API limit)"""
        with pytest.raises(ValidationError) as exc_info:
            FileContentReader(max_file_length=8000, prompt_space=3000)  # 11000 > 10000

        error = exc_info.value
        assert "Configuration error" in error.message


# ============================================================================
# TRUNCATION TESTS
# ============================================================================

class TestTruncation:
    """Test file truncation functionality"""

    def test_truncate_large_file(self, large_file):
        """Test truncating large file"""
        reader = FileContentReader()
        file_content = reader.read_file_truncated(large_file)

        assert file_content.char_count <= DEFAULT_MAX_FILE_LENGTH + 100  # +100 for truncation note
        assert "[... truncated" in file_content.content
        assert "9,000" in file_content.content or "9000" in file_content.content

    def test_truncate_with_custom_limit(self, huge_file):
        """Test truncation with custom limit"""
        reader = FileContentReader()
        file_content = reader.read_file_truncated(huge_file, max_chars=5000)

        # Should be ~5000 + truncation note
        assert 5000 <= file_content.char_count <= 5200
        assert "[... truncated" in file_content.content

    def test_truncate_without_note(self, large_file):
        """Test truncation without note"""
        reader = FileContentReader()
        file_content = reader.read_file_truncated(
            large_file,
            max_chars=5000,
            add_truncation_note=False
        )

        assert file_content.char_count == 5000
        assert "[... truncated" not in file_content.content

    def test_no_truncation_if_small(self, small_file):
        """Test no truncation for small files"""
        reader = FileContentReader()
        file_content = reader.read_file_truncated(small_file)

        assert file_content.char_count == 100
        assert "[... truncated" not in file_content.content


# ============================================================================
# MULTIPLE FILES TESTS
# ============================================================================

class TestMultipleFiles:
    """Test reading multiple files"""

    def test_read_multiple_files(self, temp_dir):
        """Test combining multiple files"""
        file1 = temp_dir / "file1.txt"
        file2 = temp_dir / "file2.txt"
        file3 = temp_dir / "file3.txt"

        file1.write_text("Content 1", encoding='utf-8')
        file2.write_text("Content 2", encoding='utf-8')
        file3.write_text("Content 3", encoding='utf-8')

        reader = FileContentReader()
        combined = reader.read_multiple_files([file1, file2, file3])

        assert "file1.txt" in combined.content
        assert "file2.txt" in combined.content
        assert "file3.txt" in combined.content
        assert "Content 1" in combined.content
        assert "Content 2" in combined.content
        assert "Content 3" in combined.content

    def test_multiple_files_custom_separator(self, temp_dir):
        """Test custom separator"""
        file1 = temp_dir / "a.txt"
        file2 = temp_dir / "b.txt"

        file1.write_text("AAA", encoding='utf-8')
        file2.write_text("BBB", encoding='utf-8')

        reader = FileContentReader()
        combined = reader.read_multiple_files(
            [file1, file2],
            separator="\n### SEPARATOR ###\n"
        )

        assert "### SEPARATOR ###" in combined.content

    def test_multiple_files_exceed_limit(self, temp_dir):
        """Test error when combined files exceed limit"""
        file1 = temp_dir / "big1.txt"
        file2 = temp_dir / "big2.txt"

        file1.write_text("A" * 5000, encoding='utf-8')
        file2.write_text("B" * 5000, encoding='utf-8')

        reader = FileContentReader(max_file_length=8000)

        with pytest.raises(FileTooLargeError) as exc_info:
            reader.read_multiple_files([file1, file2])

        error = exc_info.value
        assert "Combined files too large" in error.message

    def test_empty_file_list(self):
        """Test error with empty file list"""
        reader = FileContentReader()

        with pytest.raises(ValidationError) as exc_info:
            reader.read_multiple_files([])

        assert "No files provided" in exc_info.value.message


# ============================================================================
# ENCODING TESTS
# ============================================================================

class TestEncoding:
    """Test encoding detection and handling"""

    def test_utf8_encoding(self, utf8_file):
        """Test UTF-8 file reading"""
        reader = FileContentReader()
        file_content = reader.read_file(utf8_file)

        assert "世界" in file_content.content
        assert "🌸" in file_content.content
        assert "Привет" in file_content.content
        assert file_content.encoding == "utf-8"

    def test_latin1_encoding(self, latin1_file):
        """Test Latin-1 fallback encoding"""
        reader = FileContentReader()
        file_content = reader.read_file(latin1_file)

        assert "Café" in file_content.content
        assert "résumé" in file_content.content
        assert file_content.encoding in ['latin-1', 'cp1252']

    def test_custom_encoding_order(self, temp_dir):
        """Test custom encoding order"""
        file_path = temp_dir / "custom.txt"
        content = "Test content"
        file_path.write_text(content, encoding='utf-8')

        reader = FileContentReader(
            encoding='ascii',
            fallback_encodings=['ascii', 'utf-8']
        )

        file_content = reader.read_file(file_path)
        assert file_content.content == content


# ============================================================================
# VALIDATION TESTS
# ============================================================================

class TestValidation:
    """Test validation functionality"""

    def test_validate_prompt_length_ok(self, small_file):
        """Test validation passes for valid prompt"""
        reader = FileContentReader()
        file_content = reader.read_file(small_file)

        prompt = f"Analyze this:\n\n{file_content.content}"
        total = reader.validate_prompt_length(prompt)

        assert total < API_MAX_TOTAL_LENGTH

    def test_validate_prompt_length_fail(self, large_file):
        """Test validation fails for too long prompt"""
        reader = FileContentReader()
        file_content = reader.read_file_truncated(large_file)  # 8000 chars

        prompt = f"{'X' * 3000}\n\n{file_content.content}"  # 3000 + 8000+ = > 10000

        with pytest.raises(ValidationError) as exc_info:
            reader.validate_prompt_length(prompt)

        error = exc_info.value
        assert "too large" in error.message.lower()
        assert "10,000" in error.message or "10000" in error.message

    def test_validate_with_file_content(self, medium_file):
        """Test validation with FileContent object"""
        reader = FileContentReader()
        file_content = reader.read_file(medium_file)

        prompt = "Short prompt"
        total = reader.validate_prompt_length(prompt, file_content)

        assert total == len(prompt) + file_content.char_count

    def test_calculate_available_space(self):
        """Test available space calculation"""
        reader = FileContentReader()

        prompt_template = "Analyze: {content}"
        available = reader.calculate_available_space(prompt_template)

        # Should be API_MAX - len("Analyze: ")
        expected = API_MAX_TOTAL_LENGTH - len("Analyze: ")
        assert available == expected

    def test_calculate_available_space_no_room(self):
        """Test error when no space available"""
        reader = FileContentReader()

        # Very long prompt
        prompt_template = "X" * 11000

        with pytest.raises(ValidationError) as exc_info:
            reader.calculate_available_space(prompt_template)

        assert "No space available" in exc_info.value.message


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

class TestErrorHandling:
    """Test error handling"""

    def test_file_not_found(self):
        """Test error for non-existent file"""
        reader = FileContentReader()

        with pytest.raises(ValidationError) as exc_info:
            reader.read_file("nonexistent.txt")

        assert "File not found" in exc_info.value.message

    def test_empty_file_error(self, empty_file):
        """Test error for empty file"""
        reader = FileContentReader()

        with pytest.raises(ValidationError) as exc_info:
            reader.read_file(empty_file)

        assert "empty" in exc_info.value.message.lower()

    def test_unsupported_extension(self, temp_dir):
        """Test error for unsupported file type"""
        file_path = temp_dir / "test.exe"
        file_path.write_text("content", encoding='utf-8')

        reader = FileContentReader()

        with pytest.raises(ValidationError) as exc_info:
            reader.read_file(file_path)

        error = exc_info.value
        assert "Unsupported file type" in error.message
        assert ".exe" in error.message

    def test_directory_instead_of_file(self, temp_dir):
        """Test error when path is directory"""
        reader = FileContentReader()

        with pytest.raises(ValidationError) as exc_info:
            reader.read_file(temp_dir)

        assert "not a file" in exc_info.value.message.lower()

    def test_file_too_large_bytes(self, temp_dir):
        """Test error for file exceeding byte size limit"""
        file_path = temp_dir / "huge.txt"
        # Create 11 MB file (exceeds 10 MB limit)
        file_path.write_text("X" * (11 * 1024 * 1024), encoding='utf-8')

        reader = FileContentReader()

        with pytest.raises(ValidationError) as exc_info:
            reader.read_file(file_path)

        assert "too large" in exc_info.value.message.lower()


# ============================================================================
# CONVENIENCE FUNCTIONS TESTS
# ============================================================================

class TestConvenienceFunctions:
    """Test convenience functions"""

    def test_read_file_for_prompt_simple(self, small_file):
        """Test simple read_file_for_prompt"""
        content = read_file_for_prompt(small_file)

        assert isinstance(content, str)
        assert len(content) == 100
        assert content == "A" * 100

    def test_read_file_for_prompt_with_limit(self, medium_file):
        """Test read_file_for_prompt with custom limit"""
        # Should fail without truncate (medium_file is 5000 chars, limit is 3000)
        with pytest.raises(FileTooLargeError):
            read_file_for_prompt(medium_file, max_length=3000)

        # Should work with truncate
        content = read_file_for_prompt(medium_file, max_length=3000, truncate_if_needed=True)
        assert len(content) <= 3200  # 3000 + truncation note

    def test_read_file_for_prompt_truncate(self, large_file):
        """Test read_file_for_prompt with truncation"""
        content = read_file_for_prompt(
            large_file,
            max_length=5000,
            truncate_if_needed=True
        )

        assert len(content) <= 5200  # 5000 + truncation note
        assert "[... truncated" in content

    def test_read_file_for_prompt_error(self, large_file):
        """Test read_file_for_prompt raises error without truncate"""
        with pytest.raises(FileTooLargeError):
            read_file_for_prompt(large_file, truncate_if_needed=False)

    def test_get_file_info(self, small_file):
        """Test get_file_info function"""
        info = get_file_info(small_file)

        assert info['filename'] == 'small.txt'
        assert info['extension'] == '.txt'
        assert info['is_text'] is True
        assert info['size_bytes'] > 0
        assert 'path' in info

    def test_get_file_info_not_found(self):
        """Test get_file_info with non-existent file"""
        with pytest.raises(ValidationError):
            get_file_info("nonexistent.txt")


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Test complete workflows"""

    def test_complete_workflow(self, temp_dir):
        """Test complete file reading workflow"""
        # Create test file
        file_path = temp_dir / "test.py"
        code = "def hello():\n    print('Hello, World!')\n" * 100
        file_path.write_text(code, encoding='utf-8')

        # Check file info
        info = get_file_info(file_path)
        assert info['is_text'] is True

        # Read file
        reader = FileContentReader()
        file_content = reader.read_file(file_path)

        # Build prompt
        prompt = f"Review this code:\n\n{file_content.content}"

        # Validate
        total = reader.validate_prompt_length(prompt)
        assert total < API_MAX_TOTAL_LENGTH

    def test_workflow_with_large_file(self, temp_dir):
        """Test workflow with large file requiring truncation"""
        # Create large file
        file_path = temp_dir / "large_data.csv"
        data = "row,data\n" * 10000
        file_path.write_text(data, encoding='utf-8')

        # Try to read - should fail
        reader = FileContentReader()
        with pytest.raises(FileTooLargeError):
            reader.read_file(file_path)

        # Use truncation
        file_content = reader.read_file_truncated(file_path, max_chars=5000)
        assert file_content.char_count <= 5200

        # Build and validate prompt
        prompt = f"Analyze:\n{file_content.content}"
        total = reader.validate_prompt_length(prompt)
        assert total < API_MAX_TOTAL_LENGTH

    def test_multiple_files_workflow(self, temp_dir):
        """Test workflow with multiple files"""
        # Create multiple small files (reduced size to fit in limit)
        files = []
        for i in range(3):
            file_path = temp_dir / f"file{i}.txt"
            # Smaller content: ~1500 chars each = ~4500 total + headers
            file_path.write_text(f"Content {i}\n" * 100, encoding='utf-8')
            files.append(file_path)

        # Combine files
        reader = FileContentReader()
        combined = reader.read_multiple_files(files, max_total_chars=7000)

        # Should succeed now
        assert "file0.txt" in combined.content
        assert "file1.txt" in combined.content
        assert "file2.txt" in combined.content

        # Validate combined content
        prompt = f"Compare these files:\n\n{combined.content}"
        total = reader.validate_prompt_length(prompt)
        assert total < API_MAX_TOTAL_LENGTH

    def test_multiple_files_exceed_limit_workflow(self, temp_dir):
        """Test that multiple large files correctly fail"""
        # Create multiple large files that will exceed limit
        files = []
        for i in range(3):
            file_path = temp_dir / f"bigfile{i}.txt"
            # Large content: ~5000 chars each = way over limit
            file_path.write_text(f"Content {i}\n" * 500, encoding='utf-8')
            files.append(file_path)

        # Should fail with FileTooLargeError
        reader = FileContentReader()
        with pytest.raises(FileTooLargeError) as exc_info:
            reader.read_multiple_files(files, max_total_chars=7000)

        error = exc_info.value
        assert "Combined files too large" in error.message


# ============================================================================
# CONSTANTS TESTS
# ============================================================================

class TestConstants:
    """Test exported constants"""

    def test_api_constants(self):
        """Test API constant values"""
        assert API_MAX_TOTAL_LENGTH == 10000
        assert DEFAULT_MAX_FILE_LENGTH == 8000
        assert DEFAULT_PROMPT_SPACE == 2000
        assert DEFAULT_MAX_FILE_LENGTH + DEFAULT_PROMPT_SPACE == API_MAX_TOTAL_LENGTH

    def test_supported_extensions(self):
        """Test supported file extensions"""
        assert '.txt' in SUPPORTED_TEXT_EXTENSIONS
        assert '.md' in SUPPORTED_TEXT_EXTENSIONS
        assert '.py' in SUPPORTED_TEXT_EXTENSIONS
        assert '.json' in SUPPORTED_TEXT_EXTENSIONS
        assert '.csv' in SUPPORTED_TEXT_EXTENSIONS

        # Should not include binary formats
        assert '.exe' not in SUPPORTED_TEXT_EXTENSIONS
        assert '.zip' not in SUPPORTED_TEXT_EXTENSIONS


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])