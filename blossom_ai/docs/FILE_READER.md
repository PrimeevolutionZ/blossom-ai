# 📁 File Content Reader Guide

> **Read and validate files for AI prompts with automatic size management**

The File Content Reader utility helps you safely read files and prepare them for AI prompts, with automatic size validation, truncation, and encoding detection.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Core Features](#core-features)
- [Advanced Usage](#advanced-usage)
- [Use Cases](#use-cases)
- [Best Practices](#best-practices)
- [API Reference](#api-reference)

---

## 🌟 Overview

### Why Use File Reader?

**Problems it solves:**
- ❌ Files too large for API limits
- ❌ Unknown file encodings
- ❌ Manual size calculations
- ❌ Complex multi-file handling

**What you get:**
- ✅ Automatic size validation
- ✅ Smart truncation
- ✅ Encoding detection
- ✅ Multiple file support
- ✅ Clear error messages

### Key Features

| Feature | Description |
|---------|-------------|
| **Size Limits** | API_MAX_TOTAL_LENGTH = 10,000 chars |
| **Default File Limit** | 8,000 chars (leaves 2,000 for prompt) |
| **Auto-Truncation** | Graceful handling of large files |
| **Encoding Detection** | UTF-8, Latin-1, CP1252 fallback |
| **Multiple Files** | Combine multiple files safely |
| **Validation** | Pre-flight checks before API calls |

---

## 🚀 Quick Start

### Installation

```bash
pip install eclips-blossom-ai
```

### Basic Usage

```python
from blossom_ai.utils import read_file_for_prompt

# Simple file reading
content = read_file_for_prompt("code.py")
print(content)

# Use in prompt
from blossom_ai import Blossom

with Blossom(api_token="your_token") as client:
    prompt = f"Review this code:\n\n{content}"
    response = client.text.generate(prompt)
    print(response)
```

### With Truncation

```python
from blossom_ai.utils import read_file_for_prompt

# Automatically truncate if file is too large
content = read_file_for_prompt(
    "large_file.txt",
    max_length=5000,
    truncate_if_needed=True
)

# Truncation note is added automatically
print(content)
# Output: File content... [... truncated from 15,000 to 5,000 chars]
```

---

## 🎯 Core Features

### 1. Size Validation

```python
from blossom_ai.utils import FileContentReader

reader = FileContentReader()

# Default limits: 8000 chars for file, 2000 for prompt
file_content = reader.read_file("document.txt")

print(f"Character count: {file_content.char_count}")
print(f"Line count: {file_content.line_count}")
print(f"Filename: {file_content.filename}")
```

### 2. Custom Limits

```python
from blossom_ai.utils import FileContentReader

# Custom limits (must total <= 10,000)
reader = FileContentReader(
    max_file_length=7000,  # Max file size
    prompt_space=3000      # Space reserved for prompt
)

try:
    content = reader.read_file("data.csv")
except FileTooLargeError as e:
    print(f"File too large: {e.message}")
    print(f"Suggestion: {e.suggestion}")
```

### 3. Auto-Truncation

```python
from blossom_ai.utils import FileContentReader

reader = FileContentReader()

# Truncate file to fit limits
file_content = reader.read_file_truncated(
    "large_document.txt",
    max_chars=5000,
    add_truncation_note=True  # Adds info about truncation
)

print(file_content.content)
# Shows: [... truncated from 15,000 to 5,000 chars]
```

### 4. Multiple Files

```python
from blossom_ai.utils import FileContentReader

reader = FileContentReader()

# Combine multiple files
files = ["file1.py", "file2.py", "file3.py"]

combined = reader.read_multiple_files(
    files,
    max_total_chars=7000,  # Combined limit
    separator="\n\n" + "="*50 + "\n\n"  # Custom separator
)

print(combined.content)
# Output:
# === file1.py ===
# [content]
# ==================================================
# === file2.py ===
# [content]
```

### 5. Encoding Detection

```python
from blossom_ai.utils import FileContentReader

# Automatic encoding detection
reader = FileContentReader()

file_content = reader.read_file("document.txt")
print(f"Detected encoding: {file_content.encoding}")

# Custom encoding order
reader = FileContentReader(
    encoding='utf-8',
    fallback_encodings=['utf-8', 'latin-1', 'cp1252']
)
```

### 6. Validation Helpers

```python
from blossom_ai.utils import FileContentReader

reader = FileContentReader()

# Read file
file_content = reader.read_file("code.py")

# Build prompt
prompt = f"Review this code:\n\n{file_content.content}"

# Validate total length before API call
try:
    total_length = reader.validate_prompt_length(prompt, file_content)
    print(f"Total length: {total_length} chars (OK!)")
except ValidationError as e:
    print(f"Prompt too long: {e.message}")
```

---

## 🔧 Advanced Usage

### Calculate Available Space

```python
from blossom_ai.utils import FileContentReader

reader = FileContentReader()

# Your prompt template
prompt_template = """
Review this code and provide:
1. Bug analysis
2. Performance suggestions
3. Security concerns

Code:
{content}
"""

# Calculate space available for file content
available = reader.calculate_available_space(prompt_template)
print(f"Available for file: {available} chars")

# Read file with exact limit
file_content = reader.read_file_truncated(
    "code.py",
    max_chars=available
)

# Build final prompt
final_prompt = prompt_template.format(content=file_content.content)
```

### Get File Info

```python
from blossom_ai.utils import get_file_info

# Get file metadata before reading
info = get_file_info("document.txt")

print(f"Filename: {info['filename']}")
print(f"Extension: {info['extension']}")
print(f"Size: {info['size_bytes']} bytes")
print(f"Is text file: {info['is_text']}")
print(f"Path: {info['path']}")

# Decide whether to read
if info['is_text'] and info['size_bytes'] < 1_000_000:
    content = read_file_for_prompt(info['path'])
```

### Custom Separator for Multiple Files

```python
from blossom_ai.utils import FileContentReader

reader = FileContentReader()

files = ["test1.py", "test2.py", "test3.py"]

# Custom separator
combined = reader.read_multiple_files(
    files,
    separator="\n\n### NEXT FILE ###\n\n"
)

print(combined.content)
```

### Whitespace Control

```python
from blossom_ai.utils import FileContentReader

reader = FileContentReader()

# With whitespace stripping (default)
content1 = reader.read_file("file.txt", strip_whitespace=True)
# "  Hello  \n" → "Hello"

# Without whitespace stripping
content2 = reader.read_file("file.txt", strip_whitespace=False)
# "  Hello  \n" → "  Hello  \n"
```

---

## 💼 Use Cases

### Use Case 1: Code Review

```python
from blossom_ai import Blossom
from blossom_ai.utils import read_file_for_prompt

def review_code(file_path: str) -> str:
    """Review code file with AI"""
    try:
        # Read code file (auto-truncate if needed)
        code = read_file_for_prompt(
            file_path,
            max_length=6000,
            truncate_if_needed=True
        )
        
        # Generate review
        with Blossom(api_token="your_token") as client:
            prompt = f"""Review this code:

{code}

Provide:
1. Code quality assessment
2. Potential bugs
3. Performance improvements
4. Security concerns"""

            return client.text.generate(prompt, max_tokens=1000)
            
    except Exception as e:
        return f"Error: {e}"

# Usage
review = review_code("app.py")
print(review)
```

### Use Case 2: Document Analysis

```python
from blossom_ai import Blossom
from blossom_ai.utils import FileContentReader

def analyze_document(doc_path: str, questions: list[str]) -> dict:
    """Analyze document and answer questions"""
    reader = FileContentReader()
    
    # Read document
    doc = reader.read_file_truncated(
        doc_path,
        max_chars=7000,
        add_truncation_note=True
    )
    
    results = {}
    
    with Blossom(api_token="your_token") as client:
        for question in questions:
            prompt = f"""Document:
{doc.content}

Question: {question}

Answer:"""
            
            results[question] = client.text.generate(prompt)
    
    return results

# Usage
questions = [
    "What is the main topic?",
    "What are the key findings?",
    "What are the recommendations?"
]

answers = analyze_document("report.txt", questions)
for q, a in answers.items():
    print(f"Q: {q}")
    print(f"A: {a}\n")
```

### Use Case 3: Multi-File Analysis

```python
from blossom_ai import Blossom
from blossom_ai.utils import FileContentReader

def analyze_project(file_paths: list[str]) -> str:
    """Analyze multiple project files"""
    reader = FileContentReader()
    
    # Combine all files
    try:
        combined = reader.read_multiple_files(
            file_paths,
            max_total_chars=7000,
            separator="\n\n" + "="*60 + "\n\n"
        )
    except FileTooLargeError:
        # Fallback: truncate each file
        contents = []
        per_file_limit = 7000 // len(file_paths)
        
        for path in file_paths:
            fc = reader.read_file_truncated(path, max_chars=per_file_limit)
            contents.append(f"=== {fc.filename} ===\n{fc.content}")
        
        combined_text = "\n\n".join(contents)
    else:
        combined_text = combined.content
    
    # Analyze
    with Blossom(api_token="your_token") as client:
        prompt = f"""Analyze this codebase:

{combined_text}

Provide:
1. Project structure overview
2. Code quality assessment
3. Improvement suggestions"""

        return client.text.generate(prompt, max_tokens=1500)

# Usage
files = ["main.py", "utils.py", "config.py"]
analysis = analyze_project(files)
print(analysis)
```

### Use Case 4: Data Processing

```python
from blossom_ai import Blossom
from blossom_ai.utils import FileContentReader

def analyze_csv(csv_path: str) -> dict:
    """Analyze CSV data"""
    reader = FileContentReader()
    
    # Read CSV (auto-truncate if large)
    csv_content = reader.read_file_truncated(
        csv_path,
        max_chars=6000,
        add_truncation_note=True
    )
    
    with Blossom(api_token="your_token") as client:
        # Get summary
        prompt = f"""Analyze this CSV data:

{csv_content.content}

Provide in JSON format:
- row_count: number of rows
- columns: list of column names
- summary: brief description of data
- insights: key findings"""

        response = client.text.generate(
            prompt,
            json_mode=True
        )
        
        import json
        return json.loads(response)

# Usage
analysis = analyze_csv("sales_data.csv")
print(f"Rows: {analysis['row_count']}")
print(f"Columns: {analysis['columns']}")
print(f"Summary: {analysis['summary']}")
```

---

## ✅ Best Practices

### 1. Always Check File Size First

```python
from blossom_ai.utils import get_file_info, read_file_for_prompt

# ❌ Don't blindly read
content = read_file_for_prompt("unknown_file.txt")

# ✅ Check first
info = get_file_info("unknown_file.txt")
if info['size_bytes'] > 10_000_000:  # 10 MB
    print("File too large to process")
else:
    content = read_file_for_prompt(
        "unknown_file.txt",
        truncate_if_needed=True
    )
```

### 2. Use Truncation for User Files

```python
# ❌ Don't fail on large files
try:
    content = read_file_for_prompt("user_upload.txt")
except FileTooLargeError:
    print("File too large, please upload smaller file")

# ✅ Gracefully truncate
content = read_file_for_prompt(
    "user_upload.txt",
    max_length=5000,
    truncate_if_needed=True
)
# User sees: "[... truncated ...]" note
```

### 3. Reserve Space for Prompt

```python
from blossom_ai.utils import FileContentReader

# ❌ Don't use all 10,000 chars for file
reader = FileContentReader(max_file_length=10000, prompt_space=0)

# ✅ Reserve space for your prompt
reader = FileContentReader(
    max_file_length=6000,  # File content
    prompt_space=4000      # Your prompt + response
)
```

### 4. Validate Before API Call

```python
from blossom_ai.utils import FileContentReader

reader = FileContentReader()

# Read file
file_content = reader.read_file("code.py")

# Build complete prompt
prompt = f"Review this code:\n\n{file_content.content}"

# Validate BEFORE calling API
try:
    reader.validate_prompt_length(prompt, file_content)
except ValidationError as e:
    print(f"Prompt too long: {e.message}")
    # Handle error (truncate, split, etc.)
else:
    # Safe to call API
    response = client.text.generate(prompt)
```

### 5. Handle Multiple Files Carefully

```python
from blossom_ai.utils import FileContentReader

reader = FileContentReader()

files = ["file1.py", "file2.py", "file3.py"]

try:
    # Try to read all
    combined = reader.read_multiple_files(
        files,
        max_total_chars=7000
    )
except FileTooLargeError:
    # Fallback: read fewer files or truncate each
    print("Too many files, processing first 2 only")
    combined = reader.read_multiple_files(
        files[:2],
        max_total_chars=7000
    )
```

---

## 📚 API Reference

### Constants

```python
from blossom_ai.utils import (
    API_MAX_TOTAL_LENGTH,      # 10,000 chars
    DEFAULT_MAX_FILE_LENGTH,   # 8,000 chars
    DEFAULT_PROMPT_SPACE,      # 2,000 chars
    SUPPORTED_TEXT_EXTENSIONS  # ['.txt', '.md', '.py', ...]
)
```

### FileContentReader Class

```python
from blossom_ai.utils import FileContentReader

reader = FileContentReader(
    max_file_length=8000,           # Max file size
    prompt_space=2000,              # Space for prompt
    encoding='utf-8',               # Primary encoding
    fallback_encodings=['latin-1']  # Fallback encodings
)
```

**Methods:**

```python
# Read file with validation
file_content = reader.read_file(
    file_path: str,
    strip_whitespace: bool = True
) -> FileContent

# Read with truncation
file_content = reader.read_file_truncated(
    file_path: str,
    max_chars: Optional[int] = None,
    add_truncation_note: bool = True
) -> FileContent

# Read multiple files
combined = reader.read_multiple_files(
    file_paths: List[str],
    max_total_chars: Optional[int] = None,
    separator: str = "\n\n"
) -> FileContent

# Validate prompt length
total = reader.validate_prompt_length(
    prompt: str,
    file_content: Optional[FileContent] = None
) -> int

# Calculate available space
available = reader.calculate_available_space(
    prompt_template: str
) -> int
```

### FileContent Class

```python
class FileContent:
    content: str          # File content
    char_count: int       # Character count
    line_count: int       # Number of lines
    filename: str         # File name
    file_path: str        # Full path
    encoding: str         # Detected encoding
```

### Convenience Functions

```python
from blossom_ai.utils import read_file_for_prompt, get_file_info

# Quick file reading
content = read_file_for_prompt(
    file_path: str,
    max_length: int = 8000,
    truncate_if_needed: bool = False
) -> str

# Get file info
info = get_file_info(file_path: str) -> dict
# Returns: {
#   'filename': str,
#   'extension': str,
#   'size_bytes': int,
#   'is_text': bool,
#   'path': str
# }
```

### Supported File Extensions

```python
SUPPORTED_TEXT_EXTENSIONS = [
    '.txt', '.md', '.markdown',
    '.py', '.js', '.ts', '.jsx', '.tsx',
    '.java', '.cpp', '.c', '.h', '.cs',
    '.php', '.rb', '.go', '.rs', '.swift',
    '.json', '.yaml', '.yml', '.toml',
    '.xml', '.html', '.htm', '.css', '.scss',
    '.sql', '.sh', '.bash', '.zsh',
    '.csv', '.tsv', '.log',
    '.ini', '.conf', '.cfg'
]
```

---

## ⚠️ Error Handling

### Common Errors

```python
from blossom_ai.utils import (
    FileContentReader,
    FileTooLargeError,
    ValidationError
)

reader = FileContentReader()

try:
    content = reader.read_file("file.txt")
    
except FileNotFoundError:
    print("File not found")
    
except FileTooLargeError as e:
    print(f"File too large: {e.message}")
    print(f"Actual: {e.actual_size}")
    print(f"Max allowed: {e.max_size}")
    print(f"Suggestion: {e.suggestion}")
    # Try with truncation
    content = reader.read_file_truncated("file.txt")
    
except ValidationError as e:
    print(f"Validation error: {e.message}")
    print(f"Suggestion: {e.suggestion}")
    
except UnicodeDecodeError:
    print("Encoding error - file may be binary")
```

### Error Types

| Error | When | Solution |
|-------|------|----------|
| `FileNotFoundError` | File doesn't exist | Check path |
| `FileTooLargeError` | File exceeds limits | Use truncation |
| `ValidationError` | Invalid parameters | Check configuration |
| `UnicodeDecodeError` | Encoding issues | Check file type |

---

## 💡 Tips & Tricks

### Tip 1: Dynamic Limits

```python
from blossom_ai.utils import FileContentReader

def smart_read(file_path: str, prompt_length: int):
    """Adjust file limit based on prompt size"""
    from blossom_ai.utils import API_MAX_TOTAL_LENGTH
    
    file_limit = API_MAX_TOTAL_LENGTH - prompt_length - 500  # Safety margin
    
    reader = FileContentReader(
        max_file_length=file_limit,
        prompt_space=prompt_length + 500
    )
    
    return reader.read_file_truncated(file_path, max_chars=file_limit)
```

### Tip 2: Progress for Large Files

```python
from blossom_ai.utils import FileContentReader

def read_with_progress(files: list[str]):
    """Show progress when reading multiple files"""
    reader = FileContentReader()
    
    for i, file_path in enumerate(files, 1):
        print(f"Reading {i}/{len(files)}: {file_path}...")
        content = reader.read_file_truncated(file_path, max_chars=2000)
        yield content
```

### Tip 3: File Type Detection

```python
from blossom_ai.utils import get_file_info, SUPPORTED_TEXT_EXTENSIONS

def is_supported_file(file_path: str) -> bool:
    """Check if file type is supported"""
    info = get_file_info(file_path)
    return info['extension'] in SUPPORTED_TEXT_EXTENSIONS

# Usage
if is_supported_file("document.txt"):
    content = read_file_for_prompt("document.txt")
else:
    print("Unsupported file type")
```

---

## 🔗 Related Documentation

- [Text Generation](TEXT_GENERATION.md) - Using file content in prompts
- [Reasoning Guide](REASONING.md) - Enhance file analysis
- [Caching Guide](CACHING.md) - Cache file analysis results
- [Error Handling](ERROR_HANDLING.md) - Handle file errors

---

<div align="center">

**Made with 🌸 by the [Eclips Team](https://github.com/PrimeevolutionZ)**

[← Back to Index](INDEX.md) | [Reasoning Guide](REASONING.md) | [Caching Guide](CACHING.md) →

</div>