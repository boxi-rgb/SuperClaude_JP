"""
SuperClaude Update Operation Module
Refactored from update.py for unified CLI hub
"""

import sys
import time
from pathlib import Path
from typing import List, Optional, Dict, Any
import argparse

from ..base.installer import Installer
from ..core.registry import ComponentRegistry
from ..managers.settings_manager import SettingsManager
from ..core.validator import Validator
from ..utils.ui import (
    display_header, display_info, display_success, display_error, 
    display_warning, Menu, confirm, ProgressBar, Colors, format_size
)
from ..utils.logger import get_logger
from ..utils.localization import get_string
from .. import DEFAULT_INSTALL_DIR, PROJECT_ROOT
from . import OperationBase


class UpdateOperation(OperationBase):
    """Update operation implementation"""
    
    def __init__(self):
        super().__init__("update")


def register_parser(subparsers, global_parser=None) -> argparse.ArgumentParser:
    """Register update CLI arguments"""
    parents = [global_parser] if global_parser else []
    
    parser = subparsers.add_parser(
        "update",
        help=get_string("update.parser.help"),
        description=get_string("update.parser.description"),
        epilog="""
Examples:
  SuperClaude update                       # Interactive update
  SuperClaude update --check --verbose     # Check for updates (verbose)
  SuperClaude update --components core mcp # Update specific components
  SuperClaude update --backup --force      # Create backup before update (forced)
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=parents
    )
    
    # Update mode options
    parser.add_argument(
        "--check",
        action="store_true",
        help=get_string("update.parser.check_help")
    )
    
    parser.add_argument(
        "--components",
        type=str,
        nargs="+",
        help=get_string("update.parser.components_help")
    )
    
    # Backup options
    parser.add_argument(
        "--backup",
        action="store_true",
        help=get_string("update.parser.backup_help")
    )
    
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help=get_string("update.parser.no_backup_help")
    )
    
    # Update options
    parser.add_argument(
        "--reinstall",
        action="store_true",
        help=get_string("update.parser.reinstall_help")
    )
    
    return parser

def check_installation_exists(install_dir: Path) -> bool:
    """Check if SuperClaude installation exists"""
    settings_manager = SettingsManager(install_dir)

    return settings_manager.check_installation_exists()

def get_installed_components(install_dir: Path) -> Dict[str, Dict[str, Any]]:
    """Get currently installed components and their versions"""
    try:
        settings_manager = SettingsManager(install_dir)
        return settings_manager.get_installed_components()
    except Exception:
        return {}


def get_available_updates(installed_components: Dict[str, str], registry: ComponentRegistry) -> Dict[str, Dict[str, str]]:
    """Check for available updates"""
    updates = {}
    
    for component_name, current_version in installed_components.items():
        try:
            metadata = registry.get_component_metadata(component_name)
            if metadata:
                available_version = metadata.get("version", "unknown")
                if available_version != current_version:
                    updates[component_name] = {
                        "current": current_version,
                        "available": available_version,
                        "description": metadata.get("description", "No description")
                    }
        except Exception:
            continue
    
    return updates


def display_update_check(installed_components: Dict[str, str], available_updates: Dict[str, Dict[str, str]]) -> None:
    """Display update check results"""
    print(f"\n{Colors.CYAN}{Colors.BRIGHT}{get_string('update.check.results_header')}{Colors.RESET}")
    print("=" * 50)
    
    if not installed_components:
        print(f"{Colors.YELLOW}{get_string('update.check.no_installation')}{Colors.RESET}")
        return
    
    print(f"{Colors.BLUE}{get_string('update.check.installed_components')}{Colors.RESET}")
    for component, version in installed_components.items():
        print(f"  {component}: v{version}")
    
    if available_updates:
        print(f"\n{Colors.GREEN}{get_string('update.check.available_updates')}{Colors.RESET}")
        for component, info in available_updates.items():
            print(f"  {component}: v{info['current']} → v{info['available']}")
            print(f"    {info['description']}")
    else:
        print(f"\n{Colors.GREEN}{get_string('update.check.all_up_to_date')}{Colors.RESET}")
    
    print()


def get_components_to_update(args: argparse.Namespace, installed_components: Dict[str, str], 
                           available_updates: Dict[str, Dict[str, str]]) -> Optional[List[str]]:
    """Determine which components to update"""
    logger = get_logger()
    
    # Explicit components specified
    if args.components:
        # Validate that specified components are installed
        invalid_components = [c for c in args.components if c not in installed_components]
        if invalid_components:
            logger.error(get_string("update.components.not_installed", invalid_components))
            return None
        return args.components
    
    # If no updates available and not forcing reinstall
    if not available_updates and not args.reinstall:
        logger.info(get_string("update.components.no_updates_available"))
        return []
    
    # Interactive selection
    if available_updates:
        return interactive_update_selection(available_updates, installed_components)
    elif args.reinstall:
        # Reinstall all components
        return list(installed_components.keys())
    
    return []


def interactive_update_selection(available_updates: Dict[str, Dict[str, str]], 
                                installed_components: Dict[str, str]) -> Optional[List[str]]:
    """Interactive update selection"""
    if not available_updates:
        return []
    
    print(f"\n{Colors.CYAN}{get_string('update.selection.header')}{Colors.RESET}")
    
    # Create menu options
    update_options = []
    component_names = []
    
    for component, info in available_updates.items():
        update_options.append(f"{component}: v{info['current']} → v{info['available']}")
        component_names.append(component)
    
    # Add bulk options
    preset_options = [
        get_string("update.selection.update_all"),
        get_string("update.selection.select_individual"),
        get_string("update.selection.cancel")
    ]
    
    menu = Menu(get_string("update.selection.prompt"), preset_options)
    choice = menu.display()
    
    if choice == -1 or choice == 2:  # Cancelled
        return None
    elif choice == 0:  # Update all
        return component_names
    elif choice == 1:  # Select individual
        component_menu = Menu(get_string("update.selection.select_components"), update_options, multi_select=True)
        selections = component_menu.display()
        
        if not selections:
            return None
        
        return [component_names[i] for i in selections]
    
    return None


def display_update_plan(components: List[str], available_updates: Dict[str, Dict[str, str]], 
                       installed_components: Dict[str, str], install_dir: Path) -> None:
    """Display update plan"""
    print(f"\n{Colors.CYAN}{Colors.BRIGHT}{get_string('update.plan.header')}{Colors.RESET}")
    print("=" * 50)
    
    print(f"{Colors.BLUE}{get_string('install.plan.directory')}{Colors.RESET} {install_dir}")
    print(f"{Colors.BLUE}{get_string('update.plan.components')}{Colors.RESET}")
    
    for i, component_name in enumerate(components, 1):
        if component_name in available_updates:
            info = available_updates[component_name]
            print(f"  {i}. {component_name}: v{info['current']} → v{info['available']}")
        else:
            current_version = installed_components.get(component_name, "unknown")
            print(f"  {i}. {component_name}: v{current_version} {get_string('update.plan.reinstall')}")
    
    print()


def perform_update(components: List[str], args: argparse.Namespace) -> bool:
    """Perform the actual update"""
    logger = get_logger()
    start_time = time.time()
    
    try:
        # Create installer
        installer = Installer(args.install_dir, dry_run=args.dry_run)
        
        # Create component registry
        registry = ComponentRegistry(PROJECT_ROOT / "setup" / "components")
        registry.discover_components()
        
        # Create component instances
        component_instances = registry.create_component_instances(components, args.install_dir)
        
        if not component_instances:
            logger.error(get_string("install.perform.unexpected_error", "No valid component instances created"))
            return False
        
        # Register components with installer
        installer.register_components(list(component_instances.values()))
        
        # Setup progress tracking
        progress = ProgressBar(
            total=len(components),
            prefix=get_string("update.perform.prefix"),
            suffix=""
        )
        
        # Update components
        logger.info(get_string("update.perform.updating", len(components)))
        
        # Determine backup strategy
        backup = args.backup or (not args.no_backup and not args.dry_run)
        
        config = {
            "force": args.force,
            "backup": backup,
            "dry_run": args.dry_run,
            "update_mode": True
        }
        
        success = installer.update_components(components, config)
        
        # Update progress
        for i, component_name in enumerate(components):
            if component_name in installer.updated_components:
                progress.update(i + 1, get_string("update.perform.updated", component_name))
            else:
                progress.update(i + 1, get_string("update.perform.failed", component_name))
            time.sleep(0.1)  # Brief pause for visual effect
        
        progress.finish(get_string("update.perform.complete"))
        
        # Show results
        duration = time.time() - start_time
        
        if success:
            logger.success(get_string("update.perform.success", f"{duration:.1f}"))
            
            # Show summary
            summary = installer.get_update_summary()
            if summary.get('updated'):
                logger.info(get_string("update.perform.updated_components", ', '.join(summary['updated'])))
            
            if summary.get('backup_path'):
                logger.info(get_string("install.perform.backup_created", summary['backup_path']))
                
        else:
            logger.error(get_string("update.perform.error", f"{duration:.1f}"))
            
            summary = installer.get_update_summary()
            if summary.get('failed'):
                logger.error(get_string("update.perform.failed_components", ', '.join(summary['failed'])))
        
        return success
        
    except Exception as e:
        logger.exception(get_string("update.perform.unexpected_error", e))
        return False


def run(args: argparse.Namespace) -> int:
    """Execute update operation with parsed arguments"""
    operation = UpdateOperation()
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
                get_string("update.run.header"),
                get_string("update.run.subtitle")
            )
        
        # Check if SuperClaude is installed
        if not check_installation_exists(args.install_dir):
            logger.error(get_string("update.run.not_found", args.install_dir))
            logger.info(get_string("update.run.install_first"))
            return 1
        
        # Create component registry
        logger.info(get_string("update.run.checking"))
        
        registry = ComponentRegistry(PROJECT_ROOT / "setup" / "components")
        registry.discover_components()
        
        # Get installed components
        installed_components = get_installed_components(args.install_dir)
        if not installed_components:
            logger.error(get_string("update.run.could_not_get_installed"))
            return 1
        
        # Check for available updates
        available_updates = get_available_updates(installed_components, registry)
        
        # Display update check results
        if not args.quiet:
            display_update_check(installed_components, available_updates)
        
        # If only checking for updates, exit here
        if args.check:
            return 0
        
        # Get components to update
        components = get_components_to_update(args, installed_components, available_updates)
        if components is None:
            logger.info(get_string("update.run.cancelled"))
            return 0
        elif not components:
            logger.info(get_string("update.run.no_components_selected"))
            return 0
        
        # Display update plan
        if not args.quiet:
            display_update_plan(components, available_updates, installed_components, args.install_dir)
            
            if not args.dry_run:
                if not args.yes and not confirm(get_string("update.run.confirm_proceed"), default=True):
                    logger.info(get_string("update.run.cancelled"))
                    return 0
        
        # Perform update
        success = perform_update(components, args)
        
        if success:
            if not args.quiet:
                display_success(get_string("update.run.success"))
                
                if not args.dry_run:
                    print(f"\n{Colors.CYAN}{get_string('install.run.next_steps_header')}{Colors.RESET}")
                    print(get_string("update.run.next_steps_1"))
                    print(get_string("update.run.next_steps_2"))
                    print(get_string("update.run.next_steps_3"))
                    
            return 0
        else:
            display_error(get_string("update.run.failed"))
            return 1
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}{get_string('update.run.cancelled')}{Colors.RESET}")
        return 130
    except Exception as e:
        return operation.handle_operation_error("update", e)
