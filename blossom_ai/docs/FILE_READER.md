# File Content Reader

Utility for reading text files and integrating them with Blossom AI API, respecting prompt length limits.

---

## ⚠️ Important: API Limits

**The Pollinations AI API has a total limit of 10,000 characters for text generation requests.**

This includes:
- Your prompt text
- File content (if you use files)
- Any additional formatting

**By default, `FileContentReader` limits file content to 8,000 characters** to leave space for your prompt. However, **you are responsible** for ensuring the final combined length doesn't exceed 10,000 characters.

```python
# Example: This will work
file = read_file_for_prompt("data.txt")  # 7000 chars
prompt = f"Analyze: {file}"               # 7000 + 100 = 7100 chars ✅

# Example: This will fail at API level
file = read_file_for_prompt("data.txt")  # 8000 chars  
prompt = f"Very long prompt 3000 chars {file}"  # 8000 + 3000 = 11000 chars ❌
# API will reject this request!
```

---

## 📋 Features

- ✅ Read text files with size validation
- ✅ Auto-truncate files that are too long
- ✅ Multiple encoding support (UTF-8, Latin-1, CP1252, etc.)
- ✅ Combine multiple files
- ✅ Calculate available space for content
- ✅ Detailed error messages with suggestions
- ✅ Support for 20+ text file formats

---

## 🚀 Quick Start

### Simple Usage

```python
from blossom_ai import Blossom
from blossom_ai.utils import read_file_for_prompt

# Read file content (limited to 8000 chars by default)
content = read_file_for_prompt("data.txt")

# Use with API
client = Blossom()
response = client.text.generate(
    prompt=f"Analyze this data:\n\n{content}",
    model="deepseek"
)
print(response)
```

### With Auto-Truncation

```python
from blossom_ai.utils import read_file_for_prompt

# Automatically truncate if file exceeds 8000 characters
content = read_file_for_prompt(
    "large_file.txt",
    truncate_if_needed=True
)
```

### Full Control

```python
from blossom_ai.utils import FileContentReader

# Create reader with custom file limit
reader = FileContentReader(
    max_file_length=6000,    # Limit file to 6000 chars
    prompt_space=4000        # Reserve 4000 for prompt
)

# Read file
file_content = reader.read_file("document.txt")

print(f"Read: {file_content.char_count:,} characters")
print(f"Lines: {file_content.line_count:,}")
print(f"Encoding: {file_content.encoding}")
```

---

## 📚 API Reference

### FileContentReader

Main class for working with file content.

#### Initialization

```python
reader = FileContentReader(
    max_file_length=8000,         # Maximum file content length (default: 8000)
    prompt_space=2000,            # Space reserved for prompt (default: 2000)
    encoding='utf-8',             # Primary encoding to try
    fallback_encodings=['utf-8', 'latin-1', 'cp1252']  # Fallback encodings
)
```

**Note:** `max_file_length + prompt_space` should not exceed `10000` (API limit).

---

#### Methods

##### `read_file(file_path, max_chars=None, strip_whitespace=True)`

Read file content with validation.

**Parameters:**
- `file_path` (str | Path): Path to text file
- `max_chars` (int, optional): Custom character limit (uses `max_file_length` if None)
- `strip_whitespace` (bool): Strip leading/trailing whitespace

**Returns:** `FileContent` object

**Raises:** `FileTooLargeError` if file exceeds the limit

```python
from blossom_ai.utils import FileContentReader
from blossom_ai.core import FileTooLargeError

reader = FileContentReader()

try:
    file_content = reader.read_file("data.txt")
except FileTooLargeError as e:
    print(e.message)
    # Use truncation instead
    file_content = reader.read_file_truncated("data.txt")
```

---

##### `read_file_truncated(file_path, max_chars=None, add_truncation_note=True)`

Read file and truncate if necessary.

**Parameters:**
- `file_path` (str | Path): Path to text file
- `max_chars` (int, optional): Maximum characters to read (uses `max_file_length` if None)
- `add_truncation_note` (bool): Add note if content was truncated

**Returns:** `FileContent` with potentially truncated content

```python
# Automatically truncate if file is too long
file_content = reader.read_file_truncated(
    "huge_file.txt",
    max_chars=5000,
    add_truncation_note=True
)
# Content will include: "[... truncated, showing 5,000 of 50,000 characters ...]"
```

---

##### `read_multiple_files(file_paths, separator="\n\n---\n\n", max_total_chars=None)`

Read and combine multiple files.

**Parameters:**
- `file_paths` (List[str | Path]): List of file paths
- `separator` (str): String to insert between files
- `max_total_chars` (int, optional): Maximum total characters (uses `max_file_length` if None)

**Returns:** Combined `FileContent`

**Raises:** `FileTooLargeError` if combined content exceeds limit

```python
combined = reader.read_multiple_files(
    ["file1.txt", "file2.txt", "file3.txt"],
    separator="\n\n--- NEXT FILE ---\n\n",
    max_total_chars=8000
)
```

