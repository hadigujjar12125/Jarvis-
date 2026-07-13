#!/usr/bin/env python3
"""Main application entry point for JARVIS Pro."""

import sys
import argparse
import logging
from pathlib import Path

# Setup basic logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    from config import ASSISTANT_NAME, USER_NAME
    from ai import AIAgent
    from voice import listen, speak
    from core.command_handler import CommandHandler
    from gui.gui import JARVISGui
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    sys.exit(1)


class JARVISApplication:
    """Main JARVIS Pro application."""

    def __init__(self, use_gui: bool = False) -> None:
        self.use_gui = use_gui
        self.ai_agent = AIAgent()
        self.command_handler = CommandHandler()
        self.gui = None
        logger.info(f"JARVIS initialized (GUI: {use_gui})")

    def _process_input(self, user_input: str) -> str:
        """Process user input and return response."""
        if not user_input or not user_input.strip():
            return "Please provide input."

        command = user_input.strip()
        logger.info(f"Processing: {command}")

        try:
            # Try command handler first
            handled, response = self.command_handler.handle(command)
            if handled:
                logger.info(f"Command handled: {response[:50]}")
                return response
            
            # Fall back to AI
            response = self.ai_agent.ask(command)
            logger.info(f"AI response: {response[:50]}")
            return response
        except Exception as e:
            logger.error(f"Error processing input: {e}", exc_info=True)
            error_msg = f"I encountered an error: {str(e)}"
            return error_msg

    def run_gui(self) -> None:
        """Run GUI mode."""
        logger.info("Starting GUI mode")
        try:
            self.gui = JARVISGui(on_submit=self._process_input)
            
            # Welcome message
            welcome = f"Welcome {USER_NAME}! I'm {ASSISTANT_NAME}."
            self.gui._display_message(ASSISTANT_NAME, welcome)
            
            self.gui.run()
        except Exception as e:
            logger.error(f"GUI error: {e}", exc_info=True)
            print("GUI failed, falling back to CLI")
            self.run_cli()

    def run_cli(self) -> None:
        """Run CLI mode."""
        logger.info("Starting CLI mode")
        print(f"\n{ASSISTANT_NAME} Pro CLI")
        print(f"Welcome {USER_NAME}!\n")
        print("Commands: shutdown, restart, sleep, lock, system info, cpu usage, etc.")
        print("Type 'exit' to quit\n")

        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in {"exit", "quit", "bye"}:
                    print(f"{ASSISTANT_NAME}: Goodbye!")
                    break

                if not user_input:
                    continue

                response = self._process_input(user_input)
                print(f"{ASSISTANT_NAME}: {response}\n")

            except KeyboardInterrupt:
                print(f"\n{ASSISTANT_NAME}: Goodbye!")
                break
            except Exception as e:
                logger.error(f"CLI error: {e}", exc_info=True)
                print(f"Error: {e}")

    def run_voice(self) -> None:
        """Run voice mode."""
        logger.info("Starting voice mode")
        print(f"{ASSISTANT_NAME} Voice Mode")
        print("Say something to start\n")

        while True:
            try:
                # Listen for input
                user_input = listen()
                if not user_input:
                    continue

                if user_input.lower() in {"exit", "quit", "bye"}:
                    speak(f"Goodbye {USER_NAME}!")
                    break

                # Process and respond
                response = self._process_input(user_input)
                speak(response)

            except KeyboardInterrupt:
                speak("Goodbye!")
                break
            except Exception as e:
                logger.error(f"Voice mode error: {e}", exc_info=True)
                speak(f"Error occurred")

    def run(self) -> None:
        """Run application."""
        if self.use_gui:
            self.run_gui()
        else:
            self.run_cli()


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="JARVIS Pro - Advanced AI Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py              # Run GUI mode
  python main.py --cli        # Run CLI mode
  python main.py --voice      # Run voice mode
  python main.py --debug      # Run with debug logging
        """
    )
    
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Run in CLI mode instead of GUI"
    )
    parser.add_argument(
        "--voice",
        action="store_true",
        help="Run in voice mode"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    
    args = parser.parse_args()
    
    try:
        if args.debug:
            logging.getLogger().setLevel(logging.DEBUG)
            logger.info("Debug mode enabled")
        
        app = JARVISApplication(use_gui=not args.cli and not args.voice)
        
        if args.voice:
            app.run_voice()
        elif args.cli:
            app.run_cli()
        else:
            app.run_gui()
    
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
