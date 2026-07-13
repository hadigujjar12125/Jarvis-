#!/usr/bin/env python3
"""File editing module for JARVIS Pro."""

import os
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import shutil
import re

logger = logging.getLogger(__name__)


class FileEditor:
    """Manage file operations including read, write, search, and navigation."""

    def __init__(self):
        """Initialize file editor."""
        self.current_directory = os.getcwd()
        self.file_history: List[str] = []
        self.supported_extensions = {
            '.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.json',
            '.yaml', '.yml', '.xml', '.md', '.txt', '.sql', '.java', '.cpp',
            '.c', '.h', '.cs', '.php', '.rb', '.go', '.rs'
        }

    def read_file(self, file_path: str) -> Optional[str]:
        """Read file contents."""
        try:
            full_path = self._resolve_path(file_path)
            
            if not os.path.exists(full_path):
                logger.warning(f"File not found: {full_path}")
                return None
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.file_history.append(full_path)
            logger.info(f"Read file: {full_path}")
            return content
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            return None

    def write_file(self, file_path: str, content: str, create_dirs: bool = True) -> bool:
        """Write content to file."""
        try:
            full_path = self._resolve_path(file_path)
            
            if create_dirs:
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.file_history.append(full_path)
            logger.info(f"Wrote file: {full_path}")
            return True
        except Exception as e:
            logger.error(f"Error writing file: {e}")
            return False

    def append_file(self, file_path: str, content: str) -> bool:
        """Append content to file."""
        try:
            full_path = self._resolve_path(file_path)
            
            if not os.path.exists(full_path):
                logger.warning(f"File not found: {full_path}")
                return False
            
            with open(full_path, 'a', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Appended to file: {full_path}")
            return True
        except Exception as e:
            logger.error(f"Error appending to file: {e}")
            return False

    def modify_file(self, file_path: str, replacements: Dict[str, str]) -> bool:
        """Replace content in file."""
        try:
            content = self.read_file(file_path)
            if content is None:
                return False
            
            for old, new in replacements.items():
                content = content.replace(old, new)
            
            return self.write_file(file_path, content)
        except Exception as e:
            logger.error(f"Error modifying file: {e}")
            return False

    def rename_file(self, old_path: str, new_path: str) -> bool:
        """Rename file."""
        try:
            old_full = self._resolve_path(old_path)
            new_full = self._resolve_path(new_path)
            
            if not os.path.exists(old_full):
                logger.warning(f"File not found: {old_full}")
                return False
            
            os.rename(old_full, new_full)
            logger.info(f"Renamed {old_full} to {new_full}")
            return True
        except Exception as e:
            logger.error(f"Error renaming file: {e}")
            return False

    def delete_file(self, file_path: str, confirm: bool = True) -> bool:
        """Delete file safely."""
        try:
            full_path = self._resolve_path(file_path)
            
            if not os.path.exists(full_path):
                logger.warning(f"File not found: {full_path}")
                return False
            
            # Create backup before deletion
            backup_path = full_path + ".backup"
            shutil.copy2(full_path, backup_path)
            
            os.remove(full_path)
            logger.info(f"Deleted file: {full_path} (backup: {backup_path})")
            return True
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            return False

    def search_files(self, directory: str, pattern: str, 
                    search_content: bool = False) -> List[str]:
        """Search for files by name or content."""
        try:
            full_dir = self._resolve_path(directory)
            results = []
            
            if search_content:
                # Search in file contents
                for root, dirs, files in os.walk(full_dir):
                    # Skip hidden directories
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                    
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                if re.search(pattern, f.read(), re.IGNORECASE):
                                    results.append(file_path)
                        except:
                            pass
            else:
                # Search by filename
                for root, dirs, files in os.walk(full_dir):
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                    
                    for file in files:
                        if re.search(pattern, file, re.IGNORECASE):
                            results.append(os.path.join(root, file))
            
            logger.info(f"Found {len(results)} files matching pattern: {pattern}")
            return results
        except Exception as e:
            logger.error(f"Error searching files: {e}")
            return []

    def get_project_structure(self, directory: Optional[str] = None, 
                             max_depth: int = 3) -> Dict:
        """Get project directory structure."""
        try:
            if directory is None:
                directory = self.current_directory
            
            full_dir = self._resolve_path(directory)
            
            def build_tree(path: str, depth: int = 0) -> Dict:
                if depth > max_depth:
                    return {}
                
                tree = {}
                try:
                    items = os.listdir(path)
                    for item in items:
                        if item.startswith('.'):
                            continue
                        
                        item_path = os.path.join(path, item)
                        if os.path.isdir(item_path):
                            tree[item] = build_tree(item_path, depth + 1)
                        else:
                            tree[item] = "file"
                except PermissionError:
                    pass
                
                return tree
            
            structure = build_tree(full_dir)
            logger.info(f"Generated project structure for {full_dir}")
            return structure
        except Exception as e:
            logger.error(f"Error getting project structure: {e}")
            return {}

    def _resolve_path(self, path: str) -> str:
        """Resolve relative path to absolute."""
        if os.path.isabs(path):
            return path
        return os.path.join(self.current_directory, path)

    def get_file_history(self) -> List[str]:
        """Get file access history."""
        return self.file_history

    def clear_history(self) -> None:
        """Clear file history."""
        self.file_history.clear()