---

##### `validate_prompt_length(prompt, file_content=None)`

Validate that prompt (+ optional file content) fits within API limits.

**Parameters:**
- `prompt` (str): Your complete prompt text
- `file_content` (FileContent, optional): Optional FileContent to include

**Returns:** Total character count

**Raises:** `ValidationError` if combined length exceeds API limit (10,000)

```python
# Check final prompt length before sending to API
file_content = reader.read_file("data.txt")
prompt = f"Analyze this:\n\n{file_content.content}"

try:
    total = reader.validate_prompt_length(prompt)
    print(f"Total: {total} chars - OK to send!")
except ValidationError as e:
    print(f"Error: {e.message}")
    # Shorten prompt or use smaller file
```

---

##### `calculate_available_space(prompt_template)`

Calculate how many characters are available for file content given a prompt template.

**Parameters:**
- `prompt_template` (str): Your prompt template (may contain `{content}` placeholder)

**Returns:** Available character count

```python
available = reader.calculate_available_space(
    "Analyze: {content}\n\nProvide insights."
)
print(f"Available for file: {available:,} characters")
```

---

### FileContent

Data class containing file content and metadata.

**Attributes:**
- `content` (str): File content as string
- `filename` (str): Name of the file
- `file_path` (str): Full path to file
- `char_count` (int): Number of characters
- `line_count` (int): Number of lines
- `encoding` (str): Encoding used to read file

---

### Convenience Functions

#### `read_file_for_prompt(file_path, max_length=8000, truncate_if_needed=False)`

Quick function to read file content for use in prompts.

**Default limit is 8000 characters** to leave space for your prompt.

```python
from blossom_ai.utils import read_file_for_prompt

# Simple read (max 8000 chars)
content = read_file_for_prompt("data.txt")

# With auto-truncation
content = read_file_for_prompt(
    "large_file.txt",
    max_length=5000,
    truncate_if_needed=True
)
```

---

#### `get_file_info(file_path)`

Get file information without reading full content.

**Returns:** Dict with file metadata

```python
from blossom_ai.utils import get_file_info

info = get_file_info("document.txt")
print(info['filename'])      # "document.txt"
print(info['size_mb'])       # 2.5
print(info['extension'])     # ".txt"
print(info['is_text'])       # True
```

---

## 🎯 Common Use Cases

### 1. Code Analysis

```python
from blossom_ai import Blossom
from blossom_ai.utils import FileContentReader

reader = FileContentReader(max_file_length=7000)

# Read code file
code = reader.read_file("script.py")

prompt = f"""Review this code and suggest improvements:

{code.content}

Focus on:
- Performance optimizations
- Code readability
- Best practices
"""

# Validate before sending
reader.validate_prompt_length(prompt)

# Generate
client = Blossom()
response = client.text.generate(prompt=prompt, model="qwen-coder")
print(response)
```

---

### 2. Document Summarization

```python
from blossom_ai import Blossom
from blossom_ai.utils import read_file_for_prompt

# Auto-truncate if needed
content = read_file_for_prompt(
    "long_article.txt",
    max_length=6000,
    truncate_if_needed=True
)

client = Blossom()
response = client.text.generate(
    prompt=f"Summarize this article in 3-5 bullet points:\n\n{content}",
    model="deepseek"
)
print(response)
```

---

### 3. Multiple File Comparison

```python
from blossom_ai import Blossom
from blossom_ai.utils import FileContentReader

reader = FileContentReader(max_file_length=8000)

files = ["version1.py", "version2.py"]
combined = reader.read_multiple_files(
    files,
    separator="\n\n=== NEXT VERSION ===\n\n"
)

client = Blossom()
response = client.text.generate(
    prompt=f"Compare these code versions:\n\n{combined.content}",
    model="gemini"
)
print(response)
```

---

### 4. Streaming with File Content

```python
from blossom_ai import Blossom
from blossom_ai.utils import read_file_for_prompt

content = read_file_for_prompt("data.csv", max_length=5000)

client = Blossom()

print("Analyzing data...\n")
for chunk in client.text.generate_stream(
    prompt=f"Analyze this CSV data:\n\n{content}",
    model="deepseek"
):
    print(chunk.content, end='', flush=True)
```

---

## ⚙️ Configuration

### Available Constants

```python
from blossom_ai.utils import (
    API_MAX_TOTAL_LENGTH,      # 10000 - Total API limit
    DEFAULT_MAX_FILE_LENGTH,   # 8000 - Default file limit
    DEFAULT_PROMPT_SPACE,      # 2000 - Default prompt space
    SUPPORTED_TEXT_EXTENSIONS  # Supported file types
)

print(API_MAX_TOTAL_LENGTH)      # 10000
print(DEFAULT_MAX_FILE_LENGTH)   # 8000
print(DEFAULT_PROMPT_SPACE)      # 2000
```

### Supported File Extensions

