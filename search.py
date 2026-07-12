import requests
import logging
from config import SEARCH_API_KEY

logger = logging.getLogger(__name__)


class SearchEngine:
    def __init__(self):
        self.api_key = SEARCH_API_KEY
        self.url = "https://serpapi.com/search"

    def search(self, query):
        """Search using SerpAPI."""
        if not self.api_key:
            logger.warning("Search API key not set (SEARCH_API_KEY)")
            return []

        if not query or not query.strip():
            logger.warning("Empty search query")
            return []

        try:
            params = {
                "q": query.strip(),
                "api_key": self.api_key,
                "engine": "google"
            }

            response = requests.get(self.url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            results = []
            
            for item in data.get("organic_results", [])[:5]:
                try:
                    title = item.get("title", "")
                    snippet = item.get("snippet", "")
                    link = item.get("link", "")
                    
                    if title and link:
                        results.append({
                            "title": title,
                            "snippet": snippet,
                            "link": link
                        })
                except (KeyError, ValueError) as e:
                    logger.debug(f"Error parsing search result: {e}")
                    continue
            
            return results

        except requests.Timeout:
            logger.error("Search API request timed out")
            return []
        except requests.ConnectionError as e:
            logger.error(f"Search API connection error: {e}")
            return []
        except requests.HTTPError as e:
            logger.error(f"Search API HTTP error: {e}")
            return []
        except ValueError as e:
            logger.error(f"Search API JSON decode error: {e}")
            return []
        except Exception as e:
            logger.error(f"Search Error: {e}", exc_info=True)
            return []
