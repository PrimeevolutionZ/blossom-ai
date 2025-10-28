# Changelog

This document tracks the changes and updates across different versions of the Blossom AI SDK.
## v0.3.2 (Latest)

### 📚 Documentation & Standardization

- **PyPI Page Enhancement**: Updated package metadata for better PyPI presentation
  - Changed development status to `Production/Stable`
  - Added direct links to documentation, changelog, and security policy
  - Improved project discoverability and user navigation

- **Project Standardization**: Added essential project documentation files
  - **CONTRIBUTING.md** - Comprehensive guide for contributors
  - **SECURITY.md** - Detailed security policy and best practices
  - **bug_report.md** - Standardized bug report template
  - **feature_request.md** - Standardized feature request template

- **Metadata Updates** in `pyproject.toml`:
  - Updated development status classifier to `Production/Stable`
  - Added direct documentation links:
    - Documentation Index
    - Changelog
    - Security Policy

### 🎯 Impact

- **Better PyPI Presence**: Enhanced package page with clear documentation links
- **Improved Onboarding**: New contributors can easily understand contribution process
- **Security Transparency**: Clear security policy builds user trust
- **Standardized Reporting**: Consistent issue and feature request templates

### 📝 Notes

- **No code changes** - This is a documentation and metadata update only
- **All existing functionality remains unchanged**
## v0.3.1

### 🔧 Internal Improvements

- **Major Code Refactoring**: Eliminated ResourceWarnings and improved code quality
  - Added centralized configuration in `config.py` with `ENDPOINTS`, `LIMITS`, `DEFAULTS`
  - Implemented DRY principles with `@with_retry` decorator for consistent retry logic
  - Unified error handling across all generators
  - Improved session cleanup with `atexit` handlers and explicit `close()` methods
  - Standardized all comments to English for professional consistency

- **Performance & Stability**:
  - No more ResourceWarnings in output
  - Better memory management with guaranteed session cleanup
  - the actual code optimization is about 35%
  - Improved type hints and documentation (in code)

### 📁 File Changes
- **New**: `blossom_ai/core/config.py` - Centralized configuration
- **Refactored**: `session_manager.py`, `base_generator.py`, `generators.py`, `blossom.py`, `errors.py`
- **Removed**: `base_client.py` (logic moved to base_generator)

### ⚠️ Important Notes
- **Zero breaking changes** - All existing code continues to work unchanged
- **Public API remains 100% compatible**
## v0.3.0 

### ✨ New Features

- **File Content Reader Utility**: New utility module for reading text files and integrating them with AI prompts
  - Read text files with automatic validation against configurable limits
  - Auto-truncate large files to fit within API prompt limits (10,000 characters total)
  - **Default file limit: 8,000 characters** (reserves 2,000 for prompt text)
  - Support for multiple encodings (UTF-8, Latin-1, CP1252, etc.)
  - Combine multiple files into a single prompt
  - Calculate available space for file content
  - Validate combined prompt + file length before API calls
  - Support for 20+ text file formats (.txt, .md, .json, .py, .csv, etc.)
  
- **New Utils Module**: Added `blossom_ai.utils` package with file handling utilities
  - `FileContentReader` - Main class for file operations with configurable limits
  - `FileContent` - Data class for file metadata
  - `read_file_for_prompt()` - Quick function for simple use cases (defaults to 8,000 char limit)
  - `get_file_info()` - Get file metadata without reading content

- **New Error Type**: Added `FileTooLargeError` for better error handling
  - Specific error when file content exceeds configured limits
  - Clear error messages with actionable solutions
  - Separate from general `ValidationError` for easier error handling

### 📚 Documentation

- **New Guide**: Added comprehensive [File Content Reader Guide](docs/FILE_READER.md)
  - Complete API reference for all methods
  - Clear explanation of API limits (10,000 chars total)
  - 4 practical use case examples
  - Error handling best practices with `FileTooLargeError`
  - Advanced usage patterns
- **Updated INDEX.md**: Added utilities section with file reader documentation links
- **Updated README**: Added file reader to features list

### 🔧 API Changes

