"""
Hooks component for Claude Code hooks integration (future-ready)
"""

from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path

from ..base.component import Component
from ..utils.localization import get_string


class HooksComponent(Component):
    """Claude Code hooks integration component"""
    
    def __init__(self, install_dir: Optional[Path] = None):
        """Initialize hooks component"""
        super().__init__(install_dir, Path("hooks"))
        
        # Define hook files to install (when hooks are ready)
        self.hook_files = [
            "pre_tool_use.py",
            "post_tool_use.py",
            "error_handler.py",
            "context_accumulator.py",
            "performance_monitor.py"
        ]
    
    def get_metadata(self) -> Dict[str, str]:
        """Get component metadata"""
        return {
            "name": "hooks",
            "version": "3.0.0",
            "description": get_string("hooks.component.description"),
            "category": "integration"
        }
    def get_metadata_modifications(self) -> Dict[str, Any]:
        # Build hooks configuration based on available files
        hook_config = {}
        for filename in self.hook_files:
            hook_path = self.install_component_subdir / filename
            if hook_path.exists():
                hook_name = filename.replace('.py', '')
                hook_config[hook_name] = [str(hook_path)]
        
        metadata_mods = {
            "components": {
                "hooks": {
                    "version": "3.0.0",
                    "installed": True,
                    "files_count": len(hook_config)
                }
            }
        }
        
        # Only add hooks configuration if we have actual hook files
        if hook_config:
            metadata_mods["hooks"] = {
                "enabled": True,
                **hook_config
            }

        
        return metadata_mods

    def _install(self, config: Dict[str, Any]) -> bool:
        """Install hooks component"""
        self.logger.info(get_string("hooks.install.installing"))

        # This component is future-ready - hooks aren't implemented yet
        source_dir = self._get_source_dir()

        if not source_dir.exists() or (source_dir / "PLACEHOLDER.py").exists  :
            self.logger.info(get_string("hooks.install.placeholder"))
            
            # Create placeholder hooks directory
            if not self.file_manager.ensure_directory(self.install_component_subdir):
                self.logger.error(get_string("hooks.install.create_dir_error", self.install_component_subdir))
                return False

            # Create placeholder file
            placeholder_content = '''"""
SuperClaude Hooks - Future Implementation

This directory is reserved for Claude Code hooks integration.
Hooks will provide lifecycle management and automation capabilities.

Planned hooks:
- pre_tool_use: Execute before tool usage
- post_tool_use: Execute after tool completion
- error_handler: Handle tool errors and recovery
- context_accumulator: Manage context across operations
- performance_monitor: Track and optimize performance

For more information, see SuperClaude documentation.
"""

# Placeholder for future hooks implementation
def placeholder_hook():
"""Placeholder hook function"""
pass
'''
            
            placeholder_path = self.install_component_subdir / "PLACEHOLDER.py"
            try:
                with open(placeholder_path, 'w') as f:
                    f.write(placeholder_content)
                self.logger.debug(get_string("hooks.install.placeholder_created"))
            except Exception as e:
                self.logger.warning(get_string("hooks.install.placeholder_error", e))
            
            # Update settings with placeholder registration
            try:
                metadata_mods = {
                    "components": {
                        "hooks": {
                            "version": "3.0.0",
                            "installed": True,
                            "status": "placeholder",
                            "files_count": 0
                        }
                    }
                }
                self.settings_manager.update_metadata(metadata_mods)
                self.logger.info(get_string("hooks.install.registration_updated"))
            except Exception as e:
                self.logger.error(get_string("hooks.install.metadata_error", e))
                return False
            
            self.logger.success(get_string("hooks.install.success_placeholder"))
            return True

        # If hooks source directory exists, install actual hooks
        self.logger.info(get_string("hooks.install.installing_actual"))

        # Validate installation
        success, errors = self.validate_prerequisites(Path("hooks"))
        if not success:
            for error in errors:
                self.logger.error(error)
            return False

        # Get files to install
        files_to_install = self.get_files_to_install()

        if not files_to_install:
            self.logger.warning(get_string("hooks.install.no_hooks_found"))
            return False

        # Copy hook files
        success_count = 0
        for source, target in files_to_install:
            self.logger.debug(get_string("hooks.install.copying", source.name, target))
            
            if self.file_manager.copy_file(source, target):
                success_count += 1
                self.logger.debug(get_string("hooks.install.copy_success", source.name))
            else:
                self.logger.error(get_string("hooks.install.copy_failed", source.name))

        if success_count != len(files_to_install):
            self.logger.error(get_string("hooks.install.copy_summary_error", success_count, len(files_to_install)))
            return False

        self.logger.success(get_string("hooks.install.success", success_count))

        return self._post_install()

    def _post_install(self):
        # Update metadata
        try:
            metadata_mods = self.get_metadata_modifications()
            self.settings_manager.update_metadata(metadata_mods)
            self.logger.info(get_string("hooks.install.metadata_updated"))

            # Add hook registration to metadata
            self.settings_manager.add_component_registration("hooks", {
                "version": "3.0.0",
                "category": "commands",
                "files_count": len(self.hook_files)
            })

            self.logger.info(get_string("commands.install.registration_updated"))
        except Exception as e:
            self.logger.error(get_string("hooks.install.metadata_error", e))
            return False

        return True
    
    def uninstall(self) -> bool:
        """Uninstall hooks component"""
        try:
            self.logger.info(get_string("hooks.uninstall.uninstalling"))
            
            # Remove hook files and placeholder
            removed_count = 0
            
            # Remove actual hook files
            for filename in self.hook_files:
                file_path = self.install_component_subdir / filename
                if self.file_manager.remove_file(file_path):
                    removed_count += 1
                    self.logger.debug(get_string("hooks.uninstall.removed", filename))
            
            # Remove placeholder file
            placeholder_path = self.install_component_subdir / "PLACEHOLDER.py"
            if self.file_manager.remove_file(placeholder_path):
                removed_count += 1
                self.logger.debug(get_string("hooks.uninstall.removed_placeholder"))
            
            # Remove hooks directory if empty
            try:
                if self.install_component_subdir.exists():
                    remaining_files = list(self.install_component_subdir.iterdir())
                    if not remaining_files:
                        self.install_component_subdir.rmdir()
                        self.logger.debug(get_string("hooks.uninstall.removed_dir"))
            except Exception as e:
                self.logger.warning(get_string("hooks.uninstall.remove_dir_error", e))
            
            # Update settings.json to remove hooks component and configuration
            try:
                if self.settings_manager.is_component_installed("hooks"):
                    self.settings_manager.remove_component_registration("hooks")
                    
                    # Also remove hooks configuration section if it exists
                    settings = self.settings_manager.load_settings()
                    if "hooks" in settings:
                        del settings["hooks"]
                        self.settings_manager.save_settings(settings)
                    
                    self.logger.info(get_string("hooks.uninstall.removed_from_settings"))
            except Exception as e:
                self.logger.warning(get_string("hooks.uninstall.settings_error", e))
            
            self.logger.success(get_string("hooks.uninstall.success", removed_count))
            return True
            
        except Exception as e:
            self.logger.exception(get_string("hooks.uninstall.unexpected_error", e))
            return False
    
    def get_dependencies(self) -> List[str]:
        """Get dependencies"""
        return ["core"]
    
    def update(self, config: Dict[str, Any]) -> bool:
        """Update hooks component"""
        try:
            self.logger.info(get_string("hooks.update.updating"))
            
            # Check current version
            current_version = self.settings_manager.get_component_version("hooks")
            target_version = self.get_metadata()["version"]
            
            if current_version == target_version:
                self.logger.info(get_string("hooks.update.already_latest", target_version))
                return True
            
            self.logger.info(get_string("hooks.update.updating_from_to", current_version, target_version))
            
            # Create backup of existing hook files
            backup_files = []
            
            if self.install_component_subdir.exists():
                for filename in self.hook_files + ["PLACEHOLDER.py"]:
                    file_path = self.install_component_subdir / filename
                    if file_path.exists():
                        backup_path = self.file_manager.backup_file(file_path)
                        if backup_path:
                            backup_files.append(backup_path)
                            self.logger.debug(get_string("hooks.update.backed_up", filename))
            
            # Perform installation (overwrites existing files)
            success = self.install(config)
            
            if success:
                # Remove backup files on successful update
                for backup_path in backup_files:
                    try:
                        backup_path.unlink()
                    except Exception:
                        pass  # Ignore cleanup errors
                
                self.logger.success(get_string("hooks.update.success", target_version))
            else:
                # Restore from backup on failure
                self.logger.warning(get_string("hooks.update.restore_failed"))
                for backup_path in backup_files:
                    try:
                        original_path = backup_path.with_suffix('')
                        backup_path.rename(original_path)
                        self.logger.debug(get_string("hooks.update.restored", original_path.name))
                    except Exception as e:
                        self.logger.error(get_string("hooks.update.restore_error", backup_path, e))
            
            return success
            
        except Exception as e:
            self.logger.exception(get_string("hooks.update.unexpected_error", e))
            return False
    
    def validate_installation(self) -> Tuple[bool, List[str]]:
        """Validate hooks component installation"""
        errors = []
        
        # Check if hooks directory exists
        if not self.install_component_subdir.exists():
            errors.append(get_string("hooks.validate.no_dir"))
            return False, errors
        
        # Check settings.json registration
        if not self.settings_manager.is_component_installed("hooks"):
            errors.append(get_string("hooks.validate.not_registered"))
        else:
            # Check version matches
            installed_version = self.settings_manager.get_component_version("hooks")
            expected_version = self.get_metadata()["version"]
            if installed_version != expected_version:
                errors.append(get_string("hooks.validate.version_mismatch", installed_version, expected_version))
        
        # Check if we have either actual hooks or placeholder
        has_placeholder = (self.install_component_subdir / "PLACEHOLDER.py").exists()
        has_actual_hooks = any((self.install_component_subdir / filename).exists() for filename in self.hook_files)
        
        if not has_placeholder and not has_actual_hooks:
            errors.append(get_string("hooks.validate.no_files"))
        
        return len(errors) == 0, errors
    
    def _get_source_dir(self) -> Path:
        """Get source directory for hook files"""
        # Assume we're in SuperClaude/setup/components/hooks.py
        # and hook files are in SuperClaude/SuperClaude/Hooks/
        project_root = Path(__file__).parent.parent.parent
        return project_root / "SuperClaude" / "Hooks"
    
    def get_size_estimate(self) -> int:
        """Get estimated installation size"""
        # Estimate based on placeholder or actual files
        source_dir = self._get_source_dir()
        total_size = 0
        
        if source_dir.exists():
            for filename in self.hook_files:
                file_path = source_dir / filename
                if file_path.exists():
                    total_size += file_path.stat().st_size
        
        # Add placeholder overhead or minimum size
        total_size = max(total_size, 10240)  # At least 10KB
        
        return total_size
    
    def get_installation_summary(self) -> Dict[str, Any]:
        """Get installation summary"""
        source_dir = self._get_source_dir()
        status = "placeholder" if not source_dir.exists() else "implemented"
        
        return {
            "component": self.get_metadata()["name"],
            "version": self.get_metadata()["version"],
            "status": status,
            "hook_files": self.hook_files if source_dir.exists() else ["PLACEHOLDER.py"],
            "estimated_size": self.get_size_estimate(),
            "install_directory": str(self.install_dir / "hooks"),
            "dependencies": self.get_dependencies()
        }
