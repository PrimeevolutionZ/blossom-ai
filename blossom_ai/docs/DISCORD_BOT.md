# Discord Bot Tutorial

The `generate_url()` method is perfect for Discord bots as it allows you to instantly get a URL that Discord can embed, without needing to download and re-upload the image file.

## Example: Simple `/imagine` Command

This example shows how to create a simple Discord bot command that takes a prompt and sends the generated image URL back to the channel.

```python
import discord
from blossom_ai import Blossom

# Initialize your Discord bot client
# Note: You should use a modern framework like discord.ext.commands or discord.app_commands
# for slash commands in a production bot. This is a simplified example.
bot = discord.Client()

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Check for the '!imagine' command
    if message.content.startswith('!imagine'):
        # Extract the prompt from the message
        prompt = message.content[8:].strip()
        
        if not prompt:
            await message.channel.send("Please provide a prompt after `!imagine`.")
            return

        # Use context manager for proper cleanup in an async environment
        async with Blossom() as client:
            try:
                # Generate URL instantly - no download needed!
                url = await client.image.generate_url(
                    prompt,
                    nologo=True, # Optional: Remove watermark
                    private=True # Optional: Private generation
                )
                
                # Discord will automatically show image preview from the URL
                await message.channel.send(url)
                
            except Exception as e:
                await message.channel.send(f"An error occurred during generation: {e}")

# Replace 'YOUR_DISCORD_TOKEN' with your actual bot token
# bot.run('YOUR_DISCORD_TOKEN')
```
