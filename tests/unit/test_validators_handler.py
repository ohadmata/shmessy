import pytest

from shmessy.validators_handler import ValidatorsHandler
from parametrization import Parametrization


@pytest.fixture
def validators_handler() -> ValidatorsHandler:
    return ValidatorsHandler()


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="init file should not identified as validator",
    filename="__init__.py",
    expected_output=False,
)
@Parametrization.case(
    name="Ignore base class - Should not considered as validator",
    filename="base.py",
    expected_output=False,
)
@Parametrization.case(
    name="Legit validator",
    filename="datetime.py",
    expected_output=True,
)
def test_is_validator(filename, expected_output, validators_handler):
    assert validators_handler._is_validator(filename) == expected_output
