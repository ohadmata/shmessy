import pytest
from src.shmessy import TypesHandler  # if imported outside the function, coverage drops from 92% to 64%


@pytest.fixture
def type_handler():
    return TypesHandler(ignore_virtual_types=True)
