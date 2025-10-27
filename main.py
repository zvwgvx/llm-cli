#!/usr/bin/env python3
"""
PolyCLI - A beautiful command-line interface for chatting with Ollama models.
Uses only Python built-in libraries - no external dependencies required!
"""

import json
import sys
import os
import urllib.request
import urllib.error
from typing import Optional, Dict, Any, List

class Colors:
    """ANSI color codes for terminal output - styled like Claude/Gemini CLI."""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

    # Softer, more professional colors
    GRAY = '\033[90m'           # Dim gray
    LIGHT_GRAY = '\033[37m'     # Light gray
    ORANGE = '\033[38;5;208m'   # Soft orange
    PURPLE = '\033[38;5;141m'   # Soft purple
    BLUE = '\033[38;5;75m'      # Soft blue
    GREEN = '\033[38;5;78m'     # Soft green
    RED = '\033[38;5;203m'      # Soft red
    YELLOW = '\033[38;5;221m'   # Soft yellow

    # User/Assistant colors (like Claude)
    USER_COLOR = '\033[38;5;75m'      # Soft blue for user
    ASSISTANT_COLOR = LIGHT_GRAY       # Light gray for assistant
    SYSTEM_COLOR = GRAY                # Dim gray for system messages
    ERROR_COLOR = RED                  # Soft red for errors


def print_colored(text: str, color: str = Colors.RESET, end: str = '\n'):
    """Print colored text to terminal."""
    print(f"{color}{text}{Colors.RESET}", end=end)


def print_box(text: str, title: str = "", width: int = 70):
    """Print text in a box with softer styling."""
    lines = text.strip().split('\n')

    # Top border
    if title:
        title_str = f" {title} "
        padding = (width - len(title_str) - 2) // 2
        print_colored(f"┌{'─' * padding}{title_str}{'─' * (width - padding - len(title_str) - 2)}┐", Colors.GRAY)
    else:
        print_colored(f"┌{'─' * (width - 2)}┐", Colors.GRAY)

    # Content
    for line in lines:
        content = line[:width - 4] if len(line) > width - 4 else line
        padding = width - len(content) - 4
        print_colored(f"│ ", Colors.GRAY, end='')
        print(f"{content}{' ' * padding} ", end='')
        print_colored("│", Colors.GRAY)

    # Bottom border
    print_colored(f"└{'─' * (width - 2)}┘", Colors.GRAY)


