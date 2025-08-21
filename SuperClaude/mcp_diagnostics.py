import subprocess
import sys
import json
import os
from pathlib import Path
from typing import List, Dict, Any

from setup.utils.logger import get_logger
from setup.utils.ui import display_info, display_error, display_warning


class MCPDiagnostics:
    """Runs a series of checks to diagnose MCP server issues."""

    def __init__(self) -> None:
        """Initialize the diagnostics tool."""
        # To avoid circular imports we load the registry directly
        self.registry: Dict[str, Any] = self._load_mcp_registry()
        self.logger = get_logger("superclaude.diagnostics")

    def _load_mcp_registry(self) -> Dict[str, Any]:
        """Load the MCP server registry from the JSON file."""
        try:
            registry_path = Path(__file__).parent.parent / "config/mcp_registry.json"
            with open(registry_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def run(self) -> None:
        """Run all diagnostic checks and produce a report via UI/logger."""
        display_info("Starting MCP Diagnostics...")
        self.check_prerequisites()

        # This method returns installed servers for liveness testing
        installed_servers = self.check_configurations()

        self.test_server_liveness(installed_servers)

        self.check_api_keys()
        display_info("Diagnostics complete.")

    def check_prerequisites(self) -> None:
        """Level 1: Check for node, npm, and claude CLI."""
        display_info("LEVEL 1: Checking Prerequisites...")
        self._check_command("node")
        self._check_command("npm")
        self._check_command("claude")

    def _check_command(self, command: str) -> None:
        """Helper to check for a command and its version."""
        try:
            result = subprocess.run(
                [command, "--version"],
                capture_output=True, text=True, timeout=5, check=True, shell=(sys.platform == "win32")
            )
            version = result.stdout.strip()
            display_info(f"  ✅ {command.capitalize()} found: {version}")
        except FileNotFoundError:
            display_error(f"  ❌ {command.capitalize()} not found. This is a required dependency.")
        except subprocess.CalledProcessError:
            display_warning(f"  ⚠️  Could not determine {command} version, but it appears to be installed.")
        except Exception as e:
            self.logger.exception(f"Unexpected error checking command {command}: {e}")
            display_error(f"  ❌ An unexpected error occurred while checking for {command}: {e}")

    def check_configurations(self) -> List[str]:
        """Level 2: Check config files and compare with registry.

        Returns:
            A list of installed server lines as returned by `claude mcp list`.
        """
        display_info("LEVEL 2: Checking Configurations...")

        # Check for global config
        global_config_path = Path.home() / ".claude.json"
        if global_config_path.exists():
            display_info(f"  ✅ Found global config: {global_config_path}")
        else:
            display_info(f"  ℹ️  No global config file found at {global_config_path}.")

        # Check for local config
        local_config_path = Path(".mcp.json")
        if local_config_path.exists():
            display_info(f"  ✅ Found local config: {local_config_path}")
        else:
            display_info(f"  ℹ️  No local .mcp.json file found in the current directory.")

        # Get installed servers from `claude mcp list`
        try:
            result = subprocess.run(
                ["claude", "mcp", "list"],
                capture_output=True, text=True, timeout=10, check=True, shell=(sys.platform == "win32")
            )
            installed_servers = result.stdout.strip().splitlines()
            display_info("  ✅ `claude mcp list` output:")
            for server in installed_servers:
                display_info(f"    - {server}")
                # Check against registry
                server_name = server.split(':')[0].strip()
                if server_name in self.registry:
                    display_info(f"      - ✅ Matches official registry name: '{server_name}'")
                else:
                    display_warning(f"      - ⚠️  Server name '{server_name}' is not in the official registry.")

        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            self.logger.exception(f"Failed to run 'claude mcp list': {e}")
            display_error(f"  ❌ Failed to run `claude mcp list`. Error: {e}")
            return []  # Return empty list on failure

        # Return only the server info strings
        return installed_servers

    def test_server_liveness(self, installed_servers: List[str]) -> None:
        """Level 3: Perform a direct liveness test on each server."""
        display_info("LEVEL 3: Testing Server Liveness...")

        if not installed_servers:
            display_info("  ℹ️  No installed servers found to test.")
            return

        for server_line in installed_servers:
            server_name = "<unknown>"
            process = None
            try:
                # Basic parsing of the line, e.g., "sequential-thinking: npx @modelcontextprotocol/..."
                server_name, command_part = server_line.split(":", 1)
                server_name = server_name.strip()

                # We need the actual command to run, which is after the server name
                command_to_run = command_part.strip().split()

                display_info(f"  - Testing '{server_name}'...")

                # The JSON-RPC message to check for liveness
                init_payload = '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","clientInfo":{"name":"SuperClaudeDiagnostics","version":"1.0.0"},"capabilities":{}},"id":1}'

                # Use Popen to pipe the payload to the server's stdin
                process = subprocess.Popen(
                    command_to_run,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    shell=(sys.platform == "win32")
                )
                stdout, stderr = process.communicate(input=init_payload, timeout=15)

                if process.returncode == 0 and '"result"' in stdout:
                    display_info(f"    ✅ Liveness check PASSED for '{server_name}'.")
                else:
                    display_error(f"    ❌ Liveness check FAILED for '{server_name}'.")
                    if stderr:
                        display_error(f"       Error: {stderr.strip()}")

            except subprocess.TimeoutExpired:
                display_error(f"    ❌ Liveness check TIMED OUT for '{server_name}'. The server is unresponsive.")
                if process:
                    try:
                        process.kill()
                    except Exception:
                        pass
            except Exception as e:
                self.logger.exception(f"Unexpected error during liveness test for {server_name}: {e}")
                display_error(f"    ❌ An unexpected error occurred while testing '{server_name}': {e}")

    def check_api_keys(self) -> None:
        """Level 4: Check for API keys for relevant servers."""
        display_info("LEVEL 4: Checking for API Keys...")
        for name, info in self.registry.items():
            if "api_key_env" in info:
                env_var = info["api_key_env"]
                if os.getenv(env_var):
                    display_info(f"  ✅ API key for '{name}' ({env_var}) is set.")
                else:
                    display_warning(f"  ⚠️  API key for '{name}' ({env_var}) is NOT set. This may cause issues.")
