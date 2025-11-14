# 🤖 Telegram Bot Tutorial

> **Build an AI-powered Telegram bot with image generation using Blossom AI V2 API**

Create a Telegram bot that generates AI images and provides text responses using the Blossom AI library.

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Basic Bot](#basic-bot)
- [Image Generation](#image-generation)
- [Text Generation](#text-generation)
- [Advanced Features](#advanced-features)
- [Error Handling](#error-handling)
- [Deployment](#deployment)
- [Best Practices](#best-practices)

---

## 🎯 Prerequisites

Before starting, ensure you have:

- Python 3.8 or higher
- A Telegram account
- Basic Python knowledge
- Blossom AI installed (`pip install eclips-blossom-ai`)

### Required Libraries

```bash
pip install eclips-blossom-ai
pip install python-telegram-bot
pip install python-dotenv
```

---

## 🚀 Setup

### 1. Create Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Choose a name (e.g., "AI Art Generator")
4. Choose a username (must end with "bot", e.g., "my_ai_art_bot")
5. Copy the **API Token** (keep it secret!)

### 2. Configure Bot Settings

Talk to @BotFather:

```
/setcommands
```

Then paste:

```
start - Start the bot
help - Show help message
generate - Generate an AI image
imagine - Generate HD image
chat - Chat with AI
```

### 3. Get API Tokens

- **Telegram Bot Token**: From @BotFather
- **Blossom AI Token**: Get yours at [enter.pollinations.ai](https://enter.pollinations.ai)

### 4. Create Environment File

Create a `.env` file:

```env
# .env
TELEGRAM_TOKEN=your_telegram_bot_token_here
BLOSSOM_TOKEN=your_blossom_api_token_here
```

---

## 🤖 Basic Bot

### Simple Telegram Bot

Create `bot.py`:

```python
import os
import io
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from blossom_ai import Blossom
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
BLOSSOM_TOKEN = os.getenv("BLOSSOM_TOKEN")

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Blossom AI client
ai_client = Blossom(api_token=BLOSSOM_TOKEN)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message"""
    welcome_text = """
🌸 *Welcome to AI Art Bot!*

I can generate AI images and chat with you.

*Commands:*
/generate <prompt> - Generate an image
/chat <message> - Chat with AI
/help - Show this message

*Example:*
/generate a cute cat painting
    """
    await update.message.reply_text(
        welcome_text,
        parse_mode='Markdown'
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message"""
    await start(update, context)


async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Generate AI image from prompt
    Usage: /generate a beautiful sunset
    """
    # Get prompt from message
    prompt = ' '.join(context.args)
    
    if not prompt:
        await update.message.reply_text(
            "❌ Please provide a prompt!\n"
            "Example: /generate a cute cat"
        )
        return
    
    # Send "generating" message
    status_msg = await update.message.reply_text("🎨 Generating your image...")
    
    try:
        # Generate image
        image_data = await ai_client.image.generate(
            prompt=prompt,
            width=512,
            height=512,
            model="flux",
            enhance=True
        )
        
        # Send image
        await update.message.reply_photo(
            photo=io.BytesIO(image_data),
            caption=f"✨ Generated: *{prompt}*",
            parse_mode='Markdown'
        )
        
        # Delete status message
        await status_msg.delete()
        
    except Exception as e:
        await status_msg.edit_text(f"❌ Error: {str(e)}")
        logger.error(f"Generation error: {e}")


async def chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Chat with AI
    Usage: /chat Hello, how are you?
    """
    message = ' '.join(context.args)
    
    if not message:
        await update.message.reply_text(
            "❌ Please provide a message!\n"
            "Example: /chat What is AI?"
        )
        return
    
    # Send "thinking" message
    status_msg = await update.message.reply_text("💭 Thinking...")
    
    try:
        # Generate response
        response = await ai_client.text.generate(
            prompt=message,
            model="openai"
        )
        
        # Send response
        await update.message.reply_text(response)
        
        # Delete status message
        await status_msg.delete()
        
    except Exception as e:
        await status_msg.edit_text(f"❌ Error: {str(e)}")
        logger.error(f"Chat error: {e}")


def main():
    """Start the bot"""
    # Create application
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("generate", generate_image))
    app.add_handler(CommandHandler("chat", chat_command))
    
    # Start bot
    logger.info("🤖 Bot starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
```

### Run the Bot

```bash
python bot.py
```

### Test Commands

In Telegram:

```
/start
/generate a beautiful sunset
/chat What is artificial intelligence?
```

---

## 🎨 Image Generation

### Advanced Image Generation

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def imagine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Generate HD image with options
    Usage: /imagine a dragon
    """
    prompt = ' '.join(context.args)
    
    if not prompt:
        await update.message.reply_text(
            "❌ Please provide a prompt!\n"
            "Example: /imagine a majestic dragon"
        )
        return
    
    # Show quality selection keyboard
    keyboard = [
        [
            InlineKeyboardButton("Low (256px)", callback_data=f"gen_low_{prompt}"),
            InlineKeyboardButton("Medium (512px)", callback_data=f"gen_medium_{prompt}")
        ],
        [
            InlineKeyboardButton("High (768px)", callback_data=f"gen_high_{prompt}"),
            InlineKeyboardButton("HD (1024px)", callback_data=f"gen_hd_{prompt}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"🎨 Select quality for:\n*{prompt}*",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses"""
    query = update.callback_query
    await query.answer()
    
    # Parse callback data
    data = query.data
    
    if data.startswith("gen_"):
        parts = data.split("_", 2)
        quality = parts[1]
        prompt = parts[2]
        
        # Map quality to size
        sizes = {
            "low": 256,
            "medium": 512,
            "high": 768,
            "hd": 1024
        }
        size = sizes.get(quality, 512)
        
        # Update message
        await query.edit_message_text(
            f"🎨 Generating *{quality}* quality image...",
            parse_mode='Markdown'
        )
        
        try:
            # Generate image
            image_data = await ai_client.image.generate(
                prompt=prompt,
                width=size,
                height=size,
                quality=quality,
                model="flux",
                enhance=True
            )
            
            # Send image
            await query.message.reply_photo(
                photo=io.BytesIO(image_data),
                caption=f"✨ *{prompt}*\nQuality: {quality} ({size}x{size})",
                parse_mode='Markdown'
            )
            
            # Delete selection message
            await query.message.delete()
            
        except Exception as e:
            await query.edit_message_text(f"❌ Error: {str(e)}")


# Add handler in main()
app.add_handler(CallbackQueryHandler(button_callback))
```

### Batch Generation

```python
async def batch_generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Generate multiple images
    Usage: /batch 3 a cat
    """
    if len(context.args) < 2:
        await update.message.reply_text(
            "❌ Usage: /batch <count> <prompt>\n"
            "Example: /batch 3 a cute cat"
        )
        return
    
    try:
        count = int(context.args[0])
        prompt = ' '.join(context.args[1:])
    except ValueError:
        await update.message.reply_text("❌ Count must be a number!")
        return
    
    if count > 5:
        await update.message.reply_text("❌ Maximum 5 images per batch!")
        return
    
    status_msg = await update.message.reply_text(
        f"🎨 Generating {count} images..."
    )
    
    try:
        # Generate multiple images
        import asyncio
        
        tasks = [
            ai_client.image.generate(
                prompt=prompt,
                seed=i,
                width=512,
                height=512,
                model="flux"
            )
            for i in range(count)
        ]
        
        results = await asyncio.gather(*tasks)
        
        # Send images as media group
        media = [
            telegram.InputMediaPhoto(
                media=io.BytesIO(data),
                caption=f"Variation #{i+1}" if i == 0 else ""
            )
            for i, data in enumerate(results)
        ]
        
        await update.message.reply_media_group(media=media)
        await status_msg.delete()
        
    except Exception as e:
        await status_msg.edit_text(f"❌ Error: {str(e)}")
```

---

## 💬 Text Generation

### Conversational AI

```python
# Store conversation history per user
user_conversations = {}

async def chat_with_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Chat with conversation history
    Usage: /talk Hello!
    """
    user_id = update.effective_user.id
    message = ' '.join(context.args)
    
    if not message:
        await update.message.reply_text(
            "❌ Please provide a message!\n"
            "Example: /talk Tell me a joke"
        )
        return
    
    # Initialize conversation if needed
    if user_id not in user_conversations:
        user_conversations[user_id] = []
    
    # Add user message to history
    user_conversations[user_id].append({
        "role": "user",
        "content": message
    })
    
    # Send "thinking" message
    status_msg = await update.message.reply_text("💭 Thinking...")
    
    try:
        # Generate response with history
        response = await ai_client.text.chat(
            messages=user_conversations[user_id],
            model="openai"
        )
        
        # Add assistant response to history
        user_conversations[user_id].append({
            "role": "assistant",
            "content": response
        })
        
        # Limit history to last 10 messages
        if len(user_conversations[user_id]) > 10:
            user_conversations[user_id] = user_conversations[user_id][-10:]
        
        # Send response
        await update.message.reply_text(response)
        await status_msg.delete()
        
    except Exception as e:
        await status_msg.edit_text(f"❌ Error: {str(e)}")


async def clear_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear conversation history"""
    user_id = update.effective_user.id
    
    if user_id in user_conversations:
        del user_conversations[user_id]
        await update.message.reply_text("✅ Conversation history cleared!")
    else:
        await update.message.reply_text("ℹ️ No conversation history to clear")
```

### Streaming Responses

```python
async def stream_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Stream AI response (shows typing while generating)
    Usage: /stream Write a story
    """
    prompt = ' '.join(context.args)
    
    if not prompt:
        await update.message.reply_text("❌ Please provide a prompt!")
        return
    
    # Send initial message
    response_msg = await update.message.reply_text("💭 Generating...")
    
    try:
        full_response = ""
        
        # Stream response
        async for chunk in await ai_client.text.generate(
            prompt=prompt,
            stream=True,
            model="openai"
        ):
            full_response += chunk
            
            # Update message every 50 characters to reduce API calls
            if len(full_response) % 50 == 0:
                try:
                    await response_msg.edit_text(full_response)
                except telegram.error.BadRequest:
                    # Ignore if message hasn't changed
                    pass
        
        # Final update
        await response_msg.edit_text(full_response)
        
    except Exception as e:
        await response_msg.edit_text(f"❌ Error: {str(e)}")
```

---

## ⚡ Advanced Features

### 1. Inline Mode

```python
from telegram import InlineQueryResultPhoto
import uuid

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle inline queries
    Usage: @your_bot_name a cat
    """
    query = update.inline_query.query
    
    if not query:
        return
    
    try:
        # Generate image URL (faster than sending bytes)
        url = await ai_client.image.generate_url(
            prompt=query,
            width=512,
            height=512,
            model="flux"
        )
        
        # Create result
        results = [
            InlineQueryResultPhoto(
                id=str(uuid.uuid4()),
                photo_url=url,
                thumbnail_url=url,
                title=f"Generate: {query}",
                description="Click to generate this image"
            )
        ]
        
        await update.inline_query.answer(results, cache_time=0)
        
    except Exception as e:
        logger.error(f"Inline query error: {e}")


# Add handler in main()
app.add_handler(InlineQueryHandler(inline_query))
```

### 2. User Statistics

```python
import json
from datetime import datetime

# Store user stats
def load_stats():
    try:
        with open('user_stats.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_stats(stats):
    with open('user_stats.json', 'w') as f:
        json.dump(stats, f, indent=2)

user_stats = load_stats()

def track_usage(user_id, action):
    """Track user actions"""
    user_id = str(user_id)
    
    if user_id not in user_stats:
        user_stats[user_id] = {
            "images": 0,
            "chats": 0,
            "first_seen": datetime.now().isoformat(),
            "last_seen": datetime.now().isoformat()
        }
    
    user_stats[user_id][action] += 1
    user_stats[user_id]["last_seen"] = datetime.now().isoformat()
    save_stats(user_stats)


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user statistics"""
    user_id = str(update.effective_user.id)
    
    if user_id not in user_stats:
        await update.message.reply_text("ℹ️ No statistics yet!")
        return
    
    stats = user_stats[user_id]
    
    text = f"""
📊 *Your Statistics*

🖼️ Images generated: {stats['images']}
💬 Chat messages: {stats['chats']}
📅 Member since: {stats['first_seen'][:10]}
⏰ Last active: {stats['last_seen'][:10]}
    """
    
    await update.message.reply_text(text, parse_mode='Markdown')


# Update generate_image to track usage
async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ... existing code ...
    
    # Track usage
    track_usage(update.effective_user.id, "images")
    
    # ... rest of code ...
```

### 3. Image History

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Store user's last generated images
user_image_history = {}

async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show image generation history"""
    user_id = update.effective_user.id
    
    if user_id not in user_image_history or not user_image_history[user_id]:
        await update.message.reply_text("ℹ️ No history yet!")
        return
    
    history = user_image_history[user_id][-5:]  # Last 5 images
    
    text = "🖼️ *Your Recent Images:*\n\n"
    
    for i, item in enumerate(reversed(history), 1):
        text += f"{i}. `{item['prompt']}`\n"
        text += f"   🌱 Seed: {item['seed']}\n\n"
    
    keyboard = [
        [InlineKeyboardButton(
            f"Regenerate #{i}",
            callback_data=f"regen_{item['seed']}_{item['prompt']}"
        )]
        for i, item in enumerate(reversed(history), 1)
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


# Update generate_image to save history
async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ... generate image with seed ...
    
    # Save to history
    user_id = update.effective_user.id
    if user_id not in user_image_history:
        user_image_history[user_id] = []
    
    user_image_history[user_id].append({
        "prompt": prompt,
        "seed": seed,
        "timestamp": datetime.now().isoformat()
    })
    
    # Keep only last 20
    user_image_history[user_id] = user_image_history[user_id][-20:]
```

---

## 🛡️ Error Handling

### Comprehensive Error Handler

```python
from blossom_ai import BlossomError, ValidationError, RateLimitError
from telegram.error import TelegramError

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Exception: {context.error}")
    
    # Determine error type and message
    if isinstance(context.error, ValidationError):
        message = f"❌ Invalid input: {context.error.message}"
    
    elif isinstance(context.error, RateLimitError):
        message = f"⏳ Rate limited! Please try again in {context.error.retry_after}s"
    
    elif isinstance(context.error, BlossomError):
        message = f"❌ API Error: {context.error.message}"
    
    elif isinstance(context.error, TelegramError):
        message = f"❌ Telegram Error: {str(context.error)}"
    
    else:
        message = "❌ An unexpected error occurred. Please try again."
    
    # Send error message to user
    try:
        if update and update.effective_message:
            await update.effective_message.reply_text(message)
    except Exception as e:
        logger.error(f"Could not send error message: {e}")


# Add error handler in main()
app.add_error_handler(error_handler)
```

---

## 🚀 Deployment

### Deploy with systemd (Linux)

1. **Create service file** `/etc/systemd/system/telegram-bot.service`:

```ini
[Unit]
Description=Telegram AI Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/bot
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

2. **Enable and start:**

```bash
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
sudo systemctl status telegram-bot
```

### Deploy with Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
```

Build and run:

```bash
docker build -t telegram-bot .
docker run -d --name telegram-bot \
  -e TELEGRAM_TOKEN=xxx \
  -e BLOSSOM_TOKEN=xxx \
  --restart unless-stopped \
  telegram-bot
```

### Deploy to Heroku

```bash
heroku create your-bot-name
heroku config:set TELEGRAM_TOKEN=xxx
heroku config:set BLOSSOM_TOKEN=xxx
git push heroku main
```

---

## 📝 Best Practices

### 1. Resource Management

```python
async def shutdown(application: Application):
    """Cleanup on shutdown"""
    await ai_client.close()
    logger.info("Bot stopped")

# In main()
app = Application.builder().token(TELEGRAM_TOKEN).build()
app.post_shutdown = shutdown
```

### 2. Rate Limiting

```python
from functools import wraps
import time

# Simple rate limiter
user_last_request = {}

def rate_limit(seconds=5):
    """Rate limit decorator"""
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user_id = update.effective_user.id
            now = time.time()
            
            if user_id in user_last_request:
                elapsed = now - user_last_request[user_id]
                if elapsed < seconds:
                    remaining = seconds - elapsed
                    await update.message.reply_text(
                        f"⏳ Please wait {remaining:.1f}s before next request"
                    )
                    return
            
            user_last_request[user_id] = now
            return await func(update, context)
        
        return wrapper
    return decorator


@rate_limit(seconds=10)
async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ... generation code ...
    pass
```

### 3. Logging

```python
import logging
from logging.handlers import RotatingFileHandler

# Setup file logging
handler = RotatingFileHandler(
    'bot.log',
    maxBytes=10*1024*1024,  # 10 MB
    backupCount=5
)
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))

logger.addHandler(handler)
```

---

## 🎯 Complete Example

Full-featured bot with all concepts:

```python
import os
import io
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)
from blossom_ai import Blossom
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
BLOSSOM_TOKEN = os.getenv("BLOSSOM_TOKEN")

ai_client = Blossom(api_token=BLOSSOM_TOKEN)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎨 Generate Image", callback_data="menu_generate")],
        [InlineKeyboardButton("💬 Chat with AI", callback_data="menu_chat")],
        [InlineKeyboardButton("ℹ️ Help", callback_data="menu_help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🌸 *Welcome to AI Bot!*\n\nWhat would you like to do?",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = ' '.join(context.args)
    if not prompt:
        await update.message.reply_text("❌ Usage: /generate <prompt>")
        return
    
    status = await update.message.reply_text("🎨 Generating...")
    
    try:
        image_data = await ai_client.image.generate(
            prompt=prompt,
            width=512,
            height=512,
            model="flux"
        )
        
        await update.message.reply_photo(
            photo=io.BytesIO(image_data),
            caption=f"✨ *{prompt}*",
            parse_mode='Markdown'
        )
        await status.delete()
    
    except Exception as e:
        await status.edit_text(f"❌ Error: {str(e)}")


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate))
    
    app.run_polling()


if __name__ == "__main__":
    main()
```

---

## 📚 Additional Resources

- [python-telegram-bot Documentation](https://python-telegram-bot.readthedocs.io/)
- [Blossom AI Documentation](INDEX.md)
- [Telegram Bot API](https://core.telegram.org/bots/api)

---

**Made with 🌸 by the Eclips Team**

[← Back to Index](INDEX.md) | [Next: Web Application →](WEB_APP.md)