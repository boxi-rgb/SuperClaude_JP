"""
Commands component for SuperClaude slash command definitions
"""

from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path

from ..base.component import Component
from ..utils.localization import get_string

class CommandsComponent(Component):
    """SuperClaude slash commands component"""
    
    def __init__(self, install_dir: Optional[Path] = None):
        """Initialize commands component"""
        super().__init__(install_dir, Path("commands/sc"))
    
    def get_metadata(self) -> Dict[str, str]:
        """Get component metadata"""
        return {
            "name": "commands",
            "version": "3.0.0",
            "description": get_string("commands.component.description"),
            "category": "commands"
        }
    
    def get_metadata_modifications(self) -> Dict[str, Any]:
        """Get metadata modifications for commands component"""
        return {
            "components": {
                "commands": {
                    "version": "3.0.0",
                    "installed": True,
                    "files_count": len(self.component_files)
                }
            },
            "commands": {
                "enabled": True,
                "version": "3.0.0",
                "auto_update": False
            }
        }
    
    def _install(self, config: Dict[str, Any]) -> bool:
        """Install commands component"""
        self.logger.info(get_string("commands.install.installing"))

        # Check for and migrate existing commands from old location
        self._migrate_existing_commands()

        return super()._install(config);

    def _post_install(self):
        # Update metadata
        try:
            metadata_mods = self.get_metadata_modifications()
            self.settings_manager.update_metadata(metadata_mods)
            self.logger.info(get_string("commands.install.metadata_updated"))

            # Add component registration to metadata
            self.settings_manager.add_component_registration("commands", {
                "version": "3.0.0",
                "category": "commands",
                "files_count": len(self.component_files)
            })
            self.logger.info(get_string("commands.install.registration_updated"))
        except Exception as e:
            self.logger.error(get_string("commands.install.metadata_error", e))
            return False

        return True
    
    def uninstall(self) -> bool:
        """Uninstall commands component"""
        try:
            self.logger.info(get_string("commands.uninstall.uninstalling"))
            
            # Remove command files from sc subdirectory
            commands_dir = self.install_dir / "commands" / "sc"
            removed_count = 0
            
            for filename in self.component_files:
                file_path = commands_dir / filename
                if self.file_manager.remove_file(file_path):
                    removed_count += 1
                    self.logger.debug(get_string("commands.uninstall.removed", filename))
                else:
                    self.logger.warning(get_string("commands.uninstall.remove_error", filename))
            
            # Also check and remove any old commands in root commands directory
            old_commands_dir = self.install_dir / "commands"
            old_removed_count = 0
            
            for filename in self.component_files:
                old_file_path = old_commands_dir / filename
                if old_file_path.exists() and old_file_path.is_file():
                    if self.file_manager.remove_file(old_file_path):
                        old_removed_count += 1
                        self.logger.debug(get_string("commands.uninstall.removed_old", filename))
                    else:
                        self.logger.warning(get_string("commands.uninstall.remove_old_error", filename))
            
            if old_removed_count > 0:
                self.logger.info(get_string("commands.uninstall.also_removed_old", old_removed_count))
            
            removed_count += old_removed_count
            
            # Remove sc subdirectory if empty
            try:
                if commands_dir.exists():
                    remaining_files = list(commands_dir.iterdir())
                    if not remaining_files:
                        commands_dir.rmdir()
                        self.logger.debug(get_string("commands.uninstall.removed_sc_dir"))
                        
                        # Also remove parent commands directory if empty
                        parent_commands_dir = self.install_dir / "commands"
                        if parent_commands_dir.exists():
                            remaining_files = list(parent_commands_dir.iterdir())
                            if not remaining_files:
                                parent_commands_dir.rmdir()
                                self.logger.debug(get_string("commands.uninstall.removed_parent_dir"))
            except Exception as e:
                self.logger.warning(get_string("commands.uninstall.remove_dir_error", e))
            
            # Update metadata to remove commands component
            try:
                if self.settings_manager.is_component_installed("commands"):
                    self.settings_manager.remove_component_registration("commands")
                    # Also remove commands configuration from metadata
                    metadata = self.settings_manager.load_metadata()
                    if "commands" in metadata:
                        del metadata["commands"]
                        self.settings_manager.save_metadata(metadata)
                    self.logger.info(get_string("commands.uninstall.removed_from_metadata"))
            except Exception as e:
                self.logger.warning(get_string("commands.uninstall.metadata_error", e))
            
            self.logger.success(get_string("commands.uninstall.success", removed_count))
            return True
            
        except Exception as e:
            self.logger.exception(get_string("commands.uninstall.unexpected_error", e))
            return False
    
    def get_dependencies(self) -> List[str]:
        """Get dependencies"""
        return ["core"]
    
    def update(self, config: Dict[str, Any]) -> bool:
        """Update commands component"""
        try:
            self.logger.info(get_string("commands.update.updating"))
            
            # Check current version
            current_version = self.settings_manager.get_component_version("commands")
            target_version = self.get_metadata()["version"]
            
            if current_version == target_version:
                self.logger.info(get_string("commands.update.already_latest", target_version))
                return True
            
            self.logger.info(get_string("commands.update.updating_from_to", current_version, target_version))
            
            # Create backup of existing command files
            commands_dir = self.install_dir / "commands" / "sc"
            backup_files = []
            
            if commands_dir.exists():
                for filename in self.component_files:
                    file_path = commands_dir / filename
                    if file_path.exists():
                        backup_path = self.file_manager.backup_file(file_path)
                        if backup_path:
                            backup_files.append(backup_path)
                            self.logger.debug(get_string("commands.update.backed_up", filename))
            
            # Perform installation (overwrites existing files)
            success = self.install(config)
            
            if success:
                # Remove backup files on successful update
                for backup_path in backup_files:
                    try:
                        backup_path.unlink()
                    except Exception:
                        pass  # Ignore cleanup errors
                
                self.logger.success(get_string("commands.update.success", target_version))
            else:
                # Restore from backup on failure
                self.logger.warning(get_string("commands.update.restore_failed"))
                for backup_path in backup_files:
                    try:
                        original_path = backup_path.with_suffix('')
                        backup_path.rename(original_path)
                        self.logger.debug(get_string("commands.update.restored", original_path.name))
                    except Exception as e:
                        self.logger.error(get_string("commands.update.restore_error", backup_path, e))
            
            return success
            
        except Exception as e:
            self.logger.exception(get_string("commands.update.unexpected_error", e))
            return False
    
    def validate_installation(self) -> Tuple[bool, List[str]]:
        """Validate commands component installation"""
        errors = []
        
        # Check if sc commands directory exists
        commands_dir = self.install_dir / "commands" / "sc"
        if not commands_dir.exists():
            errors.append(get_string("commands.validate.no_sc_dir"))
            return False, errors
        
        # Check if all command files exist
        for filename in self.component_files:
            file_path = commands_dir / filename
            if not file_path.exists():
                errors.append(get_string("commands.validate.missing_file", filename))
            elif not file_path.is_file():
                errors.append(get_string("commands.validate.not_a_file", filename))
        
        # Check metadata registration
        if not self.settings_manager.is_component_installed("commands"):
            errors.append(get_string("commands.validate.not_registered"))
        else:
            # Check version matches
            installed_version = self.settings_manager.get_component_version("commands")
            expected_version = self.get_metadata()["version"]
            if installed_version != expected_version:
                errors.append(get_string("commands.validate.version_mismatch", installed_version, expected_version))
        
        return len(errors) == 0, errors
    
    def _get_source_dir(self) -> Path:
        """Get source directory for command files"""
        # Assume we're in SuperClaude/setup/components/commands.py
        # and command files are in SuperClaude/SuperClaude/Commands/
        project_root = Path(__file__).parent.parent.parent
        return project_root / "SuperClaude" / "Commands"
    
    def get_size_estimate(self) -> int:
        """Get estimated installation size"""
        total_size = 0
        source_dir = self._get_source_dir()
        
        for filename in self.component_files:
            file_path = source_dir / filename
            if file_path.exists():
                total_size += file_path.stat().st_size
        
        # Add overhead for directory and settings
        total_size += 5120  # ~5KB overhead
        
        return total_size
    
    def get_installation_summary(self) -> Dict[str, Any]:
        """Get installation summary"""
        return {
            "component": self.get_metadata()["name"],
            "version": self.get_metadata()["version"],
            "files_installed": len(self.component_files),
            "command_files": self.component_files,
            "estimated_size": self.get_size_estimate(),
            "install_directory": str(self.install_dir / "commands" / "sc"),
            "dependencies": self.get_dependencies()
        }
    
    def _migrate_existing_commands(self) -> None:
        """Migrate existing commands from old location to new sc subdirectory"""
        try:
            old_commands_dir = self.install_dir / "commands"
            new_commands_dir = self.install_dir / "commands" / "sc"
            
            # Check if old commands exist in root commands directory
            migrated_count = 0
            commands_to_migrate = []
            
            if old_commands_dir.exists():
                for filename in self.component_files:
                    old_file_path = old_commands_dir / filename
                    if old_file_path.exists() and old_file_path.is_file():
                        commands_to_migrate.append(filename)
            
            if commands_to_migrate:
                self.logger.info(get_string("commands.migrate.found_commands", len(commands_to_migrate)))
                
                # Ensure new directory exists
                if not self.file_manager.ensure_directory(new_commands_dir):
                    self.logger.error(get_string("commands.migrate.create_dir_error", new_commands_dir))
                    return
                
                # Move files from old to new location
                for filename in commands_to_migrate:
                    old_file_path = old_commands_dir / filename
                    new_file_path = new_commands_dir / filename
                    
                    try:
                        # Copy file to new location
                        if self.file_manager.copy_file(old_file_path, new_file_path):
                            # Remove old file
                            if self.file_manager.remove_file(old_file_path):
                                migrated_count += 1
                                self.logger.debug(get_string("commands.migrate.migrated", filename))
                            else:
                                self.logger.warning(get_string("commands.uninstall.remove_old_error", filename))
                        else:
                            self.logger.warning(get_string("commands.migrate.copy_error", filename))
                    except Exception as e:
                        self.logger.warning(get_string("commands.migrate.error", filename, e))
                
                if migrated_count > 0:
                    self.logger.success(get_string("commands.migrate.success", migrated_count))
                    self.logger.info(get_string("commands.migrate.info"))
                    
                    # Try to remove old commands directory if empty
                    try:
                        if old_commands_dir.exists():
                            remaining_files = [f for f in old_commands_dir.iterdir() if f.is_file()]
                            if not remaining_files:
                                # Only remove if no user files remain
                                old_commands_dir.rmdir()
                                self.logger.debug(get_string("commands.migrate.remove_old_dir_error", old_commands_dir))
                    except Exception as e:
                        self.logger.debug(get_string("commands.migrate.remove_old_dir_error", e))
                        
        except Exception as e:
            self.logger.warning(get_string("commands.migrate.migration_error", e))
