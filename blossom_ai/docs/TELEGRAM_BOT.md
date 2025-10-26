# Telegram Bot Tutorial

The `generate_url()` method is highly efficient for Telegram bots, allowing you to send the generated image URL directly to the `reply_photo` function, which handles the display.

## Example: Simple `/imagine` Command

This example uses the `python-telegram-bot` library to create a bot that responds to the `/imagine` command with a generated image.

```python
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from blossom_ai import Blossom
import logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

async def imagine(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a generated image based on the prompt provided by the user."""
    
    # The prompt is everything after the command, joined by spaces
    prompt = ' '.join(context.args)
    
    if not prompt:
        await update.message.reply_text("Please provide a prompt after `/imagine`.")
        return

    # Use context manager for proper resource handling
    async with Blossom() as client:
        try:
            # Generate URL - fast and efficient
            url = await client.image.generate_url(prompt, nologo=True)
        
            # Send image directly from URL
            await update.message.reply_photo(photo=url, caption=f"Prompt: {prompt}")
            
        except Exception as e:
            await update.message.reply_text(f"An error occurred during generation: {e}")

def main() -> None:
    """Start the bot."""
    # Replace "YOUR_TELEGRAM_TOKEN" with your actual bot token
    app = Application.builder().token("YOUR_TELEGRAM_TOKEN").build()

    # on different commands - answer in Telegram
    app.add_handler(CommandHandler("imagine", imagine))

    # Run the bot until the user presses Ctrl-C
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
```
