import pytest
import os
from omegaconf import OmegaConf

import pymasep.common as common
from pymasep.utils import remove_recursive_file

@pytest.fixture(scope="function")
def mock_game(game_class):
    """
    Create a mock game for the current project with empty configuration
    """
    cfg = OmegaConf.create()
    cfg['root_path'] = '.'
    yield game_class(cfg=cfg)


@pytest.fixture(scope="function")
def mock_environment(mock_game):
    """
    Create a mock environment for the current project with empty configuration
    """
    env = common.Environment()
    env.game = mock_game
    yield env


@pytest.fixture(scope="function")
def mock_environment_conf(configuration, game_class):
    """
    Create a mock environment for the current project with configuration defined as fixture
    """
    env = common.Environment()
    game = game_class(configuration)
    env.game = game
    yield env


@pytest.fixture(scope="function")
def base_directory(relative_path, request):
    """
    Pytest fixture that set the base directory for the tests
    """
    directory = os.path.dirname(request.node.fspath)
    yield os.path.join(directory, relative_path)


@pytest.fixture(scope="function")
def base_directory_unit(relative_path, request):
    """
    Pytest fixture that set the base directory for the unit tests
    """
    directory = os.path.dirname(request.node.fspath)
    yield os.path.join(directory, relative_path, 'unit')


@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    """Cleanup a testing directory once we are finished."""

    def remove_test_dir():
        directory = os.path.dirname(os.path.realpath(request.session.path))
        remove_recursive_file(directory, '*.log')
        remove_recursive_file(directory, 'logs')

    request.addfinalizer(remove_test_dir)