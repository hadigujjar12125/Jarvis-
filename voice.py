import os
import asyncio
import logging
import speech_recognition as sr

try:
    import edge_tts
except ImportError:
    edge_tts = None

try:
    import pygame
    pygame.mixer.init()
except ImportError:
    pygame = None

from config import VOICE_NAME, MIC_DEVICE_INDEX

logger = logging.getLogger(__name__)

VOICE_FILE = "voice.mp3"


async def _speak_async(text):
    """Generate speech asynchronously using edge-tts."""
    try:
        if not edge_tts:
            logger.error("edge_tts not installed")
            return
        
        communicate = edge_tts.Communicate(text, VOICE_NAME)
        await communicate.save(VOICE_FILE)
    except Exception as e:
        logger.error(f"Error generating speech: {e}", exc_info=True)
        raise


def speak(text):
    """Speak text using text-to-speech."""
    if not text:
        return
    
    print(f"Assistant: {text}")
    
    if not pygame or not edge_tts:
        logger.warning("pygame or edge_tts not available, skipping audio")
        return
    
    try:
        asyncio.run(_speak_async(text))
    except Exception as e:
        logger.error(f"Failed to generate speech: {e}")
        return
    
    try:
        if os.path.exists(VOICE_FILE):
            pygame.mixer.music.load(VOICE_FILE)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            try:
                pygame.mixer.music.unload()
            except Exception as e:
                logger.debug(f"Error unloading audio: {e}")
    except pygame.error as e:
        logger.error(f"Pygame audio error: {e}")
    except Exception as e:
        logger.error(f"Voice error: {e}", exc_info=True)
    finally:
        # Clean up audio file
        try:
            if os.path.exists(VOICE_FILE):
                os.remove(VOICE_FILE)
        except OSError as e:
            logger.debug(f"Could not remove voice file: {e}")


def listen():
    """Listen for audio input using microphone."""
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone(device_index=MIC_DEVICE_INDEX) as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
    except sr.MicrophoneError as e:
        logger.error(f"Microphone error: {e}")
        print(f"Microphone error: {e}")
        return ""
    except sr.RequestError as e:
        logger.error(f"Microphone request error: {e}")
        print(f"Microphone error: {e}")
        return ""
    except sr.UnknownValueError:
        logger.debug("Could not understand audio")
        print("Could not understand audio")
        return ""
    except Exception as e:
        logger.error(f"Audio input error: {e}", exc_info=True)
        return ""

    try:
        command = recognizer.recognize_google(audio)
        print(f"You: {command}")
        return command
    except sr.RequestError as e:
        logger.error(f"Google Speech Recognition API error: {e}")
        print(f"API error: {e}")
        return ""
    except sr.UnknownValueError:
        logger.debug("Could not understand audio from Google API")
        print("Could not understand audio")
        return ""
    except Exception as e:
        logger.error(f"Speech recognition error: {e}", exc_info=True)
        return ""