class PolyCLI:
    """Main chat application class."""

    def __init__(self, config_path: str = "config.json"):
        """Initialize the chat application with configuration."""
        self.config = self._load_config(config_path)
        self.conversation_history: List[Dict[str, str]] = []
        self.api_url = self.config.get("api_url", "http://localhost:11434")
        self.model = self.config.get("model", "llama2")

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print_colored(f"Error: Config file '{config_path}' not found!", Colors.ERROR_COLOR)
            print_colored("Creating default config.json...", Colors.SYSTEM_COLOR)
            default_config = {
                "api_url": "http://localhost:11434",
                "model": "llama2",
                "temperature": 0.7,
                "max_tokens": 2048,
                "system_prompt": "You are a helpful AI assistant.",
                "stream": True,
                "timeout": 120
            }
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2)
            return default_config
        except json.JSONDecodeError as e:
            print_colored(f"Error parsing config file: {e}", Colors.ERROR_COLOR)
            sys.exit(1)

    def _call_ollama_api(self, prompt: str) -> Optional[str]:
        """Call Ollama API and return the response."""
        url = f"{self.api_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": self.config.get("stream", True),
            "options": {
                "temperature": self.config.get("temperature", 0.7),
                "num_predict": self.config.get("max_tokens", 2048),
            }
        }

        # Add reasoning_effort if configured
        if self.config.get("reasoning_effort"):
            payload["options"]["reasoning_effort"] = self.config.get("reasoning_effort")

        # Add system prompt to the first message
        if len(self.conversation_history) == 0 and self.config.get("system_prompt"):
            payload["system"] = self.config.get("system_prompt")

        # Convert payload to JSON bytes
        data = json.dumps(payload).encode('utf-8')

        # Create request
        req = urllib.request.Request(
            url,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        try:
            with urllib.request.urlopen(req, timeout=self.config.get("timeout", 120)) as response:
                if self.config.get("stream", True):
                    return self._handle_streaming_response(response)
                else:
                    result = json.loads(response.read().decode('utf-8'))
                    return result.get("response", "")

        except urllib.error.URLError as e:
            print_colored("Error: Cannot connect to Ollama API. Make sure Ollama is running.", Colors.ERROR_COLOR)
            print_colored(f"API URL: {self.api_url}", Colors.SYSTEM_COLOR)
            print_colored(f"Details: {e}", Colors.SYSTEM_COLOR)
            return None
        except Exception as e:
            print_colored(f"Error calling API: {e}", Colors.ERROR_COLOR)
            return None

    def _handle_streaming_response(self, response) -> Optional[str]:
        """Handle streaming response from Ollama API."""
        full_response = ""

        print()  # New line before response
        print_colored("Assistant", Colors.ASSISTANT_COLOR + Colors.DIM, end='')
        print_colored(" ~$", Colors.GRAY)
        print()  # New line after label

        try:
            for line in response:
                if line:
                    try:
                        line_str = line.decode('utf-8').strip()
                        if not line_str:
                            continue

                        chunk = json.loads(line_str)
                        if "response" in chunk:
                            token = chunk["response"]
                            full_response += token

                            # Print token immediately for smooth streaming
                            print(token, end='', flush=True)

                        # Check if done
                        if chunk.get("done", False):
                            break

                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            print_colored(f"\nError during streaming: {e}", Colors.ERROR_COLOR)
            return None

        print()  # New line after response
        print()  # Extra spacing
        return full_response

    def _display_welcome(self):
        """Display welcome message."""
        welcome_lines = [
            "PolyCLI - Chat with AI models via Ollama",
            "",
            f"Model: {self.model}",
            f"API: {self.api_url}",
            "",
            "Type your message to chat. Special commands:",
            "  /clear   - Clear conversation history",
            "  /history - Show conversation history",
            "  /config  - Show configuration",
            "  /exit    - Exit the application",
            "  Ctrl+C   - Exit the application",
        ]
        welcome_text = "\n".join(welcome_lines)
        print_box(welcome_text, "PolyCLI", 70)
        print()

    def _handle_special_command(self, user_input: str) -> bool:
        """Handle special commands. Returns True if command was handled."""
        if user_input.startswith('/'):
            command = user_input.lower().strip()

            if command in ['/exit', '/quit']:
                print_colored("Goodbye!", Colors.SYSTEM_COLOR)
                return True

            elif command == '/clear':
                self.conversation_history.clear()
                print_colored("Conversation history cleared.", Colors.SYSTEM_COLOR)

            elif command == '/history':
                if not self.conversation_history:
                    print_colored("No conversation history.", Colors.SYSTEM_COLOR)
                else:
                    print_box("Conversation History", "History", 70)
                    for msg in self.conversation_history:
                        role = msg['role'].capitalize()
                        content = msg['content']
                        if role == "User":
                            print_colored(f"\n{role}:", Colors.USER_COLOR)
                        else:
                            print_colored(f"\n{role}:", Colors.ASSISTANT_COLOR)
                        print(content)
                    print()

            elif command == '/config':
                config_text = json.dumps(self.config, indent=2, ensure_ascii=False)
                print_box(config_text, "Configuration", 70)

            else:
                print_colored(f"Unknown command: {command}", Colors.ERROR_COLOR)

            print()
            return False

        return False

    def run(self):
        """Run the main chat loop."""
        self._display_welcome()

        try:
            while True:
                # Get user input
                print_colored("You", Colors.USER_COLOR + Colors.DIM, end='')
                print_colored(" ~$ ", Colors.GRAY, end='')
                user_input = input().strip()

                if not user_input:
                    continue

                # Handle special commands
                if self._handle_special_command(user_input):
                    break

                if user_input.startswith('/'):
                    continue

                # Add user message to history
                self.conversation_history.append({
                    "role": "user",
                    "content": user_input
                })

                # Build context from conversation history
                context = ""
                for msg in self.conversation_history:
                    role = msg['role'].capitalize()
                    context += f"{role}: {msg['content']}\n\n"

                context += "Assistant: "

                # Get AI response
                response = self._call_ollama_api(context)

                if response:
                    # Add assistant response to history
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": response
                    })
                else:
                    # Remove user message if API call failed
                    self.conversation_history.pop()
                    print()

        except KeyboardInterrupt:
            print_colored("\n\nGoodbye!", Colors.SYSTEM_COLOR)
        except Exception as e:
            print_colored(f"\nUnexpected error: {e}", Colors.ERROR_COLOR)
            sys.exit(1)


def main():
    """Main entry point."""
    # Check if config file exists
    config_path = "config.json"
    if not os.path.exists(config_path):
        print_colored(f"Config file not found. Creating default {config_path}...", Colors.SYSTEM_COLOR)

    # Create and run chat application
    chat = PolyCLI(config_path)
    chat.run()


if __name__ == "__main__":
    main()