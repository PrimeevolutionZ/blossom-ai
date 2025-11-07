# Changelog

This document tracks the changes and updates across different versions of the Blossom AI SDK.
---
---

## v0.4.4 (Latest)

### 🏗️ Architecture Refactoring

This release includes a major internal refactoring that improves code maintainability, reduces duplication, and enhances testability while maintaining **100% backward compatibility**.
#### 🔧 Internal Improvements

**Code Reduction**:
- Eliminated 75% of SSE parsing duplication
- Eliminated 80% of parameter building duplication

**Better Architecture**:
- Separation of concerns (streaming, parameters, validation)
- Single Responsibility Principle applied
- DRY (Don't Repeat Yourself) throughout
- Easier to test individual components
- Cleaner generator classes focused on business logic

**Improved Reliability**:
- Better timeout handling in streaming
- Proper resource cleanup (responses always closed)
- More robust Unicode decode error handling
- Consistent error handling across sync/async

#### 🎯 For Advanced Users

New utility classes are now available for custom implementations:

**Parameter Validation**:
```python
from blossom_ai.generators import ParameterValidator

# Validate before generation
ParameterValidator.validate_prompt_length(prompt, 1000, "prompt")
ParameterValidator.validate_dimensions(width, height, 64, 2048)
ParameterValidator.validate_temperature(temperature)
```

**Type-Safe Parameters**:
```python
from blossom_ai.generators import ImageParamsV2

# Build parameters with validation
params = ImageParamsV2(
    model="flux",
    width=1024,
    height=1024,
    quality="hd",
    guidance_scale=7.5,
    negative_prompt="blurry"
)

# Only non-default values included!
request_params = params.to_dict()
```

**Custom SSE Parsing**:
```python
from blossom_ai.generators import SSEParser

parser = SSEParser()
for line in your_stream:
    parsed = parser.parse_line(line)
    if parsed:
        content = parser.extract_content(parsed)
        if content:
            print(content, end='', flush=True)
```

**Custom Streaming**:
```python
from blossom_ai.generators import SyncStreamingMixin

class MyGenerator(SyncGenerator, SyncStreamingMixin):
    def custom_stream(self):
        response = self._make_request(...)
        # Use unified streaming
        return self._stream_sse_response(response)
```

#### 📊 Testing Improvements

New architecture makes testing easier:

**Unit Test Components**:
- SSEParser can be tested independently
- ParameterValidator can be tested independently
- Parameter builders can be tested independently
- No need to mock entire generator for unit tests

**Example Test**:
```python
def test_sse_parser():
    parser = SSEParser()
    result = parser.parse_line('data: {"choices":[{"delta":{"content":"Hi"}}]}')
    assert result is not None
    assert parser.extract_content(result) == "Hi"

def test_image_params():
    params = ImageParams(width=512, height=512, nologo=True)
    data = params.to_dict()
    # model not included (it's default)
    assert data == {"width": 512, "height": 512, "nologo": "true"}
```

#### ⚠️ Breaking Changes

**None!** This is a pure internal refactoring:
- ✅ All public APIs unchanged
- ✅ All method signatures unchanged
- ✅ All return types unchanged
- ✅ 100% backward compatible
- ✅ Existing code works without changes

#### 🎁 Benefits

**For Users**:
- More stable streaming (better timeout handling)
- Better error messages (centralized validation)
- No action required (everything just works better)

**For Developers**:
- Easier to add new parameters
- Easier to add new models
- Easier to fix bugs (single location)
- Easier to test (separated concerns)
- Better code organization

#### 🔍 Migration Notes

**No migration needed!** All existing code continues to work:

```python
# Your existing code - still works perfectly!
from blossom_ai import Blossom

client = Blossom(api_version="v2", api_token="token")
image = client.image.generate("sunset", quality="hd")
text = client.text.generate("Hello", stream=True)
```

**Optional: Use new utilities for advanced scenarios**:

```python
# Advanced: Custom parameter validation
from blossom_ai.generators import ParameterValidator

try:
    ParameterValidator.validate_prompt_length(user_input, 1000, "prompt")
    result = client.text.generate(user_input)
except BlossomError as e:
    print(f"Validation failed: {e}")
```

#### 📚 Documentation

**Updated**:
- Internal architecture improved (see code comments)
- Better type hints throughout
- Clearer separation of V1 and V2 logic

**Coming Soon**:
- Architecture documentation
- Contributor guide updates
- Advanced usage examples

#### 🐛 Bug Fixes

- Fixed potential resource leaks in streaming (responses now always closed)
- Fixed timeout inconsistencies between V1 and V2 streaming
- Fixed Unicode decode errors in chunk-based streaming
- Improved error messages for parameter validation
---

See [V2 Migration Guide](docs/V2_MIGRATION_GUIDE.md) for detailed migration steps.

#### 📊 Feature Comparison

| Feature | V1 | V2 |
|---------|----|----|
| Basic generation | ✅ | ✅ |
| Quality levels | ❌ | ✅ |
| Guidance scale | ❌ | ✅ |
| Negative prompts | ❌ | ✅ |
| Transparent images | ❌ | ✅ |
| Image-to-image | ❌ | ✅ |
| Function calling | ❌ | ✅ |
| Max tokens | ❌ | ✅ |
| Frequency penalty | ❌ | ✅ |
| Presence penalty | ❌ | ✅ |
| Top-P sampling | ❌ | ✅ |
| Temperature | 0-1 | 0-2 |
| Streaming | ✅ | ✅ (improved) |
| JSON mode | ✅ | ✅ (more reliable) |

#### 🎯 Use Cases

**Use V2 when you need:**
- HD quality images
- Fine control over image generation
- Function calling for AI agents
- Advanced text parameters
- Better streaming reliability
- Structured JSON outputs

**Use V1 when you need:**
- Simple, quick integration
- Backward compatibility
- No authentication required
- Basic features are sufficient

#### 🔗 Related Links

- [V2 API Documentation](https://docs.pollinations.ai/v2)
- [Get API Token](https://enter.pollinations.ai)
- [V2 Migration Guide](docs/V2_MIGRATION_GUIDE.md)

---

<div align="center">

**[View Full Documentation](docs/INDEX.md)** • **[GitHub Repository](https://github.com/PrimeevolutionZ/blossom-ai)**

</div>