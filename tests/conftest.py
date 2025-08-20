import os
import shutil
from pathlib import Path

import pytest


@pytest.fixture()
def test_cleaner():
    funcs = []

    def add_func(func):
        funcs.append(func)

    yield add_func
    for func in funcs:
        func()


@pytest.fixture
def files_folder(tests_root) -> Path:
    return tests_root / 'data'


@pytest.fixture
def tests_root() -> Path:
    workspace = Path(os.environ.get("GITHUB_WORKSPACE", Path(__file__).parent.parent.parent))
    return workspace / "tests"


@pytest.fixture
def tmp_files_folder(test_cleaner) -> Path:
    folder_path = Path(__file__).parent / 'tmp_folder_for_tests'
    if folder_path.exists():
        shutil.rmtree(folder_path)
    folder_path.mkdir()
    test_cleaner(lambda: shutil.rmtree(folder_path))
    return folder_path
