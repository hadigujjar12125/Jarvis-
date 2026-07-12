import os
import copy
import logging

from config import GEMINI_API_KEY, OPENAI_API_KEY, AUTO_WEB_SEARCH_ENABLE

logger = logging.getLogger(__name__)

try:
    from google import genai
except ImportError:
    logger.warning("google-generativeai not installed")
    genai = None

try:
    from openai import OpenAI
except ImportError:
    logger.warning("openai not installed")
    OpenAI = None

try:
    from search import SearchEngine
except ImportError:
    logger.warning("search module not available")
    SearchEngine = None

openai_client = None
if OpenAI and OPENAI_API_KEY:
    try:
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        logger.info("OpenAI client initialized")
    except Exception as e:
        logger.error(f"OpenAI client init error: {e}")
        openai_client = None

gemini_client = None
if genai and GEMINI_API_KEY:
    try:
        gemini_client = genai.Client(api_key=GEMINI_API_KEY)
        logger.info("Gemini client initialized")
    except Exception as e:
        logger.error(f"Gemini client init error: {e}")
        gemini_client = None


def _detect_search_intent(text: str) -> bool:
    """Detect if user query requires web search."""
    if not text:
        return False
    t = text.lower()
    # Basic heuristic: question words or explicit search triggers
    triggers = ["who", "what", "when", "where", "why", "how", "search for", "google", "look up", "find ", "define ", "tell me about"]
    for tr in triggers:
        if tr in t:
            return True
    # If it's short command-like queries, don't auto-search
    if len(t.split()) <= 2:
        return False
    return False


class AIAgent:
    def __init__(self):
        self.history = [
            {
                "role": "system",
                "content": "You are Jarvis, a helpful digital assistant. Keep responses clear, polite, and useful."
            }
        ]

    def ask(self, prompt):
        if not prompt or not prompt.strip():
            return "Please say something so I can help."

        self.history.append({"role": "user", "content": prompt.strip()})
        response_text = self._generate_response()
        self.history.append({"role": "assistant", "content": response_text})
        return response_text

    def _generate_response(self):
        """Generate response using available AI models."""
        last_user = self.history[-1]["content"] if self.history and len(self.history) > 0 else ""
        augmented_history = copy.deepcopy(self.history)

        try:
            # Optionally perform automatic web search when intent detected
            if AUTO_WEB_SEARCH_ENABLE and _detect_search_intent(last_user) and SearchEngine:
                try:
                    se = SearchEngine()
                    results = se.search(last_user)
                    if results:
                        summary = "\n".join([f"- {r.get('title', 'N/A')}: {r.get('link', 'N/A')}" for r in results[:5]])
                        augmented_history.append({"role": "system", "content": f"Web search results:\n{summary}"})
                except Exception as e:
                    logger.warning(f"Search error: {e}")

            # Prefer Gemini if available, otherwise OpenAI
            if gemini_client:
                return self._ask_gemini(augmented_history)

            if openai_client:
                return self._ask_openai(augmented_history)

            return "AI is not configured. Set OPENAI_API_KEY or GEMINI_API_KEY in config or environment."
        except Exception as exc:
            logger.error(f"Error generating response: {exc}", exc_info=True)
            return f"AI generation error: {exc}"

    @staticmethod
    def _ask_openai(history):
        """Query OpenAI GPT model."""
        try:
            if not openai_client:
                return "OpenAI client not available"
            
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=history,
                max_tokens=600,
                temperature=0.7,
            )
            
            if response and response.choices and len(response.choices) > 0:
                content = response.choices[0].message.content
                return content.strip() if content else "No response from OpenAI"
            
            return "Invalid response from OpenAI"
        except Exception as exc:
            logger.error(f"OpenAI error: {exc}", exc_info=True)
            return f"OpenAI error: {exc}"

    @staticmethod
    def _ask_gemini(history):
        """Query Google Gemini model."""
        try:
            if not gemini_client:
                return "Gemini client not available"
            
            # Build prompt from recent history
            recent = history[-6:]
            prompt_parts = []
            for m in recent:
                role = m.get('role', 'user').upper()
                content = m.get('content', '')
                prompt_parts.append(f"{role}: {content}")
            prompt = "\n".join(prompt_parts)

            response = gemini_client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )
            
            if response:
                text = getattr(response, "text", None)
                if text:
                    return str(text).strip()
                return str(response).strip()
            
            return "No response from Gemini"
        except Exception as exc:
            logger.error(f"Gemini error: {exc}", exc_info=True)
            # If Gemini fails and OpenAI is available, fall back
            if openai_client:
                try:
                    return AIAgent._ask_openai(history)
                except Exception:
                    pass
            return f"Gemini error: {exc}"
