# Contributing to Blossom AI 🌸

Thank you for your interest in contributing to Blossom AI! We welcome contributions from everyone and are grateful for even the smallest of improvements.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Running Tests](#running-tests)
- [How to Contribute](#how-to-contribute)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)

## Code of Conduct

By participating in this project, you agree to maintain a respectful, inclusive, and harassment-free environment for everyone. We expect all contributors to:

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/blossom-ai.git
   cd blossom-ai
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/PrimeevolutionZ/blossom-ai.git
   ```

## Development Setup

### Prerequisites

- Python 3.12 or higher
- pip package manager
- Git

### Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -e .
   pip install requests aiohttp
   
   # Install test dependencies (v0.4.5+)
   pip install pytest pytest-asyncio vcrpy
   
   # Optional: development tools
   pip install black ruff mypy
   ```

3. Verify installation:
   ```bash
   python -c "from blossom_ai import Blossom; print('Setup successful!')"
   ```

### Optional: Get API Token

For testing features that require authentication:
1. Visit [Pollinations Auth](https://enter.pollinations.ai)
2. Get your API token
3. Set environment variable:
   ```bash
   export POLLINATIONS_API_KEY="your-token-here"
   ```

## Running Tests

**v0.4.5+ includes comprehensive integration tests:**

### Quick Test Run

```bash
# Run all integration tests
pytest tests/test_integration.py -v

# Run specific category
pytest tests/test_integration.py -k "test_text" -v
pytest tests/test_integration.py -k "test_image" -v

# With coverage
pytest tests/test_integration.py --cov=blossom_ai --cov-report=html
```

### Test Recording (VCR.py)

**First run:** Records API interactions to cassettes
```bash
# Set your API token
export POLLINATIONS_API_KEY="your_token"

# Run and record
pytest tests/test_integration.py --record-mode=once -v
```

**Subsequent runs:** Use cached responses (instant)
```bash
# No API token needed - uses cassettes
pytest tests/test_integration.py -v
```

**Update cassettes:**
```bash
# Re-record all interactions
pytest tests/test_integration.py --record-mode=rewrite -v
```


### Running Specific Tests

```bash
# Test text generation
pytest tests/test_integration.py::test_text_generate_simple -v

# Test streaming
pytest tests/test_integration.py::test_text_generate_stream -v

# Test security (tokens not in URLs)
pytest tests/test_integration.py::test_token_not_in_url -v

# Test async
pytest tests/test_integration.py::test_async_text_generate -v
```

## How to Contribute

### Types of Contributions

We appreciate all kinds of contributions:

- **Bug fixes** - Fix issues reported in the issue tracker
- **New features** - Add support for new Pollinations API features
- **Documentation** - Improve or add documentation
- **Examples** - Add practical examples and tutorials
- **Tests** - Improve test coverage (**v0.4.5 priority!**)
- **Performance** - Optimize code for better performance
- **Code quality** - Refactoring, type hints, better error handling

### Before You Start

1. **Check existing issues** - Someone might already be working on it
2. **Open an issue** - Discuss major changes before implementing
3. **Keep it focused** - One feature or fix per pull request
4. **Stay updated** - Sync with upstream regularly

## Code Style Guidelines

### Python Style

We follow standard Python conventions:

- **PEP 8** for code style
- **PEP 257** for docstrings
- **Type hints** where appropriate
- **Descriptive names** for variables and functions

### Example Code Style

```python
from typing import Optional, Union
import asyncio

class ExampleGenerator:
    """
    Example generator with clear documentation.
    
    Args:
        timeout: Request timeout in seconds
        api_token: Optional API authentication token
    """
    
    def __init__(self, timeout: int = 30, api_token: Optional[str] = None):
        self._timeout = timeout
        self._api_token = api_token
    
    def generate(self, prompt: str, **kwargs) -> bytes:
        """
        Generate content from prompt.
        
        Args:
            prompt: Text prompt for generation
            **kwargs: Additional generation parameters
        
        Returns:
            Generated content as bytes
        
        Raises:
            ValidationError: If prompt is invalid
            APIError: If API request fails
        """
        if len(prompt) > 250:
            raise ValidationError("Prompt too long (max 250 characters)")
        
        # Implementation here
        pass
```

### Key Principles

1. **Clear docstrings** - Document classes and public methods
2. **Type hints** - Help users understand function signatures
3. **Error handling** - Use custom exceptions from `errors.py`
4. **Resource management** - Always clean up resources properly
5. **No `__del__` methods** - Use context managers or explicit cleanup (v0.4.5+)
6. **Security first** - Never log tokens, always use headers for auth

## Testing

### Writing Tests

When adding new features, **always add tests** (v0.4.5 requirement):

1. **Add integration test** in `tests/test_integration.py`
2. **Test both sync and async** - Our hybrid API needs both
3. **Test error cases** - Not just happy paths
4. **Test resource cleanup** - Verify no resource leaks
5. **Use VCR.py** - Record API interactions

Example test structure:

```python
import pytest
import vcr
from blossom_ai import Blossom

# VCR configuration
vcr_config = vcr.VCR(
    cassette_library_dir="tests/cassettes",
    record_mode='once'
)

@vcr_config.use_cassette("my_test.yaml")
def test_new_feature():
    """Test new feature with VCR recording"""
    with Blossom(api_version="v2", api_token="token") as client:
        result = client.feature.new_method()
        assert result is not None
        assert len(result) > 0

@pytest.mark.asyncio
@vcr_config.use_cassette("my_test_async.yaml")
async def test_new_feature_async():
    """Test new feature in async mode"""
    async with Blossom(api_version="v2", api_token="token") as client:
        result = await client.feature.new_method()
        assert result is not None
```

### Test Coverage Areas (v0.4.5)

- ✅ Basic functionality (generate, save)
- ✅ Error handling (validation, network, auth)
- ✅ Streaming (sync and async)
- ✅ Resource cleanup (context managers)
- ✅ Timeout protection
- ✅ Rate limiting with retry_after
- ✅ **Security (tokens not in URLs)** 🆕
- ✅ **Memory management** 🆕
- ✅ **Model caching with TTL** 🆕

### Security Testing

**v0.4.5 requires security tests:**

```python
def test_token_security():
    """Verify tokens are never in URLs"""
    client = Blossom(api_version="v2", api_token="test_token_123")
    
    url = client.image.generate_url("test")
    
    # Token should NOT be in URL
    assert "test_token_123" not in url
    assert "token=" not in url.lower()
    
    client.close_sync()
```

## Pull Request Process

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Make Your Changes

- Write clean, documented code
- Follow the style guidelines
- **Add tests** (v0.4.5 requirement!)
- Update documentation if needed
- **Run tests locally** before pushing

```bash
# Format code
black blossom_ai/

# Lint code
ruff check blossom_ai/

# Run tests
pytest tests/test_integration.py -v
```

### 3. Commit Your Changes

Use clear, descriptive commit messages:

```bash
git add .
git commit -m "Add feature: description of what you added"
# or
git commit -m "Fix: description of what you fixed"
```

Good commit message examples:
- `Add: Integration tests with VCR.py (v0.4.5)`
- `Fix: Memory leak in async session cleanup`
- `Security: Tokens only in headers, never in URLs`
- `Docs: Update installation guide for test dependencies`
- `Test: Add security test for token exposure`
- `Refactor: Improve error handling structure`

### 4. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 5. Open a Pull Request

1. Go to the [repository on GitHub](https://github.com/PrimeevolutionZ/blossom-ai)
2. Click "New Pull Request"
3. Select your branch
4. Fill in the PR template:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Security fix
- [ ] Test addition/improvement

## Testing
- [ ] Tests pass locally
- [ ] Added new tests for features
- [ ] Manual testing completed
- [ ] VCR cassettes recorded (if applicable)

## Security Checklist (v0.4.5)
- [ ] No tokens in URLs
- [ ] No sensitive data in logs
- [ ] SSL verification enforced
- [ ] Resource cleanup verified

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] Commit messages are clear
- [ ] Tests added/updated
```

### 6. Review Process

- Maintainers will review your PR
- Address any feedback or requested changes
- Once approved, your PR will be merged

## Reporting Bugs

Found a bug? Help us fix it!

### Before Reporting

1. **Search existing issues** - It might already be reported
2. **Try latest version** - Bug might be fixed in v0.4.5
3. **Minimal reproduction** - Isolate the issue
4. **Run tests** - `pytest tests/test_integration.py -v`

### Bug Report Template

```markdown
**Describe the bug**
Clear description of what's wrong

**To Reproduce**
Steps to reproduce:
1. Initialize client with '...'
2. Call method '...'
3. See error

**Code Example**
```python
from blossom_ai import Blossom

with Blossom(api_version="v2", api_token="token") as ai:
    # Code that causes the bug
    ai.text.generate("...")
```

**Expected behavior**
What should happen

**Actual behavior**
What actually happens

**Environment**
- OS: [e.g. Windows 10, Ubuntu 22.04, macOS 13]
- Python version: [e.g. 3.9.10]
- Blossom AI version: [e.g. 0.4.5]
- Test results: [paste pytest output if relevant]

**Additional context**
Error messages, stack traces, etc.
```

## Suggesting Features

Have an idea? We'd love to hear it!

### Feature Request Template

```markdown
**Feature Description**
Clear description of the feature

**Use Case**
Why is this feature needed? What problem does it solve?

**Proposed Solution**
How would you like it to work?

**Example Usage**
```python
# Show how the feature would be used
with Blossom(api_version="v2") as ai:
    result = ai.new_feature.method()
```

**Testing Considerations**
How would this feature be tested?

**Alternatives Considered**
Other ways to solve the problem

**Additional Context**
Screenshots, links, references
```

## Documentation

### Documentation Structure

- `README.md` - Main project overview
- `docs/` - Detailed documentation
- `tests/` - Test examples with VCR.py (v0.4.5+)
- Inline docstrings - API documentation

### Improving Documentation

Good documentation contributions:

- Fix typos or unclear explanations
- Add practical examples
- Improve error messages
- Add tutorials for specific use cases
- Update installation guides for new features (v0.4.5)
- Document security best practices

## Community

### Getting Help

- **Issues** - [GitHub Issues](https://github.com/PrimeevolutionZ/blossom-ai/issues)
- **Discussions** - Use GitHub Discussions for questions
- **Examples** - Check `docs/` for code samples
- **Tests** - Check `tests/test_integration.py` for usage examples (v0.4.5+)

### Staying Updated

- Star the repository to get notifications
- Watch for new releases (v0.4.5 just released!)
- Check the [CHANGELOG](docs/CHANGELOG.md)

## Recognition

All contributors will be recognized in our release notes and documentation. We appreciate every contribution, no matter how small!

## v0.4.5 Contribution Priorities

**High Priority:**
1. 🧪 Adding more integration tests
2. 📚 Improving documentation
3. 🔒 Security enhancements
4. 🐛 Bug fixes

**Medium Priority:**
1. ⚡ Performance optimizations
2. 🎨 Code quality improvements
3. 📦 New features

**Always Welcome:**
1. 📝 Documentation fixes
2. 🧹 Code cleanup
3. 🔧 Dev tools improvements

## License

By contributing to Blossom AI, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to Blossom AI! 🌸**

Questions? Open an issue or reach out to the [Eclips Team](https://github.com/PrimeevolutionZ).