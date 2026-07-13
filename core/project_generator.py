#!/usr/bin/env python3
"""Project generation module for JARVIS Pro."""

import os
import json
import logging
from typing import Dict, List, Optional
from pathlib import Path
import subprocess

logger = logging.getLogger(__name__)


class ProjectGenerator:
    """Generate complete projects with folder structure and files."""

    def __init__(self, ai_agent):
        """Initialize project generator with AI agent."""
        self.ai_agent = ai_agent
        self.projects_generated: List[Dict] = []

    def generate_python_project(self, project_name: str, description: str,
                               dependencies: Optional[List[str]] = None) -> Dict:
        """Generate a complete Python project."""
        try:
            logger.info(f"Generating Python project: {project_name}")
            
            # Create project directory
            project_dir = self._create_project_structure(project_name)
            
            if dependencies is None:
                dependencies = ["requests>=2.31.0", "python-dotenv>=1.0.0"]
            
            # Generate main files
            self._generate_python_files(project_dir, project_name, description)
            
            # Generate requirements.txt
            self._generate_requirements(project_dir, dependencies)
            
            # Generate .env.example
            self._generate_env_example(project_dir)
            
            # Generate README.md
            self._generate_readme(project_dir, project_name, description)
            
            # Generate .gitignore
            self._generate_gitignore(project_dir)
            
            project = {
                "name": project_name,
                "type": "python",
                "path": project_dir,
                "description": description,
                "dependencies": dependencies
            }
            
            self.projects_generated.append(project)
            logger.info(f"Project created at {project_dir}")
            return project
        except Exception as e:
            logger.error(f"Error generating project: {e}")
            return {"error": str(e)}

    def _create_project_structure(self, project_name: str) -> str:
        """Create standard project folder structure."""
        try:
            project_dir = os.path.join(os.getcwd(), project_name)
            
            folders = [
                project_dir,
                os.path.join(project_dir, "src"),
                os.path.join(project_dir, "tests"),
                os.path.join(project_dir, "docs"),
                os.path.join(project_dir, "config"),
                os.path.join(project_dir, "utils"),
            ]
            
            for folder in folders:
                os.makedirs(folder, exist_ok=True)
            
            # Create __init__.py files
            for folder in [os.path.join(project_dir, "src"), 
                          os.path.join(project_dir, "tests")]:
                open(os.path.join(folder, "__init__.py"), "w").close()
            
            logger.info(f"Project structure created at {project_dir}")
            return project_dir
        except Exception as e:
            logger.error(f"Error creating project structure: {e}")
            raise

    def _generate_python_files(self, project_dir: str, project_name: str, 
                              description: str) -> None:
        """Generate Python source files."""
        try:
            # Main entry point
            main_file = os.path.join(project_dir, "src", "main.py")
            main_content = f'''#!/usr/bin/env python3
"""Main entry point for {project_name}."""

import logging
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main application entry point."""
    logger.info(f"Starting {project_name}")
    # Add your code here
    pass


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Fatal error: {{e}}", exc_info=True)
        sys.exit(1)
'''
            with open(main_file, "w") as f:
                f.write(main_content)
            
            # Config file
            config_file = os.path.join(project_dir, "config", "config.py")
            config_content = '''#!/usr/bin/env python3
"""Configuration module."""

import os
from dotenv import load_dotenv

load_dotenv()

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")

# API
DEBUG_MODE = os.getenv("DEBUG_MODE", "0").lower() in ("1", "true", "yes")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
'''
            with open(config_file, "w") as f:
                f.write(config_content)
            
            # Utils file
            utils_file = os.path.join(project_dir, "utils", "helpers.py")
            utils_content = '''#!/usr/bin/env python3
"""Helper utilities."""

import logging

logger = logging.getLogger(__name__)


def log_info(message: str) -> None:
    """Log info message."""
    logger.info(message)


def log_error(message: str, exc_info: bool = False) -> None:
    """Log error message."""
    logger.error(message, exc_info=exc_info)
'''
            with open(utils_file, "w") as f:
                f.write(utils_content)
            
            logger.info(f"Python files generated for {project_name}")
        except Exception as e:
            logger.error(f"Error generating Python files: {e}")
            raise

    def _generate_requirements(self, project_dir: str, dependencies: List[str]) -> None:
        """Generate requirements.txt."""
        try:
            req_file = os.path.join(project_dir, "requirements.txt")
            req_content = "\n".join(dependencies) + "\n"
            with open(req_file, "w") as f:
                f.write(req_content)
            logger.info(f"requirements.txt generated")
        except Exception as e:
            logger.error(f"Error generating requirements.txt: {e}")
            raise

    def _generate_env_example(self, project_dir: str) -> None:
        """Generate .env.example file."""
        try:
            env_file = os.path.join(project_dir, ".env.example")
            env_content = """# Application Configuration
DEBUG_MODE=0
LOG_LEVEL=INFO

# Database
DATABASE_URL=sqlite:///app.db

# API Keys
# Add your API keys here
"""
            with open(env_file, "w") as f:
                f.write(env_content)
            logger.info(f".env.example generated")
        except Exception as e:
            logger.error(f"Error generating .env.example: {e}")
            raise

    def _generate_readme(self, project_dir: str, project_name: str, 
                        description: str) -> None:
        """Generate README.md."""
        try:
            readme_file = os.path.join(project_dir, "README.md")
            readme_content = f"""# {project_name}

{description}

## Installation

### 1. Clone Repository
```bash
git clone <repository-url>
cd {project_name}
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Run Application
```bash
python src/main.py
```

## Project Structure

```
{project_name}/
├── src/
│   ├── __init__.py
│   └── main.py
├── tests/
├── docs/
├── config/
│   └── config.py
├── utils/
│   └── helpers.py
├── requirements.txt
├── .env.example
├── README.md
└── .gitignore
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

MIT License
"""
            with open(readme_file, "w") as f:
                f.write(readme_content)
            logger.info(f"README.md generated")
        except Exception as e:
            logger.error(f"Error generating README.md: {e}")
            raise

    def _generate_gitignore(self, project_dir: str) -> None:
        """Generate .gitignore file."""
        try:
            gitignore_file = os.path.join(project_dir, ".gitignore")
            gitignore_content = """# Environment
.env
.venv
venv/

# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Tests
.pytest_cache/
.coverage
htmlcov/

# Database
*.db
*.sqlite
"""
            with open(gitignore_file, "w") as f:
                f.write(gitignore_content)
            logger.info(f".gitignore generated")
        except Exception as e:
            logger.error(f"Error generating .gitignore: {e}")
            raise

    def install_dependencies(self, project_dir: str) -> bool:
        """Install project dependencies."""
        try:
            req_file = os.path.join(project_dir, "requirements.txt")
            if not os.path.exists(req_file):
                logger.warning(f"requirements.txt not found")
                return False
            
            # Try to install dependencies
            result = subprocess.run(
                ["pip", "install", "-r", req_file],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info(f"Dependencies installed successfully")
                return True
            else:
                logger.error(f"Failed to install dependencies: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Error installing dependencies: {e}")
            return False

    def get_generated_projects(self) -> List[Dict]:
        """Get list of generated projects."""
        return self.projects_generated
