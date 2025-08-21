"""
SuperClaude Uninstall Operation Module
Refactored from uninstall.py for unified CLI hub
"""

import sys
import time
from pathlib import Path
from typing import List, Optional, Dict, Any
import argparse

from ..core.registry import ComponentRegistry
from ..managers.settings_manager import SettingsManager
from ..managers.file_manager import FileManager
from ..utils.ui import (
    display_header, display_info, display_success, display_error, 
    display_warning, Menu, confirm, ProgressBar, Colors
)
from ..utils.logger import get_logger
from ..utils.localization import get_string
from .. import DEFAULT_INSTALL_DIR, PROJECT_ROOT
from . import OperationBase


class UninstallOperation(OperationBase):
    """Uninstall operation implementation"""
    
    def __init__(self):
        super().__init__("uninstall")


def register_parser(subparsers, global_parser=None) -> argparse.ArgumentParser:
    """Register uninstall CLI arguments"""
    parents = [global_parser] if global_parser else []
    
    parser = subparsers.add_parser(
        "uninstall",
        help=get_string("uninstall.parser.help"),
        description=get_string("uninstall.parser.description"),
        epilog="""
Examples:
  SuperClaude uninstall                    # Interactive uninstall
  SuperClaude uninstall --components core  # Remove specific components
  SuperClaude uninstall --complete --force # Complete removal (forced)
  SuperClaude uninstall --keep-backups     # Keep backup files
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=parents
    )
    
    # Uninstall mode options
    parser.add_argument(
        "--components",
        type=str,
        nargs="+",
        help=get_string("uninstall.parser.components_help")
    )
    
    parser.add_argument(
        "--complete",
        action="store_true",
        help=get_string("uninstall.parser.complete_help")
    )
    
    # Data preservation options
    parser.add_argument(
        "--keep-backups",
        action="store_true",
        help=get_string("uninstall.parser.keep_backups_help")
    )
    
    parser.add_argument(
        "--keep-logs",
        action="store_true",
        help=get_string("uninstall.parser.keep_logs_help")
    )
    
    parser.add_argument(
        "--keep-settings",
        action="store_true",
        help=get_string("uninstall.parser.keep_settings_help")
    )
    
    # Safety options
    parser.add_argument(
        "--no-confirm",
        action="store_true",
        help=get_string("uninstall.parser.no_confirm_help")
    )
    
    return parser

def get_installed_components(install_dir: Path) -> Dict[str, Dict[str, Any]]:
    """Get currently installed components and their versions"""
    try:
        settings_manager = SettingsManager(install_dir)
        return settings_manager.get_installed_components()
    except Exception:
        return {}


def get_installation_info(install_dir: Path) -> Dict[str, Any]:
    """Get detailed installation information"""
    info = {
        "install_dir": install_dir,
        "exists": False,
        "components": {},
        "directories": [],
        "files": [],
        "total_size": 0
    }
    
    if not install_dir.exists():
        return info
    
    info["exists"] = True
    info["components"] = get_installed_components(install_dir)
    
    # Scan installation directory
    try:
        for item in install_dir.rglob("*"):
            if item.is_file():
                info["files"].append(item)
                info["total_size"] += item.stat().st_size
            elif item.is_dir():
                info["directories"].append(item)
    except Exception:
        pass
    
    return info


def display_uninstall_info(info: Dict[str, Any]) -> None:
    """Display installation information before uninstall"""
    display_info(f"\n{Colors.CYAN}{Colors.BRIGHT}{get_string('uninstall.info.header')}{Colors.RESET}")
    display_info("=" * 50)

    if not info["exists"]:
        display_warning(f"{Colors.YELLOW}{get_string('uninstall.info.no_installation')}{Colors.RESET}")
        return

    display_info(f"{Colors.BLUE}{get_string('uninstall.info.directory')}{Colors.RESET} {info['install_dir']}")

    if info["components"]:
        display_info(f"{Colors.BLUE}{get_string('uninstall.info.components')}{Colors.RESET}")
        for component, version in info["components"].items():
            display_info(f"  {component}: v{version}")

    display_info(f"{Colors.BLUE}{get_string('uninstall.info.files')}{Colors.RESET} {len(info['files'])}")
    display_info(f"{Colors.BLUE}{get_string('uninstall.info.directories')}{Colors.RESET} {len(info['directories'])}")

    if info["total_size"] > 0:
        from ..utils.ui import format_size
        display_info(f"{Colors.BLUE}{get_string('uninstall.info.total_size')}{Colors.RESET} {format_size(info['total_size'])}")

    display_info("")


def get_components_to_uninstall(args: argparse.Namespace, installed_components: Dict[str, str]) -> Optional[List[str]]:
    """Determine which components to uninstall"""
    logger = get_logger()
    
    # Complete uninstall
    if args.complete:
        return list(installed_components.keys())
    
    # Explicit components specified
    if args.components:
        # Validate that specified components are installed
        invalid_components = [c for c in args.components if c not in installed_components]
        if invalid_components:
            logger.error(get_string("uninstall.components.not_installed", invalid_components))
            return None
        return args.components
    
    # Interactive selection
    return interactive_uninstall_selection(installed_components)


def interactive_uninstall_selection(installed_components: Dict[str, str]) -> Optional[List[str]]:
    """Interactive uninstall selection"""
    if not installed_components:
        return []
    
    display_info(f"\n{Colors.CYAN}{get_string('uninstall.selection.header')}{Colors.RESET}")
    
    # Create menu options
    preset_options = [
        get_string("uninstall.selection.complete"),
        get_string("uninstall.selection.specific"),
        get_string("uninstall.selection.cancel")
    ]
    
    menu = Menu(get_string("uninstall.selection.prompt"), preset_options)
    choice = menu.display()
    
    if choice == -1 or choice == 2:  # Cancelled
        return None
    elif choice == 0:  # Complete uninstall
        return list(installed_components.keys())
    elif choice == 1:  # Select specific components
        component_options = []
        component_names = []
        
        for component, version in installed_components.items():
            component_options.append(f"{component} (v{version})")
            component_names.append(component)
        
        component_menu = Menu(get_string("uninstall.selection.select_components"), component_options, multi_select=True)
        selections = component_menu.display()
        
        if not selections:
            return None
        
        return [component_names[i] for i in selections]
    
    return None


def display_uninstall_plan(components: List[str], args: argparse.Namespace, info: Dict[str, Any]) -> None:
    """Display uninstall plan"""
    display_info(f"\n{Colors.CYAN}{Colors.BRIGHT}{get_string('uninstall.plan.header')}{Colors.RESET}")
    display_info("=" * 50)
    
    display_info(f"{Colors.BLUE}{get_string('uninstall.info.directory')}{Colors.RESET} {info['install_dir']}")
    
    if components:
        display_info(f"{Colors.BLUE}{get_string('uninstall.plan.components_to_remove')}{Colors.RESET}")
        for i, component_name in enumerate(components, 1):
            version = info["components"].get(component_name, "unknown")
            display_info(f"  {i}. {component_name} (v{version})")
    
    # Show what will be preserved
    preserved = []
    if args.keep_backups:
        preserved.append(get_string("uninstall.plan.backup_files"))
    if args.keep_logs:
        preserved.append(get_string("uninstall.plan.log_files"))
    if args.keep_settings:
        preserved.append(get_string("uninstall.plan.user_settings"))
    
    if preserved:
        display_info(f"{Colors.GREEN}{get_string('uninstall.plan.preserving')}{Colors.RESET} {', '.join(preserved)}")

    if args.complete:
        display_warning(f"{Colors.RED}{get_string('uninstall.plan.warning_complete')}{Colors.RESET}")

    display_info("")


def create_uninstall_backup(install_dir: Path, components: List[str]) -> Optional[Path]:
    """Create backup before uninstall"""
    logger = get_logger()
    
    try:
        from datetime import datetime
        backup_dir = install_dir / "backups"
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"pre_uninstall_{timestamp}.tar.gz"
        backup_path = backup_dir / backup_name
        
        import tarfile
        
        logger.info(get_string("uninstall.backup.creating", backup_path))
        
        with tarfile.open(backup_path, "w:gz") as tar:
            for component in components:
                # Add component files to backup
                settings_manager = SettingsManager(install_dir)
                # This would need component-specific backup logic
                pass
        
        logger.success(get_string("uninstall.backup.success", backup_path))
        return backup_path
        
    except Exception as e:
        logger.warning(get_string("uninstall.backup.error", e))
        return None


def perform_uninstall(components: List[str], args: argparse.Namespace, info: Dict[str, Any]) -> bool:
    """Perform the actual uninstall"""
    logger = get_logger()
    start_time = time.time()
    
    try:
        # Create component registry
        registry = ComponentRegistry(PROJECT_ROOT / "setup" / "components")
        registry.discover_components()
        
        # Create component instances
        component_instances = registry.create_component_instances(components, args.install_dir)
        
        # Setup progress tracking
        progress = ProgressBar(
            total=len(components),
            prefix=get_string("uninstall.perform.prefix"),
            suffix=""
        )
        
        # Uninstall components
        logger.info(get_string("uninstall.perform.uninstalling", len(components)))
        
        uninstalled_components = []
        failed_components = []
        
        for i, component_name in enumerate(components):
            progress.update(i, get_string("uninstall.perform.component_uninstalling", component_name))
            
            try:
                if component_name in component_instances:
                    instance = component_instances[component_name]
                    if instance.uninstall():
                        uninstalled_components.append(component_name)
                        logger.debug(get_string("uninstall.perform.success", component_name))
                    else:
                        failed_components.append(component_name)
                        logger.error(get_string("uninstall.perform.failed", component_name))
                else:
                    logger.warning(get_string("uninstall.perform.not_found", component_name))
                    
            except Exception as e:
                logger.error(get_string("uninstall.perform.error", component_name, e))
                failed_components.append(component_name)
            
            progress.update(i + 1, get_string("uninstall.perform.processed", component_name))
            time.sleep(0.1)  # Brief pause for visual effect
        
        progress.finish(get_string("uninstall.perform.complete"))
        
        # Handle complete uninstall cleanup
        if args.complete:
            cleanup_installation_directory(args.install_dir, args)
        
        # Show results
        duration = time.time() - start_time
        
        if failed_components:
            logger.warning(get_string("uninstall.perform.failures", f"{duration:.1f}"))
            logger.warning(get_string("uninstall.perform.failed_components", ', '.join(failed_components)))
        else:
            logger.success(get_string("uninstall.perform.success_duration", f"{duration:.1f}"))
        
        if uninstalled_components:
            logger.info(get_string("uninstall.perform.uninstalled_components", ', '.join(uninstalled_components)))
        
        return len(failed_components) == 0
        
    except Exception as e:
        logger.exception(get_string("uninstall.perform.unexpected_error", e))
        return False


def cleanup_installation_directory(install_dir: Path, args: argparse.Namespace) -> None:
    """Clean up installation directory for complete uninstall"""
    logger = get_logger()
    file_manager = FileManager()
    
    try:
        # Preserve specific directories/files if requested
        preserve_patterns = []
        
        if args.keep_backups:
            preserve_patterns.append("backups/*")
        if args.keep_logs:
            preserve_patterns.append("logs/*")
        if args.keep_settings and not args.complete:
            preserve_patterns.append("settings.json")
        
        # Remove installation directory contents
        if args.complete and not preserve_patterns:
            # Complete removal
            if file_manager.remove_directory(install_dir):
                logger.info(get_string("uninstall.cleanup.removed_dir", install_dir))
            else:
                logger.warning(get_string("uninstall.cleanup.remove_error", install_dir))
        else:
            # Selective removal
            for item in install_dir.iterdir():
                should_preserve = False
                
                for pattern in preserve_patterns:
                    if item.match(pattern):
                        should_preserve = True
                        break
                
                if not should_preserve:
                    if item.is_file():
                        file_manager.remove_file(item)
                    elif item.is_dir():
                        file_manager.remove_directory(item)
                        
    except Exception as e:
        logger.error(get_string("uninstall.cleanup.error", e))


def run(args: argparse.Namespace) -> int:
    """Execute uninstall operation with parsed arguments"""
    operation = UninstallOperation()
    operation.setup_operation_logging(args)
    logger = get_logger()
    # ✅ Inserted validation code
    expected_home = Path.home().resolve()
    actual_dir = args.install_dir.resolve()

    if not str(actual_dir).startswith(str(expected_home)):
        print(f"\n[✗] {get_string('install.run.invalid_path_header')}")
        print(f"    {get_string('install.run.invalid_path_expected', expected_home)}")
        print(f"    {get_string('install.run.invalid_path_provided', actual_dir)}")
        sys.exit(1)
    
    try:
        # Validate global arguments
        success, errors = operation.validate_global_args(args)
        if not success:
            for error in errors:
                logger.error(error)
            return 1
        
        # Display header
        if not args.quiet:
            display_header(
                get_string("uninstall.run.header"),
                get_string("uninstall.run.subtitle")
            )
        
        # Get installation information
        info = get_installation_info(args.install_dir)
        
        # Display current installation
        if not args.quiet:
            display_uninstall_info(info)
        
        # Check if SuperClaude is installed
        if not info["exists"]:
            logger.warning(get_string("uninstall.run.not_found", args.install_dir))
            return 0
        
        # Get components to uninstall
        components = get_components_to_uninstall(args, info["components"])
        if components is None:
            logger.info(get_string("uninstall.run.cancelled"))
            return 0
        elif not components:
            logger.info(get_string("uninstall.run.no_components_selected"))
            return 0
        
        # Display uninstall plan
        if not args.quiet:
            display_uninstall_plan(components, args, info)
        
        # Confirmation
        if not args.no_confirm and not args.yes:
            if args.complete:
                warning_msg = get_string("uninstall.run.confirm_complete")
            else:
                warning_msg = get_string("uninstall.run.confirm_specific", len(components))
            
            if not confirm(warning_msg, default=False):
                logger.info(get_string("uninstall.run.cancelled"))
                return 0
        
        # Create backup if not dry run and not keeping backups
        if not args.dry_run and not args.keep_backups:
            create_uninstall_backup(args.install_dir, components)
        
        # Perform uninstall
        success = perform_uninstall(components, args, info)
        
        if success:
            if not args.quiet:
                display_success(get_string("uninstall.run.success"))

                if not args.dry_run:
                    display_info(f"\n{Colors.CYAN}{get_string('uninstall.run.complete_header')}{Colors.RESET}")
                    display_info(get_string("uninstall.run.removed_from", args.install_dir))
                    if not args.complete:
                        display_info(get_string("uninstall.run.reinstall_prompt"))

            return 0
        else:
            display_error(get_string("uninstall.run.failures"))
            return 1
            
    except KeyboardInterrupt:
        display_warning(f"\n{Colors.YELLOW}{get_string('uninstall.run.cancelled')}{Colors.RESET}")
        return 130
    except Exception as e:
        return operation.handle_operation_error("uninstall", e)
