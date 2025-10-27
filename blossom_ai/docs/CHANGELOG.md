# Changelog

This document tracks the changes and updates across different versions of the Blossom AI SDK.

## v0.2.91 (Latest)

### 📚 Documentation Updates

- **API Reference Fix**: Restored complete parameter tables that were missing in v0.2.8-0.2.9
  - Added full parameter tables for `Blossom` class initialization
  - Added complete parameter documentation for all `image`, `text`, and `audio` methods
  - Added detailed error types and attributes documentation
- **New Documentation Files**:
  - Added `EXAMPLES.md` - Comprehensive practical examples from original documentation
  - Added `INDEX.md` - Central navigation hub for all documentation
- **README Update**: Added link to new `EXAMPLES.md` in documentation section

## v0.2.9

### 🐛 Bug Fixes

- **Critical Path Fix**: Fixed missing `/` in file paths that caused import errors

## v0.2.8

### 🐛 Bug Fixes

- **README Links**: Corrected incorrect documentation links in README.md

## v0.2.7

### ✨ New Features

- **Documentation Restructuring**: The project documentation has been fully modularized and restructured for improved clarity, navigation, and maintainability
- **Updated README**: The main README now serves as a concise project overview with links to the detailed guides

## v0.2.6

### ✨ New Features

- **Enhanced Resource Management**: Implemented proper session cleanup using `atexit` hooks and improved context manager support for both sync and async operations
- **Global Session Registry**: Centralized tracking of all active sessions for better resource control

### 🛠️ Bug Fixes

- Fixed `ResourceWarning` regarding unclosed sessions in certain scenarios
- Improved thread-safety for resource cleanup in complex async environments

## v0.2.5

### ✨ New Features

- **Image URL Generation**: Added the `ai.image.generate_url()` method for instant retrieval of image URLs without downloading bytes. This is significantly faster and more efficient for bot and web integrations
- **Private Generation Support**: Added the `private` parameter to image generation methods

## v0.2.0

### ✨ New Features

- **Initial Release**: Core functionality for Image, Text, and Audio generation
- **Unified API**: Single `Blossom` class for both synchronous and asynchronous operations
- **Streaming Support**: Real-time text generation with built-in timeout protection