# 🖥️ CLI Interface Guide

Complete guide to using Blossom AI from the command line.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Interactive Mode](#interactive-mode)
- [Command-Line Usage](#command-line-usage)
- [Configuration](#configuration)
- [Examples](#examples)
- [Automation](#automation)

---

## 🌟 Overview

Blossom AI includes a built-in CLI (Command-Line Interface) for:

- ⚡ **Quick Testing** - Test API without writing code
- 🖼️ **Image Generation** - Generate images from terminal
- 💬 **Text Generation** - Generate text from terminal
- 🔍 **Model Discovery** - List available models
- 🤖 **Automation** - Use in scripts and workflows
- 📚 **Interactive Mode** - Explore features with menu

---

## 📦 Installation

The CLI is included with Blossom AI - no extra installation needed!

```bash
pip install eclips-blossom-ai
```

Verify installation:

```bash
python -m blossom_ai.utils.cli --help
```

---

## 🚀 Quick Start

### Launch Interactive Mode

```bash
# Start interactive menu
python -m blossom_ai.utils.cli
```

You'll see:

```
┌─────────────────────────────────────┐
│  🌸 Blossom AI - Interactive CLI   │
├─────────────────────────────────────┤
│  What would you like to do?         │
│                                     │
│  1. 🖼️  Generate Image              │
│  2. 💬 Generate Text                │
│  3. ℹ️  Show Available Models       │
│  4. 🚪 Exit                         │
└─────────────────────────────────────┘

Enter choice (1-4):
```

### Quick Commands

```bash
# Generate image
python -m blossom_ai.utils.cli --image "a sunset" --output sunset.png

# Generate text
python -m blossom_ai.utils.cli --text "Write a haiku"

# With API token
python -m blossom_ai.utils.cli --token YOUR_TOKEN --text "Hello"
```

---

## 🎯 Interactive Mode

### Starting Interactive Mode

```bash
python -m blossom_ai.utils.cli
```

Or with token:

```bash
python -m blossom_ai.utils.cli --token YOUR_TOKEN
```

### Option 1: Generate Image

```
Select: 1

Enter image prompt: a beautiful sunset over mountains
Enter output filename (default: output.png): sunset.png
Enter width (default: 1024): 1920
Enter height (default: 1024): 1080
Enter model (default: flux): flux
Enter quality (low/medium/high/hd, default: medium): hd

⏳ Generating image...
✅ Image saved to: sunset.png
```

### Option 2: Generate Text

```
Select: 2

Enter text prompt: Write a haiku about coding
Enter model (default: openai): openai
Use streaming? (y/n, default: n): y

⏳ Generating text...

AI Response:
Code flows like a stream
Functions dance in memory
Bugs flee from my screen

✅ Generation complete!
```

### Option 3: Show Models

```
Select: 3

📋 Available Image Models:
  - flux (default)
  - turbo
  - gptimage
  ...

📋 Available Text Models:
  - openai (default)
  - openai-fast
  - openai-large
  - deepseek
  ...
```

---

## 💻 Command-Line Usage

### Basic Syntax

```bash
python -m blossom_ai.utils.cli [OPTIONS]
```

### Common Options

| Option            | Description    | Example               |
|-------------------|----------------|-----------------------|
| `--token TOKEN`   | API token      | `--token YOUR_TOKEN`  |
| `--image PROMPT`  | Generate image | `--image "a cat"`     |
| `--text PROMPT`   | Generate text  | `--text "Hello AI"`   |
| `--output FILE`   | Output file    | `--output result.png` |
| `--model MODEL`   | Model name     | `--model flux`        |
| `--width WIDTH`   | Image width    | `--width 1920`        |
| `--height HEIGHT` | Image height   | `--height 1080`       |
| `--quality LEVEL` | Image quality  | `--quality hd`        |
| `--stream`        | Stream text    | `--stream`            |
| `--help`          | Show help      | `--help`              |

### Image Generation

#### Basic Image

```bash
python -m blossom_ai.utils.cli \
  --image "a beautiful landscape" \
  --output landscape.png
```

#### Custom Size

```bash
python -m blossom_ai.utils.cli \
  --image "a robot" \
  --output robot.png \
  --width 512 \
  --height 512
```

#### HD Quality

```bash
python -m blossom_ai.utils.cli \
  --image "a sunset" \
  --output sunset.png \
  --quality hd \
  --width 1920 \
  --height 1080
```

#### Different Model

```bash
python -m blossom_ai.utils.cli \
  --image "abstract art" \
  --output art.png \
  --model turbo
```

### Text Generation

#### Basic Text

```bash
python -m blossom_ai.utils.cli \
  --text "Explain quantum computing"
```

#### With Streaming

```bash
python -m blossom_ai.utils.cli \
  --text "Tell me a story" \
  --stream
```

#### Different Model

```bash
python -m blossom_ai.utils.cli \
  --text "Write a poem" \
  --model openai-fast
```

#### Save to File

```bash
python -m blossom_ai.utils.cli \
  --text "Write an essay" > essay.txt
```

### List Models

```bash
# Show all available models
python -m blossom_ai.utils.cli --models
```

---

## ⚙️ Configuration

### API Token

#### Option 1: Environment Variable (Recommended)

```bash
# Linux/macOS
export POLLINATIONS_API_KEY="your-token-here"

# Windows (Command Prompt)
set POLLINATIONS_API_KEY=your-token-here

# Windows (PowerShell)
$env:POLLINATIONS_API_KEY="your-token-here"
```

Then use CLI without `--token`:

```bash
python -m blossom_ai.utils.cli --text "Hello"
```

#### Option 2: Command-Line Flag

```bash
python -m blossom_ai.utils.cli \
  --token YOUR_TOKEN \
  --text "Hello"
```

#### Option 3: .env File

Create `.env` file:

```bash
POLLINATIONS_API_KEY=your-token-here
```

Then use CLI normally:

```bash
python -m blossom_ai.utils.cli --text "Hello"
```

### Default Settings

Create a config file `~/.blossom_config.json`:

```json
{
  "image_model": "flux",
  "text_model": "openai",
  "image_width": 1024,
  "image_height": 1024,
  "image_quality": "medium",
  "timeout": 60
}
```

---

## 📚 Examples

### Example 1: Generate Multiple Images

```bash
#!/bin/bash

# Generate images for different prompts
prompts=("sunset" "forest" "ocean" "mountain")

for prompt in "${prompts[@]}"; do
    python -m blossom_ai.utils.cli \
        --image "a beautiful $prompt" \
        --output "${prompt}.png" \
        --width 512 \
        --height 512
    echo "✅ Generated: ${prompt}.png"
done
```

### Example 2: Batch Text Generation

```bash
#!/bin/bash

# Generate text for multiple questions
questions=(
    "What is Python?"
    "What is JavaScript?"
    "What is Rust?"
)

for i in "${!questions[@]}"; do
    echo "Question $((i+1)): ${questions[$i]}"
    python -m blossom_ai.utils.cli \
        --text "${questions[$i]}"
    echo "---"
done
```

### Example 3: Image Series

```bash
#!/bin/bash

# Generate numbered series
for i in {1..5}; do
    python -m blossom_ai.utils.cli \
        --image "scene number $i in a story" \
        --output "scene_$i.png" \
        --width 768 \
        --height 768 \
        --quality high
done
```

### Example 4: Daily Wallpaper

```bash
#!/bin/bash

# Generate daily wallpaper
DATE=$(date +%Y-%m-%d)
PROMPT="beautiful nature scene"

python -m blossom_ai.utils.cli \
    --image "$PROMPT" \
    --output "wallpaper_$DATE.png" \
    --width 1920 \
    --height 1080 \
    --quality hd

echo "✅ Wallpaper generated: wallpaper_$DATE.png"
```

### Example 5: Text Processing Pipeline

```bash
#!/bin/bash

# Generate, process, and save
python -m blossom_ai.utils.cli \
    --text "Write a technical article about AI" \
    | tee article.txt \
    | wc -w

echo "✅ Article saved with $(wc -w < article.txt) words"
```

### Example 6: Conditional Generation

```bash
#!/bin/bash

# Generate only if file doesn't exist
IMAGE="generated.png"

if [ ! -f "$IMAGE" ]; then
    python -m blossom_ai.utils.cli \
        --image "a unique artwork" \
        --output "$IMAGE"
    echo "✅ Generated: $IMAGE"
else
    echo "⚠️ File already exists: $IMAGE"
fi
```

---

## 🤖 Automation

### Cron Jobs (Linux/macOS)

```bash
# Edit crontab
crontab -e

# Add job (runs daily at 8 AM)
0 8 * * * /usr/bin/python3 -m blossom_ai.utils.cli --image "daily inspiration" --output ~/wallpaper.png

# Add job (runs every hour)
0 * * * * /usr/bin/python3 -m blossom_ai.utils.cli --text "Hourly summary" >> ~/summaries.txt
```

### Windows Task Scheduler

Create `generate_image.bat`:

```batch
@echo off
python -m blossom_ai.utils.cli --image "daily image" --output C:\Images\daily.png
```

Schedule in Task Scheduler:
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (daily, hourly, etc.)
4. Action: Start a program → `generate_image.bat`

### GitHub Actions

`.github/workflows/generate.yml`:

```yaml
name: Generate Content

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
  workflow_dispatch:

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install Blossom AI
        run: pip install eclips-blossom-ai
      
      - name: Generate Image
        env:
          POLLINATIONS_API_KEY: ${{ secrets.POLLINATIONS_API_KEY }}
        run: |
          python -m blossom_ai.utils.cli \
            --image "daily artwork" \
            --output daily.png
      
      - name: Upload Artifact
        uses: actions/upload-artifact@v3
        with:
          name: generated-image
          path: daily.png
```

### Docker Container

`Dockerfile`:

```dockerfile
FROM python:3.10-slim

RUN pip install eclips-blossom-ai

ENV POLLINATIONS_API_KEY=""

ENTRYPOINT ["python", "-m", "blossom_ai.utils.cli"]
```

Build and run:

```bash
# Build
docker build -t blossom-cli .

# Run
docker run -e POLLINATIONS_API_KEY="your-token" \
  blossom-cli --text "Hello from Docker"
```

### Shell Alias (Quick Access)

Add to `~/.bashrc` or `~/.zshrc`:

```bash
# Short alias
alias bai='python -m blossom_ai.utils.cli'

# Specific commands
alias bai-img='python -m blossom_ai.utils.cli --image'
alias bai-txt='python -m blossom_ai.utils.cli --text'
```

Use it:

```bash
bai-img "a sunset" --output sunset.png
bai-txt "Write a poem"
```

### Makefile Integration

`Makefile`:

```makefile
.PHONY: generate-images generate-text

generate-images:
	python -m blossom_ai.utils.cli --image "scene 1" --output scene1.png
	python -m blossom_ai.utils.cli --image "scene 2" --output scene2.png

generate-text:
	python -m blossom_ai.utils.cli --text "Summary" > summary.txt

all: generate-images generate-text
```

Run:

```bash
make generate-images
make generate-text
make all
```

---

## 🎓 Tips & Tricks

### 1. Use Quotes for Prompts

```bash
# ✅ Good - with quotes
python -m blossom_ai.utils.cli --image "a beautiful sunset"

# ❌ Bad - without quotes (shell splits it)
python -m blossom_ai.utils.cli --image a beautiful sunset
```

### 2. Redirect Output

```bash
# Save text to file
python -m blossom_ai.utils.cli --text "Essay" > essay.txt

# Append to file
python -m blossom_ai.utils.cli --text "More text" >> log.txt

# Suppress output
python -m blossom_ai.utils.cli --image "test" --output test.png > /dev/null 2>&1
```

### 3. Error Handling in Scripts

```bash
#!/bin/bash

if python -m blossom_ai.utils.cli --image "test" --output test.png; then
    echo "✅ Success"
else
    echo "❌ Failed"
    exit 1
fi
```

### 4. Progress Indicators

```bash
#!/bin/bash

echo -n "Generating image... "
python -m blossom_ai.utils.cli --image "test" --output test.png > /dev/null 2>&1
echo "✅ Done"
```

### 5. Parallel Generation

```bash
#!/bin/bash

# Generate multiple images in parallel
for i in {1..3}; do
    python -m blossom_ai.utils.cli \
        --image "scene $i" \
        --output "scene_$i.png" &
done

# Wait for all to complete
wait
echo "✅ All images generated"
```

---

## 🛡️ Troubleshooting

### Issue: Command Not Found

```bash
# Try full path
python3 -m blossom_ai.utils.cli --help

# Or check Python
which python
python --version
```

### Issue: API Token Not Found

```bash
# Check if env var is set
echo $POLLINATIONS_API_KEY

# Set it
export POLLINATIONS_API_KEY="your-token"

# Or use --token flag
python -m blossom_ai.utils.cli --token YOUR_TOKEN --text "test"
```

### Issue: Output File Permission Error

```bash
# Check directory permissions
ls -la

# Use absolute path
python -m blossom_ai.utils.cli \
    --image "test" \
    --output /absolute/path/image.png
```

### Issue: Timeout

```bash
# Increase timeout (if supported)
python -m blossom_ai.utils.cli \
    --image "complex scene" \
    --output result.png \
    --timeout 120
```

---

## 📚 Related Documentation

- **[Quick Start](QUICKSTART.md)** - Get started with Blossom AI
- **[Image Generation](IMAGE_GENERATION.md)** - Image generation guide
- **[Text Generation](TEXT_GENERATION.md)** - Text generation guide
- **[API Reference](API_REFERENCE.md)** - Complete API documentation

---

## 🆘 Need Help?

- 📖 **Documentation:** [INDEX.md](INDEX.md)
- 🐛 **Report Bug:** [GitHub Issues](https://github.com/PrimeevolutionZ/blossom-ai/issues)
- 💬 **Ask Question:** [GitHub Discussions](https://github.com/PrimeevolutionZ/blossom-ai/discussions)

---

<div align="center">

**Made with 🌸 by the [Eclips Team](https://github.com/PrimeevolutionZ)**

[← Back to Index](INDEX.md) | [Next: Error Handling →](ERROR_HANDLING.md)

</div>