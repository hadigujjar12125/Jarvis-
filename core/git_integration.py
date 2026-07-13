#!/usr/bin/env python3
"""Git integration module for JARVIS Pro."""

import os
import subprocess
import logging
from typing import Optional, List, Dict, Tuple

logger = logging.getLogger(__name__)


class GitIntegration:
    """Handle Git operations including commits, branches, and pushing."""

    def __init__(self, repo_path: Optional[str] = None):
        """Initialize Git integration."""
        self.repo_path = repo_path or os.getcwd()
        self.git_available = self._check_git()
        self.commit_history: List[Dict] = []

    def _check_git(self) -> bool:
        """Check if Git is installed."""
        try:
            result = subprocess.run(
                ["git", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            logger.warning("Git not found")
            return False

    def initialize_repo(self, repo_path: Optional[str] = None) -> bool:
        """Initialize a new Git repository."""
        try:
            if repo_path:
                target_path = repo_path
            else:
                target_path = self.repo_path
            
            os.makedirs(target_path, exist_ok=True)
            
            result = subprocess.run(
                ["git", "init"],
                cwd=target_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info(f"Git repository initialized at {target_path}")
                self.repo_path = target_path
                return True
            else:
                logger.error(f"Failed to initialize git repo: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Error initializing repo: {e}")
            return False

    def add_files(self, files: Optional[List[str]] = None) -> bool:
        """Stage files for commit."""
        try:
            if files is None:
                # Stage all files
                cmd = ["git", "add", "."]
            else:
                # Stage specific files
                cmd = ["git", "add"] + files
            
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info(f"Files staged: {files or 'all'}")
                return True
            else:
                logger.error(f"Failed to stage files: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Error staging files: {e}")
            return False

    def commit(self, message: str, ai_generated: bool = False) -> bool:
        """Commit changes with message."""
        try:
            if not message:
                logger.warning("Empty commit message")
                return False
            
            # If AI-generated, add prefix
            if ai_generated:
                message = f"[JARVIS] {message}"
            
            result = subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.commit_history.append({
                    "message": message,
                    "output": result.stdout
                })
                logger.info(f"Committed: {message}")
                return True
            else:
                logger.error(f"Failed to commit: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Error committing: {e}")
            return False

    def generate_commit_message(self, ai_agent, changes: str) -> str:
        """Generate commit message using AI."""
        try:
            prompt = f"""Generate a concise, professional Git commit message for these changes:

{changes}

Requirements:
1. Start with type: feat, fix, docs, style, refactor, test, chore
2. Keep under 50 characters
3. Use imperative mood
4. Be descriptive but concise
5. Return ONLY the commit message, no explanation"""

            message = ai_agent.ask(prompt)
            return message.strip()
        except Exception as e:
            logger.error(f"Error generating commit message: {e}")
            return "Update code"

    def create_branch(self, branch_name: str) -> bool:
        """Create and switch to new branch."""
        try:
            result = subprocess.run(
                ["git", "checkout", "-b", branch_name],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info(f"Branch created: {branch_name}")
                return True
            else:
                logger.error(f"Failed to create branch: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Error creating branch: {e}")
            return False

    def switch_branch(self, branch_name: str) -> bool:
        """Switch to existing branch."""
        try:
            result = subprocess.run(
                ["git", "checkout", branch_name],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info(f"Switched to branch: {branch_name}")
                return True
            else:
                logger.error(f"Failed to switch branch: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Error switching branch: {e}")
            return False

    def push(self, branch: Optional[str] = None, force: bool = False) -> bool:
        """Push changes to remote."""
        try:
            cmd = ["git", "push"]
            
            if force:
                cmd.append("--force")
            
            if branch:
                cmd.append(branch)
            
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info(f"Pushed to remote (branch: {branch or 'all'})")
                return True
            else:
                logger.error(f"Failed to push: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Error pushing: {e}")
            return False

    def get_status(self) -> Dict[str, List[str]]:
        """Get repository status."""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            status = {
                "modified": [],
                "added": [],
                "deleted": [],
                "untracked": []
            }
            
            for line in result.stdout.split('\n'):
                if line.startswith('M'):
                    status["modified"].append(line[3:])
                elif line.startswith('A'):
                    status["added"].append(line[3:])
                elif line.startswith('D'):
                    status["deleted"].append(line[3:])
                elif line.startswith('??'):
                    status["untracked"].append(line[3:])
            
            logger.info(f"Repository status retrieved")
            return status
        except Exception as e:
            logger.error(f"Error getting status: {e}")
            return {}

    def get_commit_history(self, limit: int = 10) -> List[Dict]:
        """Get commit history."""
        try:
            result = subprocess.run(
                ["git", "log", f"--max-count={limit}", "--pretty=format:%H|%an|%ae|%ad|%s"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            commits = []
            for line in result.stdout.split('\n'):
                if line:
                    parts = line.split('|')
                    commits.append({
                        "hash": parts[0] if len(parts) > 0 else "",
                        "author": parts[1] if len(parts) > 1 else "",
                        "email": parts[2] if len(parts) > 2 else "",
                        "date": parts[3] if len(parts) > 3 else "",
                        "message": parts[4] if len(parts) > 4 else ""
                    })
            
            logger.info(f"Retrieved {len(commits)} commits")
            return commits
        except Exception as e:
            logger.error(f"Error getting commit history: {e}")
            return []
