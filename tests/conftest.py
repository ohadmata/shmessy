import shutil
from pathlib import Path

import pytest


@pytest.fixture
def files_folder() -> Path:
    folder_path = Path(__file__).parent / 'data'
    assert folder_path.exists()
    return folder_path


@pytest.fixture
def tmp_files_folder() -> Path:
    folder_path = Path(__file__).parent / 'tmp_folder_for_tests'
    if folder_path.exists():
        shutil.rmtree(folder_path)
    folder_path.mkdir()
    return folder_path
