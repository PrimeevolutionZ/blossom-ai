"""
Blossom AI - Simple CLI Interface
Command-line interface for terminal usage only
"""

import os
import sys
from typing import Optional, Literal
from pathlib import Path

try:
    from blossom_ai import Blossom
    from blossom_ai.core.errors import BlossomError, print_info, print_error, print_success
except ImportError:
    print("❌ Blossom AI not installed. Run: pip install blossom-ai")
    sys.exit(1)


# ==============================================================================
# CLI INTERFACE (TERMINAL ONLY)
# ==============================================================================

class BlossomCLI:
    """
    Command-line interface for Blossom AI

    Usage:
        # From Python (interactive mode)
        >>> from blossom_ai.utils import BlossomCLI
        >>> cli = BlossomCLI()
        >>> cli.run()

        # From terminal
        $ python -m blossom_ai.utils.cli
    """

    def __init__(self, api_token: Optional[str] = None, api_version: Literal["v1", "v2"] = "v2"):
        """
        Initialize CLI

        Args:
            api_token: API token (optional, reads from env if not provided)
            api_version: API version to use (v1 or v2)
        """
        self.api_token = api_token or os.getenv("POLLINATIONS_API_KEY") or os.getenv("BLOSSOM_API_KEY")
        self.api_version = api_version
        self.client: Optional[Blossom] = None

    def _init_client(self):
        """Initialize Blossom client"""
        if self.client is None:
            try:
                self.client = Blossom(
                    api_token=self.api_token,
                    api_version=self.api_version,
                    timeout=60
                )
                print_success(f"✓ Connected to Blossom AI ({self.api_version.upper()})")
            except Exception as e:
                print_error(f"Failed to initialize client: {e}")
                sys.exit(1)

    def _print_banner(self):
        """Print welcome banner"""
        banner = """
╔══════════════════════════════════════════╗
║                                          ║
║        🌸 BLOSSOM AI CLI 🌸             ║
║                                          ║
║  Simple interface for AI generation      ║
║                                          ║
╚══════════════════════════════════════════╝
"""
        print(banner)

        if self.api_token:
            print("🔑 API Token: ✓ Configured")
        else:
            print("⚠️  API Token: Not set (using free tier)")
            print("   Set token: export POLLINATIONS_API_KEY='your-token'")

        print(f"📡 API Version: {self.api_version.upper()}")
        print()

    def _print_menu(self):
        """Print main menu"""
        menu = """
┌─────────────────────────────────────┐
│  What would you like to do?         │
├─────────────────────────────────────┤
│  1. 🖼️  Generate Image              │
│  2. 💬 Generate Text                │
│  3. 🗣️  Generate Audio (TTS)        │
│  4. ℹ️  Show Available Models       │
│  5. 🚪 Exit                         │
└─────────────────────────────────────┘
"""
        print(menu)

    def _generate_image(self):
        """Interactive image generation"""
        print("\n🖼️  IMAGE GENERATION")
        print("─" * 50)

        prompt = input("📝 Image prompt: ").strip()
        if not prompt:
            print_error("Prompt cannot be empty!")
            return

        # Optional parameters
        print("\n⚙️  Optional settings (press Enter to skip):")

        model_input = input(f"   Model [flux]: ").strip()
        model = model_input if model_input else "flux"

        width_input = input("   Width [1024]: ").strip()
        width = int(width_input) if width_input else 1024

        height_input = input("   Height [1024]: ").strip()
        height = int(height_input) if height_input else 1024

        filename = input("   Save as [image.png]: ").strip()
        filename = filename if filename else "image.png"

        print("\n🎨 Generating image...")

        try:
            filepath = self.client.image.save(
                prompt=prompt,
                filename=filename,
                model=model,
                width=width,
                height=height
            )
            print_success(f"✓ Image saved: {filepath}")

            # Show URL
            url = self.client.image.generate_url(prompt, model=model, width=width, height=height)
            print(f"🔗 URL: {url}")

        except BlossomError as e:
            print_error(f"Generation failed: {e}")
        except Exception as e:
            print_error(f"Unexpected error: {e}")

    def _generate_text(self):
        """Interactive text generation"""
        print("\n💬 TEXT GENERATION")
        print("─" * 50)

        prompt = input("📝 Text prompt: ").strip()
        if not prompt:
            print_error("Prompt cannot be empty!")
            return

        # Optional parameters
        print("\n⚙️  Optional settings (press Enter to skip):")

        model_input = input("   Model [openai]: ").strip()
        model = model_input if model_input else "openai"

        system_input = input("   System prompt: ").strip()
        system = system_input if system_input else None

        stream_input = input("   Stream output? [y/N]: ").strip().lower()
        stream = stream_input == 'y'

        print("\n🤖 Generating text...")

        try:
            if stream:
                print("\n" + "─" * 50)
                for chunk in self.client.text.generate(
                    prompt=prompt,
                    model=model,
                    system=system,
                    stream=True
                ):
                    print(chunk, end="", flush=True)
                print("\n" + "─" * 50)
            else:
                result = self.client.text.generate(
                    prompt=prompt,
                    model=model,
                    system=system
                )
                print("\n" + "─" * 50)
                print(result)
                print("─" * 50)

            print_success("\n✓ Generation complete")

        except BlossomError as e:
            print_error(f"Generation failed: {e}")
        except Exception as e:
            print_error(f"Unexpected error: {e}")

    def _generate_audio(self):
        """Interactive audio generation"""
        if self.api_version == "v2":
            print_error("Audio generation not available in V2 API yet")
            return

        print("\n🗣️  AUDIO GENERATION (TTS)")
        print("─" * 50)

        text = input("📝 Text to speak: ").strip()
        if not text:
            print_error("Text cannot be empty!")
            return

        # Optional parameters
        print("\n⚙️  Optional settings (press Enter to skip):")

        voice_input = input("   Voice [alloy]: ").strip()
        voice = voice_input if voice_input else "alloy"

        filename = input("   Save as [audio.mp3]: ").strip()
        filename = filename if filename else "audio.mp3"

        print("\n🎵 Generating audio...")

        try:
            filepath = self.client.audio.save(
                text=text,
                filename=filename,
                voice=voice
            )
            print_success(f"✓ Audio saved: {filepath}")

        except BlossomError as e:
            print_error(f"Generation failed: {e}")
        except Exception as e:
            print_error(f"Unexpected error: {e}")

    def _show_models(self):
        """Show available models"""
        print("\n📋 AVAILABLE MODELS")
        print("─" * 50)

        try:
            # Image models
            print("\n🖼️  Image Models:")
            image_models = self.client.image.models()
            for i, model in enumerate(image_models[:10], 1):
                print(f"   {i}. {model}")
            if len(image_models) > 10:
                print(f"   ... and {len(image_models) - 10} more")

            # Text models
            print("\n💬 Text Models:")
            text_models = self.client.text.models()
            for i, model in enumerate(text_models[:10], 1):
                print(f"   {i}. {model}")
            if len(text_models) > 10:
                print(f"   ... and {len(text_models) - 10} more")

            # Audio voices (if available)
            if self.api_version == "v1" and self.client.audio:
                print("\n🗣️  Audio Voices:")
                voices = self.client.audio.voices()
                for i, voice in enumerate(voices, 1):
                    print(f"   {i}. {voice}")

        except Exception as e:
            print_error(f"Failed to fetch models: {e}")

    def run(self):
        """Run interactive CLI"""
        self._print_banner()
        self._init_client()

        while True:
            try:
                self._print_menu()
                choice = input("Your choice [1-5]: ").strip()

                if choice == "1":
                    self._generate_image()
                elif choice == "2":
                    self._generate_text()
                elif choice == "3":
                    self._generate_audio()
                elif choice == "4":
                    self._show_models()
                elif choice == "5":
                    print("\n👋 Goodbye!")
                    break
                else:
                    print_error("Invalid choice. Please select 1-5.")

                # Pause before showing menu again
                input("\nPress Enter to continue...")
                print("\n" * 2)

            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Goodbye!")
                break
            except EOFError:
                print("\n\n👋 Goodbye!")
                break

        # Cleanup
        if self.client:
            try:
                self.client.close_sync()
            except:
                pass


