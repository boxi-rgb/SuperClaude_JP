import subprocess
from unittest.mock import patch, MagicMock
from pathlib import Path
import pytest

# Since the tests directory is at the same level as SuperClaude, we need to adjust the path
# to allow importing from SuperClaude. This is a common pattern in testing.
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from SuperClaude.mcp_diagnostics import MCPDiagnostics

@pytest.fixture
def diagnostics():
    """Fixture to create an instance of MCPDiagnostics."""
    return MCPDiagnostics()

@patch('subprocess.run')
def test_check_prerequisites_all_found(mock_run, diagnostics, capsys):
    """Test prerequisite check when all commands are found."""
    mock_run.return_value = MagicMock(stdout="v1.2.3", returncode=0)

    diagnostics.check_prerequisites()

    captured = capsys.readouterr()
    assert "✅ Node found: v1.2.3" in captured.out
    assert "✅ Npm found: v1.2.3" in captured.out
    assert "✅ Claude found: v1.2.3" in captured.out
    assert mock_run.call_count == 3

@patch('subprocess.run')
def test_check_prerequisites_one_missing(mock_run, diagnostics, capsys):
    """Test prerequisite check when one command is missing."""
    mock_run.side_effect = [
        MagicMock(stdout="v18.0.0", returncode=0),
        FileNotFoundError,
        MagicMock(stdout="v0.1.0", returncode=0),
    ]

    diagnostics.check_prerequisites()

    captured = capsys.readouterr()
    assert "✅ Node found: v18.0.0" in captured.out
    assert "❌ Npm not found." in captured.out
    assert "✅ Claude found: v0.1.0" in captured.out

@patch('os.getenv')
def test_check_api_keys(mock_getenv, diagnostics, capsys):
    """Test API key check for set and unset keys."""
    # Simulate the registry having an MCP that needs a key
    diagnostics.registry = {
        "magic": {"api_key_env": "MAGIC_KEY"},
        "another_mcp": {"api_key_env": "ANOTHER_KEY"},
    }

    # Mock one key as set, the other as not set
    mock_getenv.side_effect = lambda key: "a_secret_value" if key == "MAGIC_KEY" else None

    diagnostics.check_api_keys()

    captured = capsys.readouterr()
    assert "✅ API key for 'magic' (MAGIC_KEY) is set." in captured.out
    assert "⚠️  API key for 'another_mcp' (ANOTHER_KEY) is NOT set." in captured.out

@patch('subprocess.run')
@patch('pathlib.Path.exists')
def test_check_configurations(mock_path_exists, mock_run, diagnostics, capsys):
    """Test configuration checks and validation against registry."""
    # First call to exists() is for global, second is for local.
    # Simulate global config exists, but local does not.
    mock_path_exists.side_effect = [True, False]

    # Simulate output from `claude mcp list`
    mock_run.return_value = MagicMock(
        stdout="sequential-thinking: ...\nplaywright: ...\nmisspelled-server: ...",
        returncode=0
    )

    # Mock the registry
    diagnostics.registry = {
        "sequential-thinking": {},
        "playwright": {},
        "magic": {} # In registry but not installed
    }

    diagnostics.check_configurations()

    captured = capsys.readouterr()
    assert "✅ Found global config" in captured.out
    assert "ℹ️  No local .mcp.json file found" in captured.out
    assert "✅ `claude mcp list` output:" in captured.out
    assert "✅ Matches official registry name: 'sequential-thinking'" in captured.out
    assert "✅ Matches official registry name: 'playwright'" in captured.out
    assert "⚠️  Server name 'misspelled-server' is not in the official registry." in captured.out

@patch('subprocess.Popen')
def test_server_liveness_scenarios(mock_popen, diagnostics, capsys):
    """Test the liveness check with various server responses."""
    installed_servers = [
        "good-server: npx good-package",
        "bad-server: npx bad-package",
        "timeout-server: npx timeout-package"
    ]

    # Configure the mock for Popen
    mock_process_good = MagicMock()
    mock_process_good.communicate.return_value = ('{"jsonrpc":"2.0","result":{...},"id":1}', '')
    mock_process_good.returncode = 0

    mock_process_bad = MagicMock()
    mock_process_bad.communicate.return_value = ('', 'Error: Failed to start')
    mock_process_bad.returncode = 1

    mock_process_timeout = MagicMock()
    mock_process_timeout.communicate.side_effect = subprocess.TimeoutExpired(cmd="npx", timeout=15)

    # The mock_popen constructor will return these mocks in order
    mock_popen.side_effect = [mock_process_good, mock_process_bad, mock_process_timeout]

    diagnostics.test_server_liveness(installed_servers)

    captured = capsys.readouterr()
    # Check for good server
    assert "✅ Liveness check PASSED for 'good-server'" in captured.out
    # Check for bad server
    assert "❌ Liveness check FAILED for 'bad-server'" in captured.out
    assert "Error: Failed to start" in captured.out
    # Check for timeout server
    assert "❌ Liveness check TIMED OUT for 'timeout-server'" in captured.out
