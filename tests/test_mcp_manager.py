import subprocess
from unittest.mock import patch, MagicMock
from pathlib import Path
import pytest
import json

# Adjust path to import from the parent directory
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from SuperClaude.mcp_manager import MCPManager

@pytest.fixture
def manager():
    """Fixture to create an instance of MCPManager with a mocked registry."""
    with patch('SuperClaude.mcp_manager.MCPManager._load_mcp_registry', return_value={
        "test-mcp": {
            "name": "test-mcp",
            "description": "A test MCP server.",
            "npm_package": "@test/mcp"
        },
        "another-mcp": {
            "name": "another-mcp",
            "description": "Another test MCP server.",
            "npm_package": "@another/mcp"
        }
    }) as mock_load:
        yield MCPManager()

@patch('subprocess.run')
def test_install_mcp_success(mock_run, manager):
    """Test successful installation of a new MCP server."""
    # First call to check if installed (returns not found), second to install
    mock_run.side_effect = [
        MagicMock(stdout="", returncode=0), # Not installed
        MagicMock(stdout="Success!", returncode=0) # Install succeeds
    ]

    success, message = manager.install_mcp("test-mcp")

    assert success is True
    assert "Successfully installed MCP server 'test-mcp'" in message

    # Check that the correct claude command was called
    install_call = mock_run.call_args_list[1]
    expected_command = ["claude", "mcp", "add", "-s", "user", "--", "test-mcp", "npx", "-y", "@test/mcp"]
    assert install_call[0][0] == expected_command

@patch('subprocess.run')
def test_install_mcp_already_installed(mock_run, manager):
    """Test attempting to install an MCP server that is already installed."""
    # `claude mcp list` shows the server is installed
    mock_run.return_value = MagicMock(stdout="test-mcp: ...", returncode=0)

    success, message = manager.install_mcp("test-mcp")

    assert success is True
    assert "MCP server 'test-mcp' is already installed" in message
    mock_run.assert_called_once_with(
        ["claude", "mcp", "list"], capture_output=True, text=True, timeout=15, shell=(sys.platform == "win32")
    )

def test_install_mcp_not_in_registry(manager):
    """Test installing an MCP server that does not exist in the registry."""
    success, message = manager.install_mcp("non-existent-mcp")
    assert success is False
    assert message == "Error: MCP server 'non-existent-mcp' not found in registry."

@patch('subprocess.run')
def test_install_mcp_claude_cli_not_found(mock_run, manager):
    """Test error handling when the 'claude' CLI is not found."""
    mock_run.side_effect = FileNotFoundError

    success, message = manager.install_mcp("test-mcp")

    assert success is False
    assert message == "Error: 'claude' CLI not found. Please ensure it is installed and in your PATH."

@patch('subprocess.run')
def test_install_mcp_install_fails(mock_run, manager):
    """Test when the 'claude mcp add' command fails."""
    mock_run.side_effect = [
        MagicMock(stdout="", returncode=0), # Not installed
        MagicMock(stderr="Installation failed.", returncode=1) # Install fails
    ]

    success, message = manager.install_mcp("test-mcp")

    assert success is False
    assert message.startswith("Failed to install MCP server 'test-mcp'. Error: Installation failed.")

# タイムアウト例外のテスト追加
@patch('subprocess.run')
def test_install_mcp_timeout(mock_run, manager):
    """Test when installation times out."""
    mock_run.side_effect = [
        MagicMock(stdout="", returncode=0), # Not installed
        subprocess.TimeoutExpired(cmd="claude", timeout=180) # Timeout
    ]
    success, message = manager.install_mcp("test-mcp")
    assert success is False
    assert message == "Installation of MCP server 'test-mcp' timed out."

# 予期せぬ例外のテスト追加
@patch('subprocess.run')
def test_install_mcp_unexpected_exception(mock_run, manager):
    """Test when an unexpected exception occurs during installation."""
    mock_run.side_effect = [
        MagicMock(stdout="", returncode=0), # Not installed
        Exception("Unexpected error!") # Unexpected exception
    ]
    success, message = manager.install_mcp("test-mcp")
    assert success is False
    assert message.startswith("An unexpected error occurred during installation: Unexpected error!")
