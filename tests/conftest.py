import pytest

import true_north


@pytest.fixture(autouse=True)
def disable_colors():
    true_north.disable_colors()
    yield
    true_north.reset_colors()