```python
from blossom_ai.utils import SUPPORTED_TEXT_EXTENSIONS

print(SUPPORTED_TEXT_EXTENSIONS)
# {'.txt', '.md', '.json', '.csv', '.py', '.js', ...}
```

### Custom Settings

```python
reader = FileContentReader(
    max_file_length=6000,                       # Custom file limit
    prompt_space=4000,                          # Custom prompt space
    encoding='utf-8',                           # Primary encoding
    fallback_encodings=['utf-8', 'cp1252']      # Fallback encodings
)
```

---

## 🚨 Error Handling

### FileTooLargeError

Raised when file content exceeds the configured limit.

```python
from blossom_ai.core import FileTooLargeError
from blossom_ai.utils import FileContentReader

reader = FileContentReader(max_file_length=5000)

try:
    file_content = reader.read_file("large_file.txt")
    
except FileTooLargeError as e:
    print(f"Error: {e.message}")
    print(f"Suggestion: {e.suggestion}")
    
    # Use truncation instead
    file_content = reader.read_file_truncated("large_file.txt")
    print(f"Successfully read {file_content.char_count:,} characters")
```

### ValidationError

Raised for other validation issues (file not found, encoding errors, etc.)

```python
from blossom_ai.core import ValidationError

try:
    content = read_file_for_prompt("missing.txt")
except ValidationError as e:
    print(f"Error: {e.message}")
    print(f"Suggestion: {e.suggestion}")
```

---

## 💡 Best Practices

### 1. Always Check Final Prompt Length

```python
# Read file
content = read_file_for_prompt("data.txt")

# Build prompt
prompt = f"Long prompt text here...\n\n{content}"

# Validate BEFORE sending to API
reader = FileContentReader()
try:
    reader.validate_prompt_length(prompt)
    # Safe to send!
except ValidationError:
    # Too long, need to reduce file or prompt
    content = read_file_for_prompt("data.txt", max_length=5000, truncate_if_needed=True)
```

### 2. Use Available Space Calculation

```python
# Calculate space first
reader = FileContentReader()
available = reader.calculate_available_space("Analyze: {content}")

# Then read with that limit
content = read_file_for_prompt("file.txt", max_length=available, truncate_if_needed=True)
```

### 3. Handle Large Files Gracefully

```python
from blossom_ai.utils import get_file_info

# Check size first
info = get_file_info("file.txt")

if info['size_mb'] > 1:
    # Large file - use truncation
    content = read_file_for_prompt("file.txt", truncate_if_needed=True)
else:
    # Small file - read normally
    content = read_file_for_prompt("file.txt")
```

### 4. Provide Context in Prompts

```python
# Good - clear context
prompt = f"""
File: {file_content.filename}
Lines: {file_content.line_count:,}
Size: {file_content.char_count:,} characters

Content:
{file_content.content}

Please analyze and provide insights.
"""
```

---

## 🔧 Advanced Usage

### Custom Encoding Handling

```python
reader = FileContentReader(
    max_file_length=8000,
    encoding='utf-8',
    fallback_encodings=['utf-8', 'cp1252', 'latin-1', 'iso-8859-1']
)

# Reader will automatically try encodings in order
file_content = reader.read_file("legacy_file.txt")
print(f"Used encoding: {file_content.encoding}")
```

### Processing File in Chunks

```python
def process_large_file(filepath, chunk_size=5000):
    """Process large file in chunks"""
    with open(filepath, 'r', encoding='utf-8') as f:
        full_content = f.read()
    
    # Split into chunks
    chunks = [full_content[i:i+chunk_size] 
              for i in range(0, len(full_content), chunk_size)]
    
    results = []
    client = Blossom()
    
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)}...")
        
        response = client.text.generate(
            prompt=f"Analyze this section:\n\n{chunk}",
            model="deepseek"
        )
        results.append(response)
    
    return results
```

---

## 📝 Notes

- **API total limit:** 10,000 characters (file + prompt combined)
- **Default file limit:** 8,000 characters
- **Default prompt space:** 2,000 characters
- **Maximum file size to read:** 10 MB (safety limit)
- **Encoding detection:** Tries multiple encodings automatically
- **Files are read into memory** (not streamed)
- **You are responsible** for ensuring final prompt doesn't exceed 10,000 characters

---

## 🛠 Troubleshooting

**Problem:** `FileTooLargeError` - File exceeds limit  
**Solution:** Use `read_file_truncated()` or reduce `max_length` parameter

**Problem:** API rejects request (too long)  
**Solution:** Your prompt + file exceeds 10,000 chars. Reduce file size or shorten prompt.

**Problem:** `File not found` error  
**Solution:** Check the file path is correct and file exists

**Problem:** `Unsupported file type` error  
**Solution:** Rename file to `.txt` or ensure extension is in `SUPPORTED_TEXT_EXTENSIONS`

**Problem:** `Could not decode file` error  
**Solution:** File might be binary or use unsupported encoding

---
