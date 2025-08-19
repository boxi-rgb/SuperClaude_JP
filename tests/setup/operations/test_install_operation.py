import pytest
from unittest.mock import MagicMock, patch
import argparse
from pathlib import Path

# Use a try-except block for the import to handle different path contexts
try:
    from setup.operations import install as install_operation
except ImportError:
    pass

# A simple namespace mock for args
class ArgsMock(argparse.Namespace):
    def __init__(self, **kwargs):
        super().__init__()
        self.verbose = False
        self.quiet = False
        self.install_dir = Path("/home/testuser/.claude") # Default path
        self.dry_run = False
        self.force = False
        self.yes = True # Assume yes to avoid interactive prompts
        self.list_components = False
        self.diagnose = False
        self.components = None
        self.profile = None
        self.quick = False
        self.minimal = False
        self.no_backup = False
        for key, value in kwargs.items():
            setattr(self, key, value)

@pytest.fixture
def mock_home(mocker):
    """Mocks pathlib.Path.home() to return a consistent test path."""
    home_path = Path("/home/testuser")
    mocker.patch('pathlib.Path.home', return_value=home_path)
    return home_path

@patch('setup.operations.install.get_logger')
@patch('setup.operations.install.InstallOperation')
def test_run_orchestration_happy_path(MockInstallOperation, mock_get_logger, mocker, mock_home):
    """
    Test the main 'run' function's orchestration on a successful install path.
    """
    # 1. Setup Mocks for all imported functions
    mocker.patch('setup.operations.install.display_header')
    mocker.patch('setup.operations.install.run_system_diagnostics')
    mocker.patch('setup.operations.install.get_components_to_install', return_value=['core'])
    mocker.patch('setup.operations.install.validate_system_requirements', return_value=True)
    mocker.patch('setup.operations.install.display_installation_plan')
    mocker.patch('setup.operations.install.perform_installation', return_value=True)
    mocker.patch('setup.operations.install.display_success')

    mock_op_instance = MockInstallOperation.return_value
    mock_op_instance.validate_global_args.return_value = (True, [])

    # 2. Call the run function with standard args
    args = ArgsMock(install_dir=mock_home / ".claude")
    result = install_operation.run(args)

    # 3. Assertions
    assert result == 0
    install_operation.get_components_to_install.assert_called_once()
    install_operation.validate_system_requirements.assert_called_once()
    install_operation.display_installation_plan.assert_called_once()
    install_operation.perform_installation.assert_called_once()
    install_operation.display_success.assert_called_once()
    install_operation.run_system_diagnostics.assert_not_called()

@patch('setup.operations.install.get_logger')
@patch('setup.operations.install.InstallOperation')
def test_run_with_diagnose_flag(MockInstallOperation, mock_get_logger, mocker, mock_home):
    """
    Test that the '--diagnose' flag correctly calls run_system_diagnostics.
    """
    mocker.patch('setup.operations.install.display_header')
    mocker.patch('setup.operations.install.run_system_diagnostics')
    mocker.patch('setup.operations.install.perform_installation')

    mock_op_instance = MockInstallOperation.return_value
    mock_op_instance.validate_global_args.return_value = (True, [])

    args = ArgsMock(diagnose=True, install_dir=mock_home / ".claude")
    result = install_operation.run(args)

    assert result == 0
    install_operation.run_system_diagnostics.assert_called_once()
    install_operation.perform_installation.assert_not_called()

@patch('setup.operations.install.get_logger')
@patch('setup.operations.install.InstallOperation')
def test_run_component_selection_fails(MockInstallOperation, mock_get_logger, mocker, mock_home):
    """
    Test that the run function exits correctly if component selection returns None.
    """
    mocker.patch('setup.operations.install.display_header')
    mocker.patch('setup.operations.install.get_components_to_install', return_value=None)
    mocker.patch('setup.operations.install.perform_installation')

    mock_op_instance = MockInstallOperation.return_value
    mock_op_instance.validate_global_args.return_value = (True, [])

    args = ArgsMock(install_dir=mock_home / ".claude")
    result = install_operation.run(args)

    assert result == 1
    install_operation.get_components_to_install.assert_called_once()
    install_operation.perform_installation.assert_not_called()
