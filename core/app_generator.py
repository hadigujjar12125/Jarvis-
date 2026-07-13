#!/usr/bin/env python3
"""App generation module for JARVIS Pro."""

import json
import logging
from typing import Dict, List, Optional
from enum import Enum
import os

logger = logging.getLogger(__name__)


class AppType(Enum):
    """Types of applications to generate."""
    PYTHON_DESKTOP = "python_desktop"
    ANDROID = "android"
    WEB_API = "web_api"
    REST_API = "rest_api"
    FASTAPI_BACKEND = "fastapi_backend"
    CLI_TOOL = "cli_tool"


class AppGenerator:
    """Generate complete applications."""

    def __init__(self, ai_agent):
        """Initialize app generator with AI agent."""
        self.ai_agent = ai_agent
        self.apps_generated: List[Dict] = []

    def generate_python_desktop_app(self, app_name: str, features: List[str], 
                                   use_pyside6: bool = True) -> Dict[str, str]:
        """Generate a Python desktop application."""
        try:
            logger.info(f"Generating Python desktop app: {app_name}")
            
            framework = "PySide6" if use_pyside6 else "Tkinter"
            
            prompt = f"""Generate a complete {framework} desktop application for: {app_name}
            
Features needed:
{chr(10).join([f'- {f}' for f in features])}

Requirements:
1. Professional UI layout
2. Error handling
3. Type hints
4. Docstrings
5. MVC/MVP pattern
6. Configuration file support
7. Logging
8. Return complete working code
9. Python 3.12 compatible"""

            code = self.ai_agent.ask(prompt)
            
            app = {
                "type": "python_desktop",
                "name": app_name,
                "framework": framework,
                "features": features,
                "code": code
            }
            
            self.apps_generated.append(app)
            return app
        except Exception as e:
            logger.error(f"Error generating Python desktop app: {e}")
            return {"error": str(e)}

    def generate_rest_api(self, api_name: str, endpoints: List[str], 
                         use_fastapi: bool = True) -> Dict[str, str]:
        """Generate a REST API."""
        try:
            logger.info(f"Generating REST API: {api_name}")
            
            framework = "FastAPI" if use_fastapi else "Flask"
            
            prompt = f"""Generate a complete {framework} REST API: {api_name}
            
Endpoints needed:
{chr(10).join([f'- {e}' for e in endpoints])}

Requirements:
1. Request validation with Pydantic
2. Error handling
3. JWT authentication setup
4. CORS support
5. Database models (SQLAlchemy)
6. Input validation
7. Documentation strings
8. Type hints
9. Return complete working code
10. Python 3.12 compatible"""

            code = self.ai_agent.ask(prompt)
            
            app = {
                "type": "rest_api",
                "name": api_name,
                "framework": framework,
                "endpoints": endpoints,
                "code": code
            }
            
            self.apps_generated.append(app)
            return app
        except Exception as e:
            logger.error(f"Error generating REST API: {e}")
            return {"error": str(e)}

    def generate_fastapi_backend(self, project_name: str, models: List[str],
                                database_type: str = "postgresql") -> Dict[str, str]:
        """Generate a complete FastAPI backend."""
        try:
            logger.info(f"Generating FastAPI backend: {project_name}")
            
            prompt = f"""Generate a complete FastAPI backend for: {project_name}
            
Data models:
{chr(10).join([f'- {m}' for m in models])}

Database: {database_type}

Requirements:
1. SQLAlchemy ORM setup
2. All CRUD operations
3. Request/response models
4. Error handling
5. Logging
6. Environment configuration
7. Requirements.txt
8. .env.example
9. Main application file
10. Database initialization script
11. Authentication middleware
12. Type hints everywhere
13. Return all code files"""

            code = self.ai_agent.ask(prompt)
            
            app = {
                "type": "fastapi_backend",
                "name": project_name,
                "models": models,
                "database": database_type,
                "code": code
            }
            
            self.apps_generated.append(app)
            return app
        except Exception as e:
            logger.error(f"Error generating FastAPI backend: {e}")
            return {"error": str(e)}

    def generate_cli_tool(self, tool_name: str, commands: List[str]) -> Dict[str, str]:
        """Generate a CLI tool."""
        try:
            logger.info(f"Generating CLI tool: {tool_name}")
            
            prompt = f"""Generate a complete CLI tool: {tool_name}
            
Commands needed:
{chr(10).join([f'- {c}' for c in commands])}

Requirements:
1. Click or Typer framework
2. Help messages
3. Error handling
4. Configuration file support
5. Logging
6. Progress bars for long operations
7. Color output
8. Type hints
9. Main entry point
10. Setup.py for packaging
11. Complete working code"""

            code = self.ai_agent.ask(prompt)
            
            app = {
                "type": "cli_tool",
                "name": tool_name,
                "commands": commands,
                "code": code
            }
            
            self.apps_generated.append(app)
            return app
        except Exception as e:
            logger.error(f"Error generating CLI tool: {e}")
            return {"error": str(e)}

    def save_app(self, app: Dict, output_dir: str) -> bool:
        """Save application files to disk."""
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            # Save main code
            main_file = os.path.join(output_dir, "main.py")
            with open(main_file, "w") as f:
                f.write(app.get("code", ""))
            
            logger.info(f"App saved to {output_dir}")
            return True
        except Exception as e:
            logger.error(f"Error saving app: {e}")
            return False

    def get_generated_apps(self) -> List[Dict]:
        """Get list of generated apps."""
        return self.apps_generated