# ==============================================================================
# CLI ENTRY POINT
# ==============================================================================

def main():
    """Main CLI entry point for command-line usage"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Blossom AI - Simple CLI Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python -m blossom_ai.utils.cli
  
  # Quick image generation
  python -m blossom_ai.utils.cli --image "a cat" --output cat.png
  
  # Quick text generation
  python -m blossom_ai.utils.cli --text "Write a poem"
  
  # Quick audio generation
  python -m blossom_ai.utils.cli --audio "Hello world" --output hello.mp3
        """
    )

    parser.add_argument(
        "--version",
        choices=["v1", "v2"],
        default="v2",
        help="API version to use (default: v2)"
    )

    parser.add_argument(
        "--token",
        help="API token (or set POLLINATIONS_API_KEY env var)"
    )

    # Quick commands
    parser.add_argument(
        "--image",
        help="Quick image generation: prompt"
    )

    parser.add_argument(
        "--text",
        help="Quick text generation: prompt"
    )

    parser.add_argument(
        "--audio",
        help="Quick audio generation: text"
    )

    parser.add_argument(
        "--output",
        help="Output filename for quick commands"
    )

    parser.add_argument(
        "--model",
        help="Model to use"
    )

    args = parser.parse_args()

    # Quick commands (command-line only)
    if args.image or args.text or args.audio:
        try:
            with Blossom(api_token=args.token, api_version=args.version) as client:
                if args.image:
                    filename = args.output or "image.png"
                    kwargs = {"model": args.model} if args.model else {}
                    filepath = client.image.save(args.image, filename, **kwargs)
                    print_success(f"✓ Image saved: {filepath}")

                elif args.text:
                    kwargs = {"model": args.model} if args.model else {}
                    result = client.text.generate(args.text, **kwargs)
                    print(result)

                elif args.audio:
                    if args.version == "v2":
                        print_error("Audio not available in V2 API")
                        sys.exit(1)
                    filename = args.output or "audio.mp3"
                    kwargs = {"voice": args.model} if args.model else {}
                    filepath = client.audio.save(args.audio, filename, **kwargs)
                    print_success(f"✓ Audio saved: {filepath}")
        except Exception as e:
            print_error(f"Failed: {e}")
            sys.exit(1)
        return

    # Interactive mode
    cli = BlossomCLI(api_token=args.token, api_version=args.version)
    cli.run()


if __name__ == "__main__":
    main()