# Changelog

This document tracks the changes and updates across different versions of the Blossom AI SDK.
## v0.2.7 (Latest)

### ✨ New Features

- **Documentation Restructuring**: The project documentation has been fully modularized and restructured for improved clarity, navigation, and maintainability.
- **Updated README**: The main README now serves as a concise project overview with links to the detailed guides.

## v0.2.6 

### ✨ New Features

- **Enhanced Resource Management**: Implemented proper session cleanup using `atexit` hooks and improved context manager support for both sync and async operations.
- **Global Session Registry**: Centralized tracking of all active sessions for better resource control.

### 🐛 Bug Fixes

- Fixed `ResourceWarning` regarding unclosed sessions in certain scenarios.
- Improved thread-safety for resource cleanup in complex async environments.

## v0.2.5

### ✨ New Features

- **Image URL Generation**: Added the `ai.image.generate_url()` method for instant retrieval of image URLs without downloading bytes. This is significantly faster and more efficient for bot and web integrations.
- **Private Generation Support**: Added the `private` parameter to image generation methods.

## v0.2.0

### ✨ New Features

- **Initial Release**: Core functionality for Image, Text, and Audio generation.
- **Unified API**: Single `Blossom` class for both synchronous and asynchronous operations.
- **Streaming Support**: Real-time text generation with built-in timeout protection.
