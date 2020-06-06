import pytest


def pytest_addoption(parser):
    parser.addoption('--confirm',
                     help='prompt y/n before running each test',
                     action='store_true',
                     default=False)


@pytest.fixture
def confirm(request):
    return request.config.getoption("--confirm")
