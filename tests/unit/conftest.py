import pytest
from shmessy import TypesHandler


@pytest.fixture
def type_handler():
    return TypesHandler(ignore_virtual_types=True)
