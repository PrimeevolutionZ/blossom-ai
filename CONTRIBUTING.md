# Contributing to Blossom AI 🌸

Thank you for your interest in contributing to Blossom AI! We welcome contributions from everyone and are grateful for even the smallest of improvements.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)

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

- Python 3.8 or higher
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
   ```

3. Verify installation:
   ```bash
   python -c "from blossom_ai import Blossom; print('Setup successful!')"
   ```

### Optional: Get API Token

For testing audio generation features:
1. Visit [Pollinations Auth](https://auth.pollinations.ai)
2. Get your API token
3. Set environment variable or use in tests:
   ```bash
   export BLOSSOM_API_TOKEN="your-token-here"
   ```

## How to Contribute

### Types of Contributions

We appreciate all kinds of contributions:

- **Bug fixes** - Fix issues reported in the issue tracker
- **New features** - Add support for new Pollinations API features
- **Documentation** - Improve or add documentation
- **Examples** - Add practical examples and tutorials
- **Tests** - Improve test coverage
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
5. **No `__del__` methods** - Use context managers or explicit cleanup

### Code Organization

```
blossom_ai/
├── core/                  # Core functionality
│   ├── __init__.py
│   ├── config.py         # Configuration constants
│   ├── models.py         # Data models and available options
│   └── session_manager.py # Session management
├── generators/            # Generator classes
│   ├── __init__.py
│   ├── base_generator.py # Base class for generators
│   └── generators.py     # Image, Text, Audio generators
└── blossom.py            # Main unified client
```

## Testing

### Running Tests

We provide a comprehensive test suite:

```bash
# Run all tests
python blossom_ai/test_examples.py

# Run specific test categories
python blossom_ai/test_examples.py --sync
python blossom_ai/test_examples.py --async
python blossom_ai/test_examples.py --streaming
python blossom_ai/test_examples.py --v024

# With API token
python blossom_ai/test_examples.py --token YOUR_TOKEN
```

### Writing Tests

When adding new features:

1. **Add tests** for new functionality
2. **Test both sync and async** - Our hybrid API needs both
3. **Test error cases** - Not just happy paths
4. **Test resource cleanup** - Verify no resource leaks

Example test structure:

```python
def test_new_feature_sync():
    """Test new feature in synchronous mode"""
    with Blossom() as ai:
        result = ai.feature.new_method()
        assert result is not None
        assert len(result) > 0

async def _test_new_feature_async():
    """Test new feature in asynchronous mode"""
    async with Blossom() as ai:
        result = await ai.feature.new_method()
        assert result is not None
        return True
```

### Test Coverage Areas

- ✅ Basic functionality (generate, save)
- ✅ Error handling (validation, network, auth)
- ✅ Streaming (sync and async)
- ✅ Resource cleanup (context managers)
- ✅ Timeout protection
- ✅ Rate limiting

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
- Add tests if applicable
- Update documentation if needed

### 3. Commit Your Changes

Use clear, descriptive commit messages:

```bash
git add .
git commit -m "Add feature: description of what you added"
# or
git commit -m "Fix: description of what you fixed"
```

Good commit message examples:
- `Add: URL generation for image generator`
- `Fix: Memory leak in async session cleanup`
- `Docs: Add Discord bot tutorial`
- `Test: Add streaming timeout protection tests`
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

## Testing
- [ ] Tests pass locally
- [ ] Added new tests for features
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] Commit messages are clear
```

### 6. Review Process

- Maintainers will review your PR
- Address any feedback or requested changes
- Once approved, your PR will be merged

## Reporting Bugs

Found a bug? Help us fix it!

### Before Reporting

1. **Search existing issues** - It might already be reported
2. **Try latest version** - Bug might be fixed
3. **Minimal reproduction** - Isolate the issue

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

with Blossom() as ai:
    # Code that causes the bug
    ai.text.generate("...")
```

**Expected behavior**
What should happen

**Actual behavior**
What actually happens

**Environment**
- OS: [e.g. Windows 10, Ubuntu 22.04, macOS 13]
- Python version: [e.g. 3.8.10]
- Blossom AI version: [e.g. 0.3.0]

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
with Blossom() as ai:
    result = ai.new_feature.method()
```

**Alternatives Considered**
Other ways to solve the problem

**Additional Context**
Screenshots, links, references
```

## Documentation

### Documentation Structure

- `README.md` - Main project overview
- `docs/` - Detailed documentation
- `examples.py` - Practical code examples
- Inline docstrings - API documentation

### Improving Documentation

Good documentation contributions:

- Fix typos or unclear explanations
- Add practical examples
- Improve error messages
- Add tutorials for specific use cases
- Translate documentation

## Community

### Getting Help

- **Issues** - [GitHub Issues](https://github.com/PrimeevolutionZ/blossom-ai/issues)
- **Discussions** - Use GitHub Discussions for questions
- **Examples** - Check `docs/EXAMPLES.md` for code samples

### Staying Updated

- Star the repository to get notifications
- Watch for new releases
- Check the [CHANGELOG](docs/CHANGELOG.md)

## Recognition

All contributors will be recognized in our release notes and documentation. We appreciate every contribution, no matter how small!

## License

By contributing to Blossom AI, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to Blossom AI! 🌸**

Questions? Open an issue or reach out to the [Eclips Team](https://github.com/PrimeevolutionZ).