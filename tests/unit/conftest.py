import pytest
from shmessy import TypesHandler


@pytest.fixture
def type_handler():
    return TypesHandler(types_to_ignore=["email", "ipv4"])
