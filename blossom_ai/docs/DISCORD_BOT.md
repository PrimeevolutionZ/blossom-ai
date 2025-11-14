# 🤖 Discord Bot Tutorial

> **Build an AI-powered Discord bot with image generation using Blossom AI V2 API**

Learn how to create a Discord bot that generates AI images on demand using the Blossom AI library.

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Basic Bot](#basic-bot)
- [Image Generation Commands](#image-generation-commands)
- [Advanced Features](#advanced-features)
- [Error Handling](#error-handling)
- [Deployment](#deployment)
- [Best Practices](#best-practices)

---

## 🎯 Prerequisites

Before starting, ensure you have:

- Python 3.8 or higher
- A Discord account
- Basic Python knowledge
- Blossom AI installed (`pip install eclips-blossom-ai`)

### Required Libraries

```bash
pip install eclips-blossom-ai
pip install discord.py
pip install python-dotenv
```

---

## 🚀 Setup

### 1. Create Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"**
3. Give it a name (e.g., "AI Image Bot")
4. Go to **"Bot"** section
5. Click **"Add Bot"**
6. Copy the **Bot Token** (keep it secret!)
7. Enable **Message Content Intent** under "Privileged Gateway Intents"

### 2. Invite Bot to Server

1. Go to **"OAuth2"** → **"URL Generator"**
2. Select scopes: `bot`, `applications.commands`
3. Select permissions:
   - Send Messages
   - Attach Files
   - Use Slash Commands
4. Copy the generated URL and open it in browser
5. Select your server and authorize

### 3. Get API Tokens

- **Discord Bot Token**: From Discord Developer Portal
- **Blossom AI Token**: Get yours at [enter.pollinations.ai](https://enter.pollinations.ai)

### 4. Create Environment File

Create a `.env` file:

```env
# .env
DISCORD_TOKEN=your_discord_bot_token_here
BLOSSOM_TOKEN=your_blossom_api_token_here
```

---

## 🤖 Basic Bot

### Simple Discord Bot with Image Generation

Create `bot.py`:

```python
import discord
from discord.ext import commands
from blossom_ai import Blossom
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
BLOSSOM_TOKEN = os.getenv("BLOSSOM_TOKEN")

# Create bot with intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize Blossom AI client (reuse connection)
ai_client = Blossom(api_token=BLOSSOM_TOKEN)


@bot.event
async def on_ready():
    """Bot startup event"""
    print(f"✅ Bot is ready! Logged in as {bot.user}")
    print(f"📊 Connected to {len(bot.guilds)} server(s)")


@bot.command(name="generate")
async def generate_image(ctx, *, prompt: str):
    """
    Generate an AI image
    Usage: !generate a cute cat
    """
    # Send "thinking" message
    thinking_msg = await ctx.send("🎨 Generating your image...")
    
    try:
        # Generate image using Blossom AI
        image_data = await ai_client.image.generate(
            prompt=prompt,
            width=512,
            height=512,
            model="flux"
        )
        
        # Create Discord file from bytes
        file = discord.File(
            fp=io.BytesIO(image_data),
            filename="generated.png"
        )
        
        # Send image
        await ctx.send(
            content=f"✨ Generated: **{prompt}**",
            file=file
        )
        
        # Delete thinking message
        await thinking_msg.delete()
        
    except Exception as e:
        await thinking_msg.edit(content=f"❌ Error: {str(e)}")


@bot.command(name="ping")
async def ping(ctx):
    """Check bot latency"""
    await ctx.send(f"🏓 Pong! Latency: {round(bot.latency * 1000)}ms")


# Run bot
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
```

### Run the Bot

```bash
python bot.py
```

### Test Commands

In your Discord server:

```
!ping
!generate a sunset over mountains
!generate a cute robot painting
```

---

## 🎨 Image Generation Commands

### Command with Options

```python
@bot.command(name="img")
async def generate_with_options(ctx, *, prompt: str):
    """
    Generate image with quality options
    Usage: !img a dragon --hd --seed 42
    """
    # Parse arguments
    parts = prompt.split("--")
    actual_prompt = parts[0].strip()
    
    # Default parameters
    quality = "medium"
    seed = None
    width = 512
    height = 512
    
    # Parse options
    for part in parts[1:]:
        part = part.strip().lower()
        if part == "hd":
            quality = "hd"
            width = 1024
            height = 1024
        elif part.startswith("seed"):
            seed = int(part.split()[1])
        elif part.startswith("wide"):
            width = 1024
            height = 576
    
    # Send status
    status = await ctx.send(f"🎨 Generating **{quality}** quality image...")
    
    try:
        # Generate image
        image_data = await ai_client.image.generate(
            prompt=actual_prompt,
            width=width,
            height=height,
            quality=quality,
            seed=seed,
            model="flux",
            enhance=True
        )
        
        # Send result
        file = discord.File(
            fp=io.BytesIO(image_data),
            filename=f"img_{quality}.png"
        )
        
        embed = discord.Embed(
            title="✨ Generated Image",
            description=actual_prompt,
            color=discord.Color.blue()
        )
        embed.add_field(name="Quality", value=quality, inline=True)
        embed.add_field(name="Size", value=f"{width}x{height}", inline=True)
        if seed:
            embed.add_field(name="Seed", value=seed, inline=True)
        embed.set_image(url="attachment://img_" + quality + ".png")
        
        await ctx.send(embed=embed, file=file)
        await status.delete()
        
    except Exception as e:
        await status.edit(content=f"❌ Generation failed: {str(e)}")
```

### Usage Examples

```
!img a beautiful landscape
!img a dragon --hd
!img a cat --seed 42
!img sunset --wide
!img cityscape --hd --seed 12345
```

---

## ⚡ Advanced Features

### 1. Slash Commands (Modern Discord)

```python
import discord
from discord import app_commands

@bot.tree.command(name="generate", description="Generate an AI image")
@app_commands.describe(
    prompt="What to generate",
    quality="Image quality (low/medium/high/hd)",
    seed="Seed for reproducibility (optional)"
)
async def slash_generate(
    interaction: discord.Interaction,
    prompt: str,
    quality: str = "medium",
    seed: int = None
):
    """Slash command for image generation"""
    await interaction.response.defer()
    
    try:
        # Set dimensions based on quality
        sizes = {
            "low": (256, 256),
            "medium": (512, 512),
            "high": (768, 768),
            "hd": (1024, 1024)
        }
        width, height = sizes.get(quality, (512, 512))
        
        # Generate image
        image_data = await ai_client.image.generate(
            prompt=prompt,
            width=width,
            height=height,
            quality=quality,
            seed=seed,
            model="flux"
        )
        
        # Send result
        file = discord.File(
            fp=io.BytesIO(image_data),
            filename="generated.png"
        )
        
        await interaction.followup.send(
            content=f"✨ **{prompt}**",
            file=file
        )
        
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}")


# Sync slash commands on startup
@bot.event
async def on_ready():
    await bot.tree.sync()
    print("✅ Slash commands synced!")
```

### 2. Image Variations

```python
@bot.command(name="variation")
async def create_variation(ctx, seed: int):
    """
    Create variation of previous image using same seed
    Usage: !variation 42
    """
    # Store last prompt in bot memory (add to bot class)
    if not hasattr(bot, 'last_prompt'):
        await ctx.send("❌ No previous image to vary!")
        return
    
    await ctx.send(f"🎨 Creating variation with seed {seed}...")
    
    try:
        image_data = await ai_client.image.generate(
            prompt=bot.last_prompt,
            seed=seed,
            width=512,
            height=512,
            model="flux"
        )
        
        file = discord.File(
            fp=io.BytesIO(image_data),
            filename=f"variation_{seed}.png"
        )
        
        await ctx.send(
            content=f"✨ Variation #{seed}",
            file=file
        )
        
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")
```

### 3. Batch Generation

```python
@bot.command(name="batch")
async def batch_generate(ctx, count: int, *, prompt: str):
    """
    Generate multiple images
    Usage: !batch 3 a cat
    """
    if count > 5:
        await ctx.send("❌ Maximum 5 images per batch!")
        return
    
    status = await ctx.send(f"🎨 Generating {count} images...")
    
    try:
        # Generate multiple images in parallel
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
        
        # Send all images
        files = [
            discord.File(
                fp=io.BytesIO(data),
                filename=f"img_{i}.png"
            )
            for i, data in enumerate(results)
        ]
        
        await ctx.send(
            content=f"✨ Generated {count} images: **{prompt}**",
            files=files
        )
        await status.delete()
        
    except Exception as e:
        await status.edit(content=f"❌ Error: {str(e)}")
```

---

## 🛡️ Error Handling

### Comprehensive Error Handling

```python
from blossom_ai import BlossomError, ValidationError, RateLimitError

@bot.command(name="safe_generate")
async def safe_generate(ctx, *, prompt: str):
    """Generate with proper error handling"""
    status = await ctx.send("🎨 Generating...")
    
    try:
        # Validate prompt length
        if len(prompt) > 200:
            await status.edit(content="❌ Prompt too long! (max 200 chars)")
            return
        
        # Generate image
        image_data = await ai_client.image.generate(
            prompt=prompt,
            width=512,
            height=512,
            model="flux"
        )
        
        # Check file size (Discord limit: 8MB)
        if len(image_data) > 8 * 1024 * 1024:
            await status.edit(content="❌ Image too large for Discord!")
            return
        
        # Send result
        file = discord.File(
            fp=io.BytesIO(image_data),
            filename="generated.png"
        )
        await ctx.send(file=file)
        await status.delete()
        
    except ValidationError as e:
        await status.edit(content=f"❌ Invalid input: {e.message}")
    
    except RateLimitError as e:
        await status.edit(
            content=f"⏳ Rate limited! Try again in {e.retry_after}s"
        )
    
    except BlossomError as e:
        await status.edit(content=f"❌ API Error: {e.message}")
    
    except discord.HTTPException as e:
        await status.edit(content=f"❌ Discord Error: {str(e)}")
    
    except Exception as e:
        await status.edit(content=f"❌ Unexpected error: {str(e)}")
        print(f"Error details: {e}")


# Global error handler
@bot.event
async def on_command_error(ctx, error):
    """Handle command errors globally"""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing argument: {error.param.name}")
    
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found! Use `!help` for available commands")
    
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ Cooldown! Try again in {error.retry_after:.1f}s")
    
    else:
        await ctx.send(f"❌ Error: {str(error)}")
        print(f"Unhandled error: {error}")
```

---

## 🚀 Deployment

### Deploy to Heroku

1. **Create `Procfile`:**

```
worker: python bot.py
```

2. **Create `requirements.txt`:**

```bash
pip freeze > requirements.txt
```

3. **Create `runtime.txt`:**

```
python-3.11.0
```

4. **Deploy:**

```bash
# Install Heroku CLI
heroku login
heroku create your-bot-name
heroku config:set DISCORD_TOKEN=your_token
heroku config:set BLOSSOM_TOKEN=your_token
git push heroku main
heroku ps:scale worker=1
```

### Deploy to Railway

1. Connect GitHub repository
2. Add environment variables
3. Deploy automatically on push

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
docker build -t discord-bot .
docker run -e DISCORD_TOKEN=xxx -e BLOSSOM_TOKEN=xxx discord-bot
```

---

## 📝 Best Practices

### 1. Resource Management

```python
# Use context manager for cleanup
async def main():
    async with Blossom(api_token=BLOSSOM_TOKEN) as ai_client:
        # Use ai_client here
        await bot.start(DISCORD_TOKEN)

# Proper shutdown
@bot.event
async def on_disconnect():
    await ai_client.close()
```

### 2. Rate Limiting

```python
from discord.ext import commands
import asyncio

# Add cooldown to commands
@bot.command(name="generate")
@commands.cooldown(1, 10, commands.BucketType.user)  # 1 use per 10s per user
async def generate(ctx, *, prompt: str):
    # ... generation code
    pass
```

### 3. Logging

```python
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('discord_bot')

@bot.event
async def on_ready():
    logger.info(f"Bot ready: {bot.user}")

@bot.command(name="generate")
async def generate(ctx, *, prompt: str):
    logger.info(f"User {ctx.author} requested: {prompt}")
    # ... generation code
```

### 4. User Feedback

```python
@bot.command(name="generate")
async def generate_with_progress(ctx, *, prompt: str):
    """Show generation progress"""
    # Progress messages
    messages = [
        "🎨 Starting generation...",
        "🖌️ Processing prompt...",
        "✨ Creating image...",
        "🎉 Almost done..."
    ]
    
    status = await ctx.send(messages[0])
    
    try:
        for i, msg in enumerate(messages[1:], 1):
            await asyncio.sleep(1)
            await status.edit(content=msg)
        
        # Generate
        image_data = await ai_client.image.generate(prompt=prompt)
        
        # Send
        file = discord.File(io.BytesIO(image_data), filename="art.png")
        await ctx.send(file=file)
        await status.delete()
        
    except Exception as e:
        await status.edit(content=f"❌ Error: {str(e)}")
```

---

## 🎯 Complete Example

Here's a full-featured bot combining all concepts:

```python
import discord
from discord.ext import commands
from discord import app_commands
from blossom_ai import Blossom, BlossomError
import os
import io
import logging
from dotenv import load_dotenv

# Setup
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('bot')

# Config
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
BLOSSOM_TOKEN = os.getenv("BLOSSOM_TOKEN")

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# AI client
ai_client = Blossom(api_token=BLOSSOM_TOKEN)


@bot.event
async def on_ready():
    await bot.tree.sync()
    logger.info(f"✅ Bot ready as {bot.user}")


@bot.tree.command(name="imagine", description="Generate AI art")
@app_commands.describe(
    prompt="What to create",
    quality="Quality level",
    seed="Seed for reproducibility"
)
async def imagine(
    interaction: discord.Interaction,
    prompt: str,
    quality: str = "medium",
    seed: int = None
):
    await interaction.response.defer()
    
    try:
        sizes = {"low": 256, "medium": 512, "high": 768, "hd": 1024}
        size = sizes.get(quality, 512)
        
        image_data = await ai_client.image.generate(
            prompt=prompt,
            width=size,
            height=size,
            quality=quality,
            seed=seed,
            model="flux",
            enhance=True
        )
        
        file = discord.File(io.BytesIO(image_data), filename="art.png")
        
        embed = discord.Embed(
            title="✨ Your Creation",
            description=prompt,
            color=discord.Color.purple()
        )
        embed.set_image(url="attachment://art.png")
        embed.set_footer(text=f"Quality: {quality} | By {interaction.user.name}")
        
        await interaction.followup.send(embed=embed, file=file)
        
    except BlossomError as e:
        await interaction.followup.send(f"❌ {e.message}")


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
```

---

## 📚 Additional Resources

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Blossom AI Documentation](INDEX.md)
- [Discord Developer Portal](https://discord.com/developers/docs)

---

## 🆘 Troubleshooting

**Bot not responding:**
- Check Message Content Intent is enabled
- Verify bot has permissions in server
- Check token is correct

**Images not sending:**
- Check file size < 8MB (Discord limit)
- Verify bot has "Attach Files" permission
- Check image format is supported

**Rate limiting:**
- Add cooldowns to commands
- Implement queue system for requests
- Use caching for repeated prompts

---

**Made with 🌸 by the Eclips Team**

[← Back to Index](INDEX.md) | [Next: Telegram Bot →](TELEGRAM_BOT.md)