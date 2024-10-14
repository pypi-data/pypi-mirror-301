"""
File operations module for Git Mirror.

This module provides classes for handling file-related operations,
including file caching and file tree handling.
"""

from pathlib import Path
from typing import Dict, List


class FileTreeHandler:
    """
    A class for handling file tree operations including copying and change detection.
    """

    def __init__(self, git_ops):
        """
        Initialize the FileTreeHandler.

        Parameters
        ----------
        file_cache : FileCache
            FileCache object for tracking file changes.
        git_ops : GitOperations
            GitOperations object for Git-related file operations.
        """
        self.git_ops = git_ops

    def should_ignore(self, file_path: str, ignore_patterns: List[str]) -> bool:
        """
        Check if a file should be ignored based on ignore patterns.

        Parameters
        ----------
        file_path : str
            Path to the file.
        ignore_patterns : list of str
            List of glob patterns for files to ignore.

        Returns
        -------
        bool
            True if the file should be ignored, False otherwise.
        """
        for pattern in ignore_patterns:
            if Path(file_path).match(pattern):
                return True
        return False

    def copy_file_tree(
        self, src_dir: Path, dest_dir: Path, ignore_patterns: List[str]
    ) -> None:
        """
        Copy the file tree from source to destination, updating only changed files.

        Parameters
        ----------
        src_dir : Path
            Source directory.
        dest_dir : Path
            Destination directory.
        ignore_patterns : list of str
            List of glob patterns for files to ignore.
        """
        for src_path in src_dir.rglob("*"):
            if src_path.is_file() and not self.should_ignore(src_path, ignore_patterns):
                relative_path = src_path.relative_to(src_dir)
                dest_path = dest_dir / relative_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                self.git_ops.copy_file(src_path, dest_path)

    def detect_file_changes(self, src_dir: Path, dest_dir: Path) -> Dict[str, str]:
        """
        Detect changes between source and destination directories.

        Parameters
        ----------
        src_dir : Path
            Source directory.
        dest_dir : Path
            Destination directory.

        Returns
        -------
        dict
            Dictionary of changed files with their change types ('added', 'modified', or 'deleted').
        """
        changes = {}
        for src_path in src_dir.rglob("*"):
            if src_path.is_file():
                relative_path = src_path.relative_to(src_dir)
                dest_path = dest_dir / relative_path
                if not dest_path.exists():
                    changes[str(relative_path)] = "added"

        for dest_path in dest_dir.rglob("*"):
            if dest_path.is_file():
                relative_path = dest_path.relative_to(dest_dir)
                src_path = src_dir / relative_path
                if not src_path.exists():
                    changes[str(relative_path)] = "deleted"

        return changes
