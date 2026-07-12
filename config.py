import os
import logging

logger = logging.getLogger(__name__)

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY", "").strip()

# Wake word configuration
WAKE_WORD = os.getenv("WAKE_WORD", "jarvis").strip()
ENABLE_WAKE_WORD = os.getenv("ENABLE_WAKE_WORD", "1").lower() in ("1", "true", "yes")

# Memory pruning defaults
try:
    MEMORY_MAX_ITEMS = int(os.getenv("MEMORY_MAX_ITEMS", "100"))
except (ValueError, TypeError):
    MEMORY_MAX_ITEMS = 100
    logger.warning("Invalid MEMORY_MAX_ITEMS, using default: 100")

try:
    MEMORY_TTL_DAYS = int(os.getenv("MEMORY_TTL_DAYS", "30"))
except (ValueError, TypeError):
    MEMORY_TTL_DAYS = 30
    logger.warning("Invalid MEMORY_TTL_DAYS, using default: 30")

# Command allowlist/denylist safety
allowlist_str = os.getenv("COMMAND_ALLOWLIST", "").strip()
COMMAND_ALLOWLIST = [cmd.strip() for cmd in allowlist_str.split(",") if cmd.strip()] if allowlist_str else []

denylist_str = os.getenv("COMMAND_DENYLIST", "rm ,format ,shutdown ,reboot ,del ,wipe").strip()
COMMAND_DENYLIST = [cmd.strip() for cmd in denylist_str.split(",") if cmd.strip()]

# Auto web search behavior
AUTO_WEB_SEARCH_ENABLE = os.getenv("AUTO_WEB_SEARCH_ENABLE", "1").lower() in ("1", "true", "yes")

# Assistant settings
ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "Jarvis").strip()
USER_NAME = os.getenv("USER_NAME", "User").strip()
VOICE_NAME = os.getenv("VOICE_NAME", "en-US-GuyNeural").strip()

# Microphone settings
try:
    MIC_DEVICE_INDEX = int(os.getenv("MIC_DEVICE_INDEX", "0"))
except (ValueError, TypeError):
    MIC_DEVICE_INDEX = 0
    logger.warning("Invalid MIC_DEVICE_INDEX, using default: 0")

# Debug mode
DEBUG_MODE = os.getenv("DEBUG_MODE", "0").lower() in ("1", "true", "yes")
