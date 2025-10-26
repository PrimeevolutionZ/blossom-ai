# Error Handling

Blossom AI is designed with robust error handling to provide helpful and actionable error messages.

## Types of Errors

The SDK wraps common API and network issues into specific exceptions to make debugging easier.

| Exception Type | Description | Actionable Suggestion |
| :--- | :--- | :--- |
| `BlossomAPIError` | An error occurred on the Pollinations.AI server side (e.g., invalid prompt, rate limit). | Check your prompt, ensure you are within rate limits, or try again later. |
| `BlossomAuthenticationError` | The provided API token is invalid or missing for a protected resource (e.g., Audio Generation). | Ensure you are passing a valid `api_token` when initializing the `Blossom` client. |
| `BlossomTimeoutError` | The request took too long to complete, or streaming stopped receiving data. | For streaming, check your network connection. For long generations, consider increasing the timeout parameter (if available). |
| `BlossomNetworkError` | A network issue prevented the request from reaching the server. | Check your internet connection or firewall settings. |

## Example: Handling API Errors

You should wrap your API calls in `try...except` blocks to handle potential issues gracefully.

```python
from blossom_ai import Blossom
from blossom_ai.exceptions import BlossomAPIError, BlossomAuthenticationError

try:
    with Blossom() as ai:
        # Example of a call that might fail
        result = ai.image.generate("a prompt that violates policy")
        print("Success!")
        
except BlossomAuthenticationError as e:
    print(f"Authentication Failed: {e}")
    print("Hint: You might need to provide a valid API token.")
    
except BlossomAPIError as e:
    print(f"API Error Occurred: {e}")
    print("Hint: Check the error message for details on why the API rejected the request.")
    
except Exception as e:
    print(f"An unexpected error occurred: {e}")
```

## Robustness and Graceful Fallbacks

The client includes built-in mechanisms for graceful fallbacks when underlying API endpoints are temporarily unavailable, but explicit error handling in your application code is always recommended.
