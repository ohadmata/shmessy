import pytest


@pytest.fixture
def type_handler():
    from src.shmessy import TypesHandler  # if imported outside the function, coverage drops from 92% to 64%
    return TypesHandler(ignore_virtual_types=True)
