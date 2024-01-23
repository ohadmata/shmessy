from pathlib import Path

import pytest


@pytest.fixture
def files_folder() -> Path:
    folder_path = Path(__file__).parent / 'data'
    assert folder_path.exists()
    return folder_path