- **New Exports** in main `blossom_ai` package:
  - `FileContentReader` - Main file reader class
  - `FileContent` - File metadata container
  - `read_file_for_prompt` - Quick file reading function
  - `get_file_info` - File info getter
  - `FileTooLargeError` - New error type
  - `API_MAX_TOTAL_LENGTH` - API limit constant (10,000)
  - `DEFAULT_MAX_FILE_LENGTH` - Default file limit (8,000)
  - `DEFAULT_PROMPT_SPACE` - Default prompt space (2,000)
  - `SUPPORTED_TEXT_EXTENSIONS` - Supported file types

### ⚠️ Important Notes

**API Limits:**
- The Pollinations AI text generation API has a **total limit of 10,000 characters**
- This includes your prompt text + file content combined
- `FileContentReader` defaults to limiting files to **8,000 characters** to leave space for prompts
- **Users are responsible** for ensuring their final prompt doesn't exceed 10,000 characters
- Use `validate_prompt_length()` to check before sending to API

**Example:**
```python
from blossom_ai.utils import read_file_for_prompt

# File limited to 8000 chars by default
content = read_file_for_prompt("data.txt")  

# You must ensure: len(your_prompt + content) <= 10000
prompt = f"Analyze this: {content}"  # Your responsibility to check total length
```

### 🛠️ Migration Guide

**Using File Reader (New in v0.3.0):**

```python
# Before v0.3.0 - manual file reading
with open("data.txt", "r") as f:
    content = f.read()
    if len(content) > 10000:
        content = content[:10000]  # Manual truncation

# v0.3.0 - automatic validation with clear limits
from blossom_ai.utils import read_file_for_prompt
from blossom_ai.core import FileTooLargeError

try:
    # Limited to 8000 chars by default (leaves 2000 for prompt)
    content = read_file_for_prompt("data.txt")
except FileTooLargeError as e:
    print(e.message)
    # Use auto-truncation
    content = read_file_for_prompt("data.txt", truncate_if_needed=True)

# Remember: ensure final prompt + file <= 10,000 characters
```

All existing code continues to work without changes. The new utilities are optional additions.

---

## v0.2.92

### 🐛 Bug Fixes

- **Documentation**: Fixed links for docs in `README.md`

---

## v0.2.91

### 📚 Documentation Updates

- **API Reference Fix**: Restored complete parameter tables that were missing in v0.2.8-0.2.9
  - Added full parameter tables for `Blossom` class initialization
  - Added complete parameter documentation for all `image`, `text`, and `audio` methods
  - Added detailed error types and attributes documentation
- **New Documentation Files**:
  - Added `EXAMPLES.md` - Comprehensive practical examples from original documentation
  - Added `INDEX.md` - Central navigation hub for all documentation
- **README Update**: Added link to new `EXAMPLES.md` in documentation section

---

## v0.2.9

### 🐛 Bug Fixes

- **Critical Path Fix**: Fixed missing `/` in file paths that caused import errors

---

## v0.2.8

### 🐛 Bug Fixes

- **README Links**: Corrected incorrect documentation links in README.md

---

## v0.2.7

### ✨ New Features

- **Documentation Restructuring**: The project documentation has been fully modularized and restructured for improved clarity, navigation, and maintainability
- **Updated README**: The main README now serves as a concise project overview with links to the detailed guides

---

## v0.2.6

### ✨ New Features

- **Enhanced Resource Management**: Implemented proper session cleanup using `atexit` hooks and improved context manager support for both sync and async operations
- **Global Session Registry**: Centralized tracking of all active sessions for better resource control

### 🛠️ Bug Fixes

- Fixed `ResourceWarning` regarding unclosed sessions in certain scenarios
- Improved thread-safety for resource cleanup in complex async environments

---

## v0.2.5

### ✨ New Features

- **Image URL Generation**: Added the `ai.image.generate_url()` method for instant retrieval of image URLs without downloading bytes. This is significantly faster and more efficient for bot and web integrations
- **Private Generation Support**: Added the `private` parameter to image generation methods

---

## v0.2.0

### ✨ New Features

- **Initial Release**: Core functionality for Image, Text, and Audio generation
- **Unified API**: Single `Blossom` class for both synchronous and asynchronous operations
- **Streaming Support**: Real-time text generation with built-in timeout protection

---

<div align="center">

**[View Full Documentation](docs/INDEX.md)** • **[GitHub Repository](https://github.com/PrimeevolutionZ/blossom-ai)**

</div>