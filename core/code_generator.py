#!/usr/bin/env python3
"""Code generation module for JARVIS Pro."""

import json
import logging
from typing import Dict, List, Optional, Tuple
from enum import Enum
import re

logger = logging.getLogger(__name__)


class Language(Enum):
    """Supported programming languages."""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    REACT = "react"
    HTML = "html"
    CSS = "css"
    JAVA = "java"
    CSHARP = "csharp"
    CPP = "cpp"
    PHP = "php"
    SQL = "sql"
    NODEJS = "nodejs"
    NEXTJS = "nextjs"


class CodeGenerator:
    """Generate, explain, debug, and refactor code."""

    def __init__(self, ai_agent):
        """Initialize code generator with AI agent."""
        self.ai_agent = ai_agent
        self.code_history: List[Dict] = []
        self.language_extensions = {
            Language.PYTHON: ".py",
            Language.JAVASCRIPT: ".js",
            Language.TYPESCRIPT: ".ts",
            Language.REACT: ".jsx",
            Language.HTML: ".html",
            Language.CSS: ".css",
            Language.JAVA: ".java",
            Language.CSHARP: ".cs",
            Language.CPP: ".cpp",
            Language.PHP: ".php",
            Language.SQL: ".sql",
            Language.NODEJS: ".js",
            Language.NEXTJS: ".jsx",
        }

    def generate_code(self, prompt: str, language: Language) -> str:
        """Generate code based on prompt and language."""
        try:
            lang_name = language.value
            full_prompt = f"""Generate {lang_name} code for: {prompt}
            
Requirements:
1. Production-ready code
2. Include error handling
3. Add type hints/annotations
4. Include docstrings/comments
5. Follow best practices
6. Ensure Python 3.12 compatibility if applicable
7. Return only the code, no explanations"""

            response = self.ai_agent.ask(full_prompt)
            
            # Store in history
            self.code_history.append({
                "type": "generated",
                "language": lang_name,
                "prompt": prompt,
                "code": response
            })
            
            logger.info(f"Generated {lang_name} code")
            return response
        except Exception as e:
            logger.error(f"Error generating code: {e}")
            return f"Error generating code: {e}"

    def explain_code(self, code: str) -> str:
        """Explain what code does."""
        try:
            prompt = f"""Explain this code in detail:

{code}

Provide:
1. Purpose of the code
2. How it works
3. Key components
4. Input/output
5. Edge cases
6. Potential improvements"""

            response = self.ai_agent.ask(prompt)
            return response
        except Exception as e:
            logger.error(f"Error explaining code: {e}")
            return f"Error explaining code: {e}"

    def debug_code(self, code: str, error: Optional[str] = None) -> str:
        """Debug code and identify issues."""
        try:
            if error:
                prompt = f"""Debug this code that has an error:

{code}

Error: {error}

Provide:
1. Root cause of the error
2. Why it occurs
3. Step-by-step fix
4. Corrected code
5. Prevention tips"""
            else:
                prompt = f"""Analyze this code for potential bugs and issues:

{code}

Provide:
1. Potential bugs
2. Logic errors
3. Performance issues
4. Security vulnerabilities
5. Suggested fixes"""

            response = self.ai_agent.ask(prompt)
            
            self.code_history.append({
                "type": "debugged",
                "code": code,
                "error": error,
                "debug_result": response
            })
            
            return response
        except Exception as e:
            logger.error(f"Error debugging code: {e}")
            return f"Error debugging code: {e}"

    def refactor_code(self, code: str, goal: Optional[str] = None) -> str:
        """Refactor code for better quality."""
        try:
            if goal:
                prompt = f"""Refactor this code with goal: {goal}

{code}

Refactor to:
1. Improve readability
2. {goal}
3. Follow best practices
4. Improve performance if possible
5. Add appropriate type hints

Return only the refactored code."""
            else:
                prompt = f"""Refactor this code:

{code}

Improve:
1. Code readability
2. Maintainability
3. Performance
4. Following SOLID principles
5. Type safety

Return only the refactored code."""

            response = self.ai_agent.ask(prompt)
            
            self.code_history.append({
                "type": "refactored",
                "original": code,
                "goal": goal,
                "refactored": response
            })
            
            return response
        except Exception as e:
            logger.error(f"Error refactoring code: {e}")
            return f"Error refactoring code: {e}"

    def optimize_code(self, code: str) -> str:
        """Optimize code for performance."""
        try:
            prompt = f"""Optimize this code for performance:

{code}

Optimizations:
1. Reduce time complexity
2. Reduce space complexity
3. Remove redundant operations
4. Use efficient algorithms
5. Profile improvements

Return only the optimized code with comments explaining changes."""

            response = self.ai_agent.ask(prompt)
            
            self.code_history.append({
                "type": "optimized",
                "original": code,
                "optimized": response
            })
            
            return response
        except Exception as e:
            logger.error(f"Error optimizing code: {e}")
            return f"Error optimizing code: {e}"

    def add_documentation(self, code: str) -> str:
        """Add comprehensive documentation and comments."""
        try:
            prompt = f"""Add comprehensive documentation to this code:

{code}

Include:
1. Module docstring
2. Function/method docstrings
3. Inline comments
4. Type hints
5. Example usage
6. Error documentation

Return only the documented code."""

            response = self.ai_agent.ask(prompt)
            return response
        except Exception as e:
            logger.error(f"Error adding documentation: {e}")
            return f"Error adding documentation: {e}"

    def generate_tests(self, code: str, language: Language) -> str:
        """Generate unit tests for code."""
        try:
            lang_name = language.value
            prompt = f"""Generate comprehensive unit tests for this {lang_name} code:

{code}

Tests should:
1. Cover all functions/methods
2. Include edge cases
3. Test error conditions
4. Achieve high coverage
5. Use appropriate testing framework

Return only the test code."""

            response = self.ai_agent.ask(prompt)
            
            self.code_history.append({
                "type": "tests_generated",
                "language": lang_name,
                "code": code,
                "tests": response
            })
            
            return response
        except Exception as e:
            logger.error(f"Error generating tests: {e}")
            return f"Error generating tests: {e}"

    def get_code_history(self) -> List[Dict]:
        """Get code generation history."""
        return self.code_history

    def clear_history(self) -> None:
        """Clear code history."""
        self.code_history.clear()
        logger.info("Code history cleared")
