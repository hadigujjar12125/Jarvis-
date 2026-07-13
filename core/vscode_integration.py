#!/usr/bin/env python3
"""VS Code integration module for JARVIS Pro."""

import os
import subprocess
import logging
import json
from typing import Optional, List, Dict, Tuple
import sys

logger = logging.getLogger(__name__)


class VSCodeIntegration:
    """Integrate with VS Code for file creation, editing, and execution."""

    def __init__(self):
        """Initialize VS Code integration."""
        self.vscode_available = self._check_vscode()
        self.last_file_created: Optional[str] = None
        self.execution_history: List[Dict] = []

    def _check_vscode(self) -> bool:
        """Check if VS Code is installed and accessible."""
        try:
            result = subprocess.run(
                ["code", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            logger.warning("VS Code not found or not in PATH")
            return False

    def create_file(self, file_path: str, content: str, open_in_vscode: bool = True) -> bool:
        """Create file and optionally open in VS Code."""
        try:
            # Create directory if needed
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Write file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.last_file_created = file_path
            logger.info(f"Created file: {file_path}")
            
            # Open in VS Code if available
            if open_in_vscode and self.vscode_available:
                self.open_in_vscode(file_path)
            
            return True
        except Exception as e:
            logger.error(f"Error creating file: {e}")
            return False

    def edit_file(self, file_path: str, open_in_vscode: bool = True) -> bool:
        """Edit file in VS Code."""
        try:
            if not os.path.exists(file_path):
                logger.warning(f"File not found: {file_path}")
                return False
            
            if open_in_vscode and self.vscode_available:
                self.open_in_vscode(file_path)
                return True
            
            logger.warning("VS Code not available")
            return False
        except Exception as e:
            logger.error(f"Error editing file: {e}")
            return False

    def open_in_vscode(self, file_path: str) -> bool:
        """Open file in VS Code."""
        try:
            if not self.vscode_available:
                logger.warning("VS Code not available")
                return False
            
            subprocess.Popen(
                ["code", file_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            logger.info(f"Opened in VS Code: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error opening in VS Code: {e}")
            return False

    def open_folder_in_vscode(self, folder_path: str) -> bool:
        """Open folder in VS Code."""
        try:
            if not self.vscode_available:
                logger.warning("VS Code not available")
                return False
            
            if not os.path.exists(folder_path):
                logger.warning(f"Folder not found: {folder_path}")
                return False
            
            subprocess.Popen(
                ["code", folder_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            logger.info(f"Opened folder in VS Code: {folder_path}")
            return True
        except Exception as e:
            logger.error(f"Error opening folder in VS Code: {e}")
            return False

    def run_python_code(self, code: str, file_path: Optional[str] = None) -> Tuple[str, str]:
        """Run Python code and capture output."""
        try:
            if file_path is None:
                file_path = "temp_code.py"
            
            # Write code to file
            with open(file_path, 'w') as f:
                f.write(code)
            
            # Execute
            result = subprocess.run(
                [sys.executable, file_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            self.execution_history.append({
                "file": file_path,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            })
            
            logger.info(f"Executed Python code from {file_path}")
            return result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            logger.error(f"Execution timeout for {file_path}")
            return "", "Execution timeout"
        except Exception as e:
            logger.error(f"Error executing Python code: {e}")
            return "", str(e)

    def run_terminal_command(self, command: str, cwd: Optional[str] = None) -> Tuple[str, str]:
        """Run terminal command safely."""
        try:
            # Security: prevent dangerous commands
            dangerous_commands = [
                "rm -rf /", "format", "del /s", "shutdown", "reboot",
                "mkfs", "dd if=/dev/zero"
            ]
            
            cmd_lower = command.lower()
            for dangerous in dangerous_commands:
                if dangerous in cmd_lower:
                    logger.warning(f"Dangerous command blocked: {command}")
                    return "", "Command blocked for safety reasons"
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=cwd
            )
            
            self.execution_history.append({
                "command": command,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            })
            
            logger.info(f"Executed terminal command: {command}")
            return result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            logger.error(f"Command timeout: {command}")
            return "", "Command timeout"
        except Exception as e:
            logger.error(f"Error running terminal command: {e}")
            return "", str(e)

    def analyze_project_errors(self, project_dir: str) -> Dict[str, List[str]]:
        """Analyze project for errors (using linters/type checkers)."""
        try:
            errors = {
                "syntax_errors": [],
                "type_errors": [],
                "lint_warnings": [],
                "import_errors": []
            }
            
            # Check for Python files
            for root, dirs, files in os.walk(project_dir):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        
                        # Run flake8 if available
                        try:
                            stdout, stderr = self.run_terminal_command(
                                f"flake8 {file_path}"
                            )
                            if stdout:
                                errors["lint_warnings"].extend(stdout.split('\n'))
                        except:
                            pass
                        
                        # Try to import to find import errors
                        try:
                            with open(file_path, 'r') as f:
                                compile(f.read(), file_path, 'exec')
                        except SyntaxError as e:
                            errors["syntax_errors"].append(
                                f"{file_path}: {e.msg}"
                            )
                        except Exception as e:
                            errors["import_errors"].append(
                                f"{file_path}: {str(e)}"
                            )
            
            logger.info(f"Analyzed project errors in {project_dir}")
            return errors
        except Exception as e:
            logger.error(f"Error analyzing project: {e}")
            return {}

    def get_execution_history(self) -> List[Dict]:
        """Get execution history."""
        return self.execution_history

    def clear_execution_history(self) -> None:
        """Clear execution history."""
        self.execution_history.clear()
