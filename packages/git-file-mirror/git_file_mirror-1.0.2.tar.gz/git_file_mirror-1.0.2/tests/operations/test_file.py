import json
import os
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from gitmirror.operations.file import FileTreeHandler


@pytest.fixture
def mock_git_ops():
    return Mock()


@pytest.fixture
def file_tree_handler(mock_git_ops):
    return FileTreeHandler(mock_git_ops)


def test_file_tree_handler_initialization(file_tree_handler, mock_git_ops):
    assert file_tree_handler.git_ops == mock_git_ops


@pytest.mark.parametrize(
    "file_path, ignore_patterns, expected",
    [
        ("file.txt", ["*.log"], False),
        ("file.log", ["*.log"], True),
        ("path/to/file.txt", ["path/to/*.txt"], True),
        ("file.tmp", ["*.tmp", "*.log"], True),
    ],
)
def test_should_ignore(file_tree_handler, file_path, ignore_patterns, expected):
    assert file_tree_handler.should_ignore(file_path, ignore_patterns) == expected


@pytest.fixture
def mock_directory_structure(tmp_path):
    src_dir = tmp_path / "src"
    dest_dir = tmp_path / "dest"
    src_dir.mkdir()
    dest_dir.mkdir()

    (src_dir / "file1.txt").write_text("content1")
    (src_dir / "file2.txt").write_text("content2")
    (src_dir / "ignoreme.log").write_text("log content")

    return src_dir, dest_dir


def test_copy_file_tree(file_tree_handler, mock_directory_structure):
    src_dir, dest_dir = mock_directory_structure
    ignore_patterns = ["*.log"]

    file_tree_handler.git_ops.get_file_hash.side_effect = (
        lambda x: f"hash_of_{Path(x).name}"
    )
    file_tree_handler.git_ops.copy_file.side_effect = lambda src, dest: shutil.copy2(
        src, dest
    )

    file_tree_handler.copy_file_tree(src_dir, dest_dir, ignore_patterns)

    assert (dest_dir / "file1.txt").exists()
    assert (dest_dir / "file2.txt").exists()
    assert not (dest_dir / "ignoreme.log").exists()
    assert file_tree_handler.git_ops.copy_file.call_count == 2


def test_detect_file_changes(file_tree_handler, mock_directory_structure):
    src_dir, dest_dir = mock_directory_structure
    (dest_dir / "old_file.txt").write_text("old content")

    file_tree_handler.git_ops.get_file_hash.side_effect = (
        lambda x: f"hash_of_{Path(x).name}"
    )

    changes = file_tree_handler.detect_file_changes(src_dir, dest_dir)

    assert changes == {
        "file1.txt": "added",
        "file2.txt": "added",
        "ignoreme.log": "added",
        "old_file.txt": "deleted",
    }


# Integration test


def test_file_operations_integration(mock_directory_structure):
    src_dir, dest_dir = mock_directory_structure
    git_ops = Mock()
    git_ops.copy_file = Mock(side_effect=lambda src, dest: shutil.copy2(src, dest))

    handler = FileTreeHandler(git_ops)

    # First run: copy all files
    handler.copy_file_tree(src_dir, dest_dir, ["*.log"])

    assert (dest_dir / "file1.txt").exists()
    assert (dest_dir / "file2.txt").exists()
    assert not (dest_dir / "ignoreme.log").exists()

    # Modify a file and run again
    (src_dir / "file1.txt").write_text("modified content")

    handler.copy_file_tree(src_dir, dest_dir, ["*.log"])

    assert (dest_dir / "file1.txt").read_text() == "modified content"
    assert git_ops.copy_file.call_count == 4  # 2 from first run, 1 from second run


if __name__ == "__main__":
    pytest.main()
