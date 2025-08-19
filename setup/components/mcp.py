"""
MCP component for MCP server integration
"""

import subprocess
import sys
import json
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path

from ..base.component import Component
from ..utils.ui import display_info, display_warning
from ..utils.localization import get_string


class MCPComponent(Component):
    """MCP servers integration component"""
    
    def __init__(self, install_dir: Optional[Path] = None):
        """Initialize MCP component"""
        super().__init__(install_dir)
        
        # Load MCP servers from registry
        self.mcp_servers = self._load_mcp_registry()

    def _load_mcp_registry(self) -> Dict[str, Any]:
        """Load MCP server registry from JSON file"""
        try:
            # Assuming the script is run from the root of the project
            registry_path = Path("config/mcp_registry.json")
            if not registry_path.exists():
                # Fallback for when run from a different context
                # This path is relative to this file's location
                registry_path = Path(__file__).parent.parent.parent / "config/mcp_registry.json"

            with open(registry_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.error(f"Failed to load MCP registry: {e}")
            return {}
    
    def get_metadata(self) -> Dict[str, str]:
        """Get component metadata"""
        return {
            "name": "mcp",
            "version": "3.0.0",
            "description": get_string("mcp.component.description"),
            "category": "integration"
        }
    
    def validate_prerequisites(self, installSubPath: Optional[Path] = None) -> Tuple[bool, List[str]]:
        """Check prerequisites"""
        errors = []
        
        # Check if Node.js is available
        try:
            result = subprocess.run(
                ["node", "--version"], 
                capture_output=True, 
                text=True, 
                timeout=10,
                shell=(sys.platform == "win32")
            )
            if result.returncode != 0:
                errors.append(get_string("mcp.validate.no_node"))
            else:
                version = result.stdout.strip()
                self.logger.debug(get_string("mcp.validate.found_node", version))
                
                # Check version (require 18+)
                try:
                    version_num = int(version.lstrip('v').split('.')[0])
                    if version_num < 18:
                        errors.append(get_string("mcp.validate.node_version_error", version))
                except:
                    self.logger.warning(get_string("mcp.validate.parse_node_version_error", version))
        except (subprocess.TimeoutExpired, FileNotFoundError):
            errors.append(get_string("mcp.validate.no_node"))
        
        # Check if Claude CLI is available
        try:
            result = subprocess.run(
                ["claude", "--version"], 
                capture_output=True, 
                text=True, 
                timeout=10,
                shell=(sys.platform == "win32")
            )
            if result.returncode != 0:
                errors.append(get_string("mcp.validate.no_claude_cli"))
            else:
                version = result.stdout.strip()
                self.logger.debug(get_string("mcp.validate.found_claude_cli", version))
        except (subprocess.TimeoutExpired, FileNotFoundError):
            errors.append(get_string("mcp.validate.no_claude_cli"))
        
        # Check if npm is available
        try:
            result = subprocess.run(
                ["npm", "--version"], 
                capture_output=True, 
                text=True, 
                timeout=10,
                shell=(sys.platform == "win32")
            )
            if result.returncode != 0:
                errors.append(get_string("mcp.validate.no_npm"))
            else:
                version = result.stdout.strip()
                self.logger.debug(get_string("mcp.validate.found_npm", version))
        except (subprocess.TimeoutExpired, FileNotFoundError):
            errors.append(get_string("mcp.validate.no_npm"))
        
        return len(errors) == 0, errors
    
    def get_files_to_install(self) -> List[Tuple[Path, Path]]:
        """Get files to install (none for MCP component)"""
        return []
    
    def get_metadata_modifications(self) -> Dict[str, Any]:
        """Get metadata modifications for MCP component"""
        return {
            "components": {
                "mcp": {
                    "version": "3.0.0",
                    "installed": True,
                    "servers_count": len(self.mcp_servers)
                }
            },
            "mcp": {
                "enabled": True,
                "servers": list(self.mcp_servers.keys()),
                "auto_update": False
            }
        }
    
    def _check_mcp_server_installed(self, server_name: str) -> bool:
        """Check if MCP server is already installed"""
        try:
            result = subprocess.run(
                ["claude", "mcp", "list"], 
                capture_output=True, 
                text=True, 
                timeout=15,
                shell=(sys.platform == "win32")
            )
            
            if result.returncode != 0:
                self.logger.warning(get_string("mcp.status.list_error", result.stderr))
                return False
            
            # Parse output to check if server is installed
            output = result.stdout.lower()
            return server_name.lower() in output
            
        except (subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
            self.logger.warning(get_string("mcp.status.check_error", e))
            return False
    
    def _install_mcp_server(self, server_info: Dict[str, Any], config: Dict[str, Any]) -> bool:
        """Install a single MCP server"""
        server_name = server_info["name"]
        npm_package = server_info["npm_package"]
        
        command = "npx"
        
        try:
            self.logger.info(get_string("mcp.install.installing", server_name))
            
            # Check if already installed
            if self._check_mcp_server_installed(server_name):
                self.logger.info(get_string("mcp.install.already_installed", server_name))
                return True
            
            # Handle API key requirements
            if "api_key_env" in server_info:
                api_key_env = server_info["api_key_env"]
                api_key_desc = server_info.get("api_key_description", get_string("mcp.install.api_key_default_desc", server_name))
                
                if not config.get("dry_run", False):
                    display_info(get_string("mcp.install.api_key_required", server_name))
                    display_info(get_string("mcp.install.api_key_env", api_key_env))
                    display_info(get_string("mcp.install.api_key_desc", api_key_desc))
                    
                    # Check if API key is already set
                    import os
                    if not os.getenv(api_key_env):
                        display_warning(get_string("mcp.install.api_key_not_found", api_key_env))
                        self.logger.warning(get_string("mcp.install.api_key_proceeding_warning", api_key_env))
            
            # Install using Claude CLI
            if config.get("dry_run"):
                self.logger.info(get_string("mcp.install.dry_run", server_name, command, npm_package))
                return True
            
            self.logger.debug(get_string("mcp.install.running", server_name, command, npm_package))
            
            result = subprocess.run(
                ["claude", "mcp", "add", "-s", "user", "--", server_name, command, "-y", npm_package],
                capture_output=True,
                text=True,
                timeout=120,  # 2 minutes timeout for installation
                shell=(sys.platform == "win32")
            )
            
            if result.returncode == 0:
                self.logger.success(get_string("mcp.install.success", server_name))
                return True
            else:
                error_msg = result.stderr.strip() if result.stderr else "Unknown error"
                self.logger.error(get_string("mcp.install.failed", server_name, error_msg))
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error(get_string("mcp.install.timeout", server_name))
            return False
        except Exception as e:
            self.logger.error(get_string("mcp.install.error", server_name, e))
            return False
    
    def _uninstall_mcp_server(self, server_name: str) -> bool:
        """Uninstall a single MCP server"""
        try:
            self.logger.info(get_string("mcp.uninstall.uninstalling", server_name))
            
            # Check if installed
            if not self._check_mcp_server_installed(server_name):
                self.logger.info(get_string("mcp.uninstall.not_installed", server_name))
                return True
            
            self.logger.debug(get_string("mcp.uninstall.running", server_name))
            
            result = subprocess.run(
                ["claude", "mcp", "remove", server_name],
                capture_output=True,
                text=True,
                timeout=60,
                shell=(sys.platform == "win32")
            )
            
            if result.returncode == 0:
                self.logger.success(get_string("mcp.uninstall.success", server_name))
                return True
            else:
                error_msg = result.stderr.strip() if result.stderr else "Unknown error"
                self.logger.error(get_string("mcp.uninstall.failed", server_name, error_msg))
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error(get_string("mcp.uninstall.timeout", server_name))
            return False
        except Exception as e:
            self.logger.error(get_string("mcp.uninstall.error", server_name, e))
            return False
    
    def _install(self, config: Dict[str, Any]) -> bool:
        """Install MCP component"""
        self.logger.info(get_string("mcp.component.installing"))

        # Validate prerequisites
        success, errors = self.validate_prerequisites()
        if not success:
            for error in errors:
                self.logger.error(error)
            return False

        # Install each MCP server
        installed_count = 0
        failed_servers = []

        for server_name, server_info in self.mcp_servers.items():
            if self._install_mcp_server(server_info, config):
                installed_count += 1
            else:
                failed_servers.append(server_name)
                
                # Check if this is a required server
                if server_info.get("required", False):
                    self.logger.error(get_string("mcp.component.required_failed", server_name))
                    return False

        # Verify installation
        if not config.get("dry_run", False):
            self.logger.info(get_string("mcp.component.verifying"))
            try:
                result = subprocess.run(
                    ["claude", "mcp", "list"],
                    capture_output=True,
                    text=True,
                    timeout=15,
                    shell=(sys.platform == "win32")
                )
                
                if result.returncode == 0:
                    self.logger.debug(get_string("mcp.component.server_list"))
                    for line in result.stdout.strip().split('\n'):
                        if line.strip():
                            self.logger.debug(f"  {line.strip()}")
                else:
                    self.logger.warning(get_string("mcp.component.verify_error"))
                    
            except Exception as e:
                self.logger.warning(get_string("mcp.component.verify_exception", e))

        if failed_servers:
            self.logger.warning(get_string("mcp.component.some_failed", failed_servers))
            self.logger.success(get_string("mcp.component.partial_success", installed_count))
        else:
            self.logger.success(get_string("mcp.component.success", installed_count))

        return self._post_install()

    def _post_install(self) -> bool:
        # Update metadata
        try:
            metadata_mods = self.get_metadata_modifications()
            self.settings_manager.update_metadata(metadata_mods)

            # Add component registration to metadata
            self.settings_manager.add_component_registration("mcp", {
                "version": "3.0.0",
                "category": "integration",
                "servers_count": len(self.mcp_servers)
            })

            self.logger.info(get_string("mcp.component.registration_updated"))
        except Exception as e:
            self.logger.error(get_string("mcp.component.metadata_error", e))
            return False

        return True

    
    def uninstall(self) -> bool:
        """Uninstall MCP component"""
        try:
            self.logger.info(get_string("mcp.component.uninstalling"))
            
            # Uninstall each MCP server
            uninstalled_count = 0
            
            for server_name in self.mcp_servers.keys():
                if self._uninstall_mcp_server(server_name):
                    uninstalled_count += 1
            
            # Update metadata to remove MCP component
            try:
                if self.settings_manager.is_component_installed("mcp"):
                    self.settings_manager.remove_component_registration("mcp")
                    # Also remove MCP configuration from metadata
                    metadata = self.settings_manager.load_metadata()
                    if "mcp" in metadata:
                        del metadata["mcp"]
                        self.settings_manager.save_metadata(metadata)
                    self.logger.info(get_string("mcp.component.removed_from_metadata"))
            except Exception as e:
                self.logger.warning(get_string("mcp.component.metadata_error", e))
            
            self.logger.success(get_string("mcp.component.uninstall_success", uninstalled_count))
            return True
            
        except Exception as e:
            self.logger.exception(get_string("mcp.component.uninstall_error", e))
            return False
    
    def get_dependencies(self) -> List[str]:
        """Get dependencies"""
        return ["core"]
    
    def update(self, config: Dict[str, Any]) -> bool:
        """Update MCP component"""
        try:
            self.logger.info(get_string("mcp.update.updating"))
            
            # Check current version
            current_version = self.settings_manager.get_component_version("mcp")
            target_version = self.get_metadata()["version"]
            
            if current_version == target_version:
                self.logger.info(get_string("mcp.update.already_latest", target_version))
                return True
            
            self.logger.info(get_string("mcp.update.updating_from_to", current_version, target_version))
            
            # For MCP servers, update means reinstall to get latest versions
            updated_count = 0
            failed_servers = []
            
            for server_name, server_info in self.mcp_servers.items():
                try:
                    # Uninstall old version
                    if self._check_mcp_server_installed(server_name):
                        self._uninstall_mcp_server(server_name)
                    
                    # Install new version
                    if self._install_mcp_server(server_info, config):
                        updated_count += 1
                    else:
                        failed_servers.append(server_name)
                        
                except Exception as e:
                    self.logger.error(get_string("mcp.update.server_error", server_name, e))
                    failed_servers.append(server_name)
            
            # Update metadata
            try:
                # Update component version in metadata
                metadata = self.settings_manager.load_metadata()
                if "components" in metadata and "mcp" in metadata["components"]:
                    metadata["components"]["mcp"]["version"] = target_version
                    metadata["components"]["mcp"]["servers_count"] = len(self.mcp_servers)
                if "mcp" in metadata:
                    metadata["mcp"]["servers"] = list(self.mcp_servers.keys())
                self.settings_manager.save_metadata(metadata)
            except Exception as e:
                self.logger.warning(get_string("mcp.component.metadata_error", e))
            
            if failed_servers:
                self.logger.warning(get_string("mcp.update.some_failed", failed_servers))
                return False
            else:
                self.logger.success(get_string("mcp.update.success", target_version))
                return True
            
        except Exception as e:
            self.logger.exception(get_string("mcp.update.unexpected_error", e))
            return False
    
    def validate_installation(self) -> Tuple[bool, List[str]]:
        """Validate MCP component installation"""
        errors = []
        
        # Check metadata registration
        if not self.settings_manager.is_component_installed("mcp"):
            errors.append(get_string("mcp.validate.not_registered"))
            return False, errors
        
        # Check version matches
        installed_version = self.settings_manager.get_component_version("mcp")
        expected_version = self.get_metadata()["version"]
        if installed_version != expected_version:
            errors.append(get_string("mcp.validate.version_mismatch", installed_version, expected_version))
        
        # Check if Claude CLI is available
        try:
            result = subprocess.run(
                ["claude", "mcp", "list"],
                capture_output=True,
                text=True,
                timeout=15,
                shell=(sys.platform == "win32")
            )
            
            if result.returncode != 0:
                errors.append(get_string("mcp.validate.cli_error"))
            else:
                # Check if required servers are installed
                output = result.stdout.lower()
                for server_name, server_info in self.mcp_servers.items():
                    if server_info.get("required", False):
                        if server_name.lower() not in output:
                            errors.append(get_string("mcp.validate.server_not_found", server_name))
                            
        except Exception as e:
            errors.append(get_string("mcp.component.verify_exception", e))
        
        return len(errors) == 0, errors
    
    def _get_source_dir(self):
        """Get source directory for framework files"""
        return None

    def get_size_estimate(self) -> int:
        """Get estimated installation size"""
        # MCP servers are installed via npm, estimate based on typical sizes
        base_size = 50 * 1024 * 1024  # ~50MB for all servers combined
        return base_size
    
    def get_installation_summary(self) -> Dict[str, Any]:
        """Get installation summary"""
        return {
            "component": self.get_metadata()["name"],
            "version": self.get_metadata()["version"],
            "servers_count": len(self.mcp_servers),
            "mcp_servers": list(self.mcp_servers.keys()),
            "estimated_size": self.get_size_estimate(),
            "dependencies": self.get_dependencies(),
            "required_tools": ["node", "npm", "claude"]
        }
