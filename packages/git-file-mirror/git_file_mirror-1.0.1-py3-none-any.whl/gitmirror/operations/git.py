"""
Git operations module for Git Mirror.

This module provides a class for handling Git-related operations,
including repository cloning, pushing changes, and file hashing.
"""

import hashlib
import os
import shutil
import subprocess
from pathlib import Path
from typing import List


class GitOperations:
    """
    A class for handling Git-related operations.
    """

    @staticmethod
    def clone_repository(
        git_url: str,
        base_branch: str,
        temp_repo_path: str,
        folders_to_include: List[str],
    ) -> None:
        """
        Clone a Git repository with sparse checkout.

        Parameters
        ----------
        git_url : str
            URL of the Git repository.
        base_branch : str
            Name of the branch to clone.
        temp_repo_path : str
            Path where the repository should be cloned.
        folders_to_include : list of str
            List of folders to include in the sparse checkout.
        """
        subprocess.run(
            [
                "git",
                "clone",
                "--filter=blob:none",
                "--sparse",
                git_url,
                "-b",
                base_branch,
                temp_repo_path,
            ],
            check=True,
        )
        subprocess.run(
            ["git", "sparse-checkout", "init", "--cone"], cwd=temp_repo_path, check=True
        )
        subprocess.run(
            ["git", "sparse-checkout", "set"] + folders_to_include,
            cwd=temp_repo_path,
            check=True,
        )
        if folders_to_include:
            subprocess.run(
                ["git", "sparse-checkout", "set"] + folders_to_include,
                cwd=temp_repo_path,
                check=True,
            )
        else:
            subprocess.run(
                ["git", "sparse-checkout", "disable"], cwd=temp_repo_path, check=True
            )

    @staticmethod
    def push_changes(
        temp_repo_path: str, commit_msg: str, new_branch: str = None
    ) -> str:
        """
        Commit and push changes to the repository.

        Parameters
        ----------
        temp_repo_path : str
            Path to the local repository.
        commit_msg : str
            Commit message.
        new_branch : str, optional
            Name of the new branch to create and push to.

        Returns
        -------
        str
            The commit hash of the pushed changes.
        """
        subprocess.run(["git", "add", "."], cwd=temp_repo_path, check=True)
        subprocess.run(
            ["git", "commit", "-m", commit_msg], cwd=temp_repo_path, check=True
        )
        if new_branch:
            subprocess.run(
                ["git", "checkout", "-b", new_branch], cwd=temp_repo_path, check=True
            )
        subprocess.run(
            ["git", "push", "origin", new_branch or "HEAD"],
            cwd=temp_repo_path,
            check=True,
        )
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=temp_repo_path, universal_newlines=True
        ).strip()

    @staticmethod
    def copy_file(src_path: Path, dest_path: Path) -> None:
        """
        Copy a file from source to destination.

        Parameters
        ----------
        src_path : Path
            Source file path.
        dest_path : Path
            Destination file path.
        """
        shutil.copy2(src_path, dest_path)
