import subprocess
import sys
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Tuple

class MCPDiagnostics:
    """Runs a series of checks to diagnose MCP server issues."""

    def __init__(self):
        """Initialize the diagnostics tool."""
        # We can reuse the MCPManager to get the registry
        # To avoid circular imports, for now, we'll just load the registry directly.
        self.registry = self._load_mcp_registry()

    def _load_mcp_registry(self) -> Dict[str, Any]:
        """Load the MCP server registry from the JSON file."""
        try:
            registry_path = Path(__file__).parent.parent / "config/mcp_registry.json"
            with open(registry_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def run(self):
        """Run all diagnostic checks and print a report."""
        print("Starting MCP Diagnostics...")
        print("-" * 30)

        self.check_prerequisites()
        print("-" * 30)

        # This method now returns the list of installed servers for the liveness test
        installed_servers = self.check_configurations()
        print("-" * 30)

        self.test_server_liveness(installed_servers)
        print("-" * 30)

        self.check_api_keys()
        print("-" * 30)
        print("Diagnostics complete.")

    def check_prerequisites(self):
        """Level 1: Check for node, npm, and claude CLI."""
        print("LEVEL 1: Checking Prerequisites...")
        self._check_command("node")
        self._check_command("npm")
        self._check_command("claude")

    def _check_command(self, command: str):
        """Helper to check for a command and its version."""
        try:
            result = subprocess.run(
                [command, "--version"],
                capture_output=True, text=True, timeout=5, check=True, shell=(sys.platform == "win32")
            )
            version = result.stdout.strip()
            print(f"  ✅ {command.capitalize()} found: {version}")
        except FileNotFoundError:
            print(f"  ❌ {command.capitalize()} not found. This is a required dependency.")
        except subprocess.CalledProcessError:
            print(f"  ⚠️  Could not determine {command} version, but it appears to be installed.")
        except Exception as e:
            print(f"  ❌ An unexpected error occurred while checking for {command}: {e}")

    def check_configurations(self):
        """Level 2: Check config files and compare with registry."""
        print("LEVEL 2: Checking Configurations...")

        # Check for global config
        global_config_path = Path.home() / ".claude.json"
        if global_config_path.exists():
            print(f"  ✅ Found global config: {global_config_path}")
            # In a real implementation, we might want to parse and display it.
        else:
            print(f"  ℹ️  No global config file found at {global_config_path}.")

        # Check for local config
        local_config_path = Path(".mcp.json")
        if local_config_path.exists():
            print(f"  ✅ Found local config: {local_config_path}")
        else:
            print(f"  ℹ️  No local .mcp.json file found in the current directory.")

        # Get installed servers from `claude mcp list`
        try:
            result = subprocess.run(
                ["claude", "mcp", "list"],
                capture_output=True, text=True, timeout=10, check=True, shell=(sys.platform == "win32")
            )
            installed_servers = result.stdout.strip().splitlines()
            print("  ✅ `claude mcp list` output:")
            for server in installed_servers:
                print(f"    - {server}")
                # Check against registry
                server_name = server.split(':')[0].strip()
                if server_name in self.registry:
                    print(f"      - ✅ Matches official registry name: '{server_name}'")
                else:
                    print(f"      - ⚠️  Server name '{server_name}' is not in the official registry.")

        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            print(f"  ❌ Failed to run `claude mcp list`. Error: {e}")
            return [] # Return empty list on failure

        # Return only the server info strings
        return result.stdout.strip().splitlines()

    def test_server_liveness(self, installed_servers: List[str]):
        """Level 3: Perform a direct liveness test on each server."""
        print("LEVEL 3: Testing Server Liveness...")

        if not installed_servers:
            print("  ℹ️  No installed servers found to test.")
            return

        for server_line in installed_servers:
            try:
                # Basic parsing of the line, e.g., "sequential-thinking: npx @modelcontextprotocol/..."
                server_name, command_part = server_line.split(":", 1)
                server_name = server_name.strip()

                # We need the actual command to run, which is after the server name
                command_to_run = command_part.strip().split()

                print(f"  - Testing '{server_name}'...")

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
                    print(f"    ✅ Liveness check PASSED for '{server_name}'.")
                else:
                    print(f"    ❌ Liveness check FAILED for '{server_name}'.")
                    if stderr:
                        print(f"       Error: {stderr.strip()}")

            except subprocess.TimeoutExpired:
                print(f"    ❌ Liveness check TIMED OUT for '{server_name}'. The server is unresponsive.")
                process.kill()
            except Exception as e:
                print(f"    ❌ An unexpected error occurred while testing '{server_name}': {e}")


    def check_api_keys(self):
        """Level 4: Check for API keys for relevant servers."""
        print("LEVEL 4: Checking for API Keys...")
        for name, info in self.registry.items():
            if "api_key_env" in info:
                env_var = info["api_key_env"]
                if os.getenv(env_var):
                    print(f"  ✅ API key for '{name}' ({env_var}) is set.")
                else:
                    print(f"  ⚠️  API key for '{name}' ({env_var}) is NOT set. This may cause issues.")
