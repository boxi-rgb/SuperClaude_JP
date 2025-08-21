import json
import subprocess
import sys
import os
import logging
from pathlib import Path
from typing import Dict, Any, Tuple, Optional


class MCPManager:
    """Manages MCP server installations."""

    def __init__(self, registry_path: str = None):
        """Initialize the MCPManager."""
        self.logger = logging.getLogger("SuperClaude.MCPManager")
        self.mcp_registry = self._load_mcp_registry(registry_path)

    def _load_mcp_registry(self, registry_path: Optional[str] = None) -> Dict[str, Any]:
        """Load the MCP server registry from the JSON file."""
        # 環境変数でパス指定可能
        if not registry_path:
            registry_path = os.environ.get("SUPERCLAUDE_MCP_REGISTRY", str(Path(__file__).parent.parent / "config/mcp_registry.json"))
        try:
            with open(registry_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.error(f"Could not load MCP registry: {e}")
            return {}

    def list_mcps(self) -> None:
        """List all available MCPs from the registry."""
        if not self.mcp_registry:
            self.logger.warning("MCP registry is empty or could not be loaded.")
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
        except subprocess.TimeoutExpired:
            self.logger.error("Timeout expired while checking MCP server installation.")
            return False
        except FileNotFoundError:
            self.logger.error("'claude' CLI not found while checking MCP server installation.")
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
            self.logger.error(f"MCP server '{server_name}' not found in registry.")
            return False, f"Error: MCP server '{server_name}' not found in registry."

        if self._check_mcp_server_installed(server_name):
            self.logger.info(f"MCP server '{server_name}' is already installed.")
            return True, f"MCP server '{server_name}' is already installed."

        server_info = self.mcp_registry[server_name]
        npm_package = server_info.get("npm_package")
        if not npm_package:
            self.logger.error(f"MCP registry entry for '{server_name}' missing 'npm_package'.")
            return False, f"Error: MCP server '{server_name}' has no npm_package specified in registry."

        print(f"Installing MCP server: {server_name}...")
        try:
            # Note: This assumes 'claude' CLI and 'npx' are in the system's PATH.
            cmd = ["claude", "mcp", "add", "-s", "user", "--", server_name, "npx", "-y", npm_package]
            result = subprocess.run(
                cmd,
                capture_output=True, text=True, timeout=180, shell=(sys.platform == "win32")
            )

            if result.returncode == 0:
                self.logger.info(f"Successfully installed MCP server '{server_name}'.")
                return True, f"Successfully installed MCP server '{server_name}'."
            else:
                error_message = result.stderr.strip() or "An unknown error occurred."
                self.logger.error(f"Failed to install MCP server '{server_name}': {error_message}")
                return False, f"Failed to install MCP server '{server_name}'. Error: {error_message}"

        except subprocess.TimeoutExpired:
            self.logger.error(f"Installation of MCP server '{server_name}' timed out.")
            return False, f"Installation of MCP server '{server_name}' timed out."
        except FileNotFoundError:
            self.logger.error("'claude' CLI not found. Please ensure it is installed and in your PATH.")
            return False, "Error: 'claude' CLI not found. Please ensure it is installed and in your PATH."
        except Exception as e:
            self.logger.exception(f"An unexpected error occurred during installation: {e}")
            return False, f"An unexpected error occurred during installation: {e}"
