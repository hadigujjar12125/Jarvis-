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
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    sys.exit(1)


class JARVISApplication:
    """Main JARVIS Pro application."""

    def __init__(self, use_gui: bool = False) -> None:
        self.use_gui = use_gui
        self.ai_agent = AIAgent()
        logger.info(f"JARVIS initialized (GUI: {use_gui})")

    def _process_input(self, user_input: str) -> str:
        """Process user input and return response."""
        if not user_input or not user_input.strip():
            return "Please provide input."

        command = user_input.strip()
        logger.info(f"Processing: {command}")

        try:
            response = self.ai_agent.ask(command)
            logger.info(f"Response: {response[:50]}")
            return response
        except Exception as e:
            logger.error(f"Error processing input: {e}", exc_info=True)
            error_msg = f"I encountered an error: {str(e)}"
            return error_msg

    def run_cli(self) -> None:
        """Run CLI mode."""
        logger.info("Starting CLI mode")
        print(f"\n{ASSISTANT_NAME} Pro CLI")
        print(f"Welcome {USER_NAME}!\n")

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
            logger.warning("GUI mode not yet implemented, falling back to CLI")
            self.run_cli()
        else:
            self.run_cli()


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="JARVIS Pro - Advanced AI Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py              # Run CLI mode
  python main.py --voice      # Run voice mode
  python main.py --debug      # Run with debug logging
        """
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
        
        app = JARVISApplication(use_gui=False)
        
        if args.voice:
            app.run_voice()
        else:
            app.run_cli()
    
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
