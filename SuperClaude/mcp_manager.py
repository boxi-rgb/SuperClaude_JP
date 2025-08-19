import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, Tuple

class MCPManager:
    """Manages MCP server installations."""

    def __init__(self):
        """Initialize the MCPManager."""
        self.mcp_registry = self._load_mcp_registry()

    def _load_mcp_registry(self) -> Dict[str, Any]:
        """Load the MCP server registry from the JSON file."""
        try:
            registry_path = Path(__file__).parent.parent / "config/mcp_registry.json"
            with open(registry_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error: Could not load MCP registry. {e}")
            return {}

    def list_mcps(self):
        """List all available MCPs from the registry."""
        if not self.mcp_registry:
            print("MCP registry is empty or could not be loaded.")
            return

        print("Available MCP Servers:")
        for name, info in self.mcp_registry.items():
            description = info.get('description', 'No description')
            print(f"  - {name}: {description}")

    def _check_mcp_server_installed(self, server_name: str) -> bool:
        """Check if an MCP server is already installed via 'claude mcp list'."""
        try:
            result = subprocess.run(
                ["claude", "mcp", "list"],
                capture_output=True, text=True, timeout=15, shell=(sys.platform == "win32")
            )
            return result.returncode == 0 and server_name.lower() in result.stdout.lower()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def install_mcp(self, server_name: str) -> Tuple[bool, str]:
        """
        Installs a specific MCP server by its name.

        Args:
            server_name: The name of the MCP server to install.

        Returns:
            A tuple containing a boolean for success and a status message.
        """
        if server_name not in self.mcp_registry:
            return False, f"Error: MCP server '{server_name}' not found in registry."

        if self._check_mcp_server_installed(server_name):
            return True, f"MCP server '{server_name}' is already installed."

        server_info = self.mcp_registry[server_name]
        npm_package = server_info["npm_package"]

        print(f"Installing MCP server: {server_name}...")
        try:
            # Note: This assumes 'claude' CLI and 'npx' are in the system's PATH.
            result = subprocess.run(
                ["claude", "mcp", "add", "-s", "user", "--", server_name, "npx", "-y", npm_package],
                capture_output=True, text=True, timeout=180, shell=(sys.platform == "win32")
            )

            if result.returncode == 0:
                return True, f"Successfully installed MCP server '{server_name}'."
            else:
                error_message = result.stderr.strip() or "An unknown error occurred."
                return False, f"Failed to install MCP server '{server_name}'. Error: {error_message}"

        except subprocess.TimeoutExpired:
            return False, f"Installation of MCP server '{server_name}' timed out."
        except FileNotFoundError:
            return False, "Error: 'claude' CLI not found. Please ensure it is installed and in your PATH."
        except Exception as e:
            return False, f"An unexpected error occurred during installation: {e}"
