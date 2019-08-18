import pytest

from cazart import Cazart


@pytest.fixture
def cazart():
    return Cazart(__name__)
