import pytest
import os
from pathlib import Path
from file_sys_utils import get_size, move_dir_content, delete_if_exists


# Setup for the tests: creating temp files/directories
@pytest.fixture(scope="module")
def setup_filesystem(tmp_path_factory):
    # Setup temporary directory structure
    base_temp_dir = tmp_path_factory.mktemp("filesystem_tests")
    src_dir = base_temp_dir / "src"
    dest_dir = base_temp_dir / "dest"
    empty_dir = base_temp_dir / "empty"
    src_dir.mkdir()
    dest_dir.mkdir()
    empty_dir.mkdir()
    # Create files in src directory
    file1 = src_dir / "file1.txt"
    file1.write_text("This is a test file.")
    file2 = src_dir / "file2.txt"
    file2.write_text("Another test file.")
    return base_temp_dir, src_dir, dest_dir, empty_dir, file1, file2


# Test get_size
def test_get_size(setup_filesystem):
    _, src_dir, _, _, file1, file2 = setup_filesystem
    file1_size = file1.stat().st_size
    file2_size = file2.stat().st_size
    total_size = file1_size + file2_size
    assert get_size(src_dir) == total_size
    assert get_size(file1) == file1_size
    assert get_size(file2) == file2_size


# Test move_dir_content
def test_move_dir_content(setup_filesystem):
    _, src_dir, dest_dir, _, file1, file2 = setup_filesystem
    move_dir_content(src_dir, dest_dir)
    assert (dest_dir / file1.name).exists()
    assert (dest_dir / file2.name).exists()
    assert not (src_dir / file1.name).exists()
    assert not (src_dir / file2.name).exists()


# Test delete_if_exists
def test_delete_if_exists(setup_filesystem):
    base_temp_dir, _, _, empty_dir, _, _ = setup_filesystem
    # Testing with directory
    assert empty_dir.exists()
    delete_if_exists(empty_dir)
    assert not empty_dir.exists()
    # Testing with non-existing path
    non_existing_path = base_temp_dir / "nonexistent"
    delete_if_exists(non_existing_path)  # Should not raise error
    assert not non_existing_path.exists()
