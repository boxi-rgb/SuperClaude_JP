"""
SuperClaude Installation Operation Module
Refactored from install.py for unified CLI hub
"""

import sys
import time
from pathlib import Path
from typing import List, Optional, Dict, Any
import argparse

from ..base.installer import Installer
from ..core.registry import ComponentRegistry
from ..managers.config_manager import ConfigManager
from ..core.validator import Validator
from ..utils.ui import (
    display_header, display_info, display_success, display_error, 
    display_warning, Menu, confirm, ProgressBar, Colors, format_size
)
from ..utils.logger import get_logger
from ..utils.localization import get_string
from .. import DEFAULT_INSTALL_DIR, PROJECT_ROOT
from . import OperationBase


class InstallOperation(OperationBase):
    """Installation operation implementation"""
    
    def __init__(self):
        super().__init__("install")


def register_parser(subparsers, global_parser=None) -> argparse.ArgumentParser:
    """Register installation CLI arguments"""
    parents = [global_parser] if global_parser else []
    
    parser = subparsers.add_parser(
        "install",
        help=get_string("install.parser.help"),
        description=get_string("install.parser.description"),
        epilog="""
Examples:
  SuperClaude install                          # Interactive installation
  SuperClaude install --quick --dry-run        # Quick installation (dry-run)
  SuperClaude install --profile developer      # Developer profile  
  SuperClaude install --components core mcp    # Specific components
  SuperClaude install --verbose --force        # Verbose with force mode
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=parents
    )
    
    # Installation mode options
    parser.add_argument(
        "--quick", 
        action="store_true",
        help=get_string("install.parser.quick_help")
    )
    
    parser.add_argument(
        "--minimal",
        action="store_true", 
        help=get_string("install.parser.minimal_help")
    )
    
    parser.add_argument(
        "--profile",
        type=str,
        help=get_string("install.parser.profile_help")
    )
    
    parser.add_argument(
        "--components",
        type=str,
        nargs="+",
        help=get_string("install.parser.components_help")
    )
    
    # Installation options
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help=get_string("install.parser.no_backup_help")
    )
    
    parser.add_argument(
        "--list-components",
        action="store_true",
        help=get_string("install.parser.list_components_help")
    )
    
    parser.add_argument(
        "--diagnose",
        action="store_true",
        help=get_string("install.parser.diagnose_help")
    )
    
    return parser


def validate_system_requirements(validator: Validator, component_names: List[str]) -> bool:
    """Validate system requirements"""
    logger = get_logger()
    
    logger.info(get_string("install.validate.validating"))
    
    try:
        # Load requirements configuration
        config_manager = ConfigManager(PROJECT_ROOT / "config")
        requirements = config_manager.get_requirements_for_components(component_names)
        
        # Validate requirements
        success, errors = validator.validate_component_requirements(component_names, requirements)
        
        if success:
            logger.success(get_string("install.validate.success"))
            return True
        else:
            logger.error(get_string("install.validate.failed"))
            for error in errors:
                logger.error(f"  - {error}")
            
            # Provide additional guidance
            print(f"\n{Colors.CYAN}{get_string('install.validate.help_header')}{Colors.RESET}")
            print(f"  {get_string('install.validate.help_diagnose')}")
            print(f"  {get_string('install.validate.help_instructions')}")
            
            return False
            
    except Exception as e:
        logger.error(get_string("install.validate.error", e))
        return False


def get_components_to_install(args: argparse.Namespace, registry: ComponentRegistry, config_manager: ConfigManager) -> Optional[List[str]]:
    """Determine which components to install"""
    logger = get_logger()
    
    # Explicit components specified
    if args.components:
        if 'all' in args.components:
            return ["core", "commands", "hooks", "mcp"]
        return args.components
    
    # Profile-based selection
    if args.profile:
        try:
            profile_path = PROJECT_ROOT / "profiles" / f"{args.profile}.json"
            profile = config_manager.load_profile(profile_path)
            return profile["components"]
        except Exception as e:
            logger.error(get_string("install.components.load_profile_error", args.profile, e))
            return None
    
    # Quick installation
    if args.quick:
        try:
            profile_path = PROJECT_ROOT / "profiles" / "quick.json"
            profile = config_manager.load_profile(profile_path)
            return profile["components"]
        except Exception as e:
            logger.warning(get_string("install.components.load_quick_profile_error", e))
            return ["core"]  # Fallback to core only
    
    # Minimal installation
    if args.minimal:
        return ["core"]
    
    # Interactive selection
    return interactive_component_selection(registry, config_manager)


def interactive_component_selection(registry: ComponentRegistry, config_manager: ConfigManager) -> Optional[List[str]]:
    """Interactive component selection"""
    logger = get_logger()
    
    try:
        # Get available components
        available_components = registry.list_components()
        
        if not available_components:
            logger.error(get_string("install.components.no_components_available"))
            return None
        
        # Create component menu with descriptions
        menu_options = []
        component_info = {}
        
        for component_name in available_components:
            metadata = registry.get_component_metadata(component_name)
            if metadata:
                description = metadata.get("description", get_string("install.components.no_description"))
                category = metadata.get("category", get_string("install.components.unknown_category"))
                menu_options.append(f"{component_name} ({category}) - {description}")
                component_info[component_name] = metadata
            else:
                menu_options.append(f"{component_name} - {get_string('install.components.unavailable_description')}")
                component_info[component_name] = {"description": "Unknown"}
        
        # Add preset options
        preset_options = [
            get_string("install.components.quick_install"),
            get_string("install.components.minimal_install"),
            get_string("install.components.custom_selection")
        ]
        
        print(f"\n{Colors.CYAN}{get_string('install.components.options_header')}{Colors.RESET}")
        menu = Menu(get_string("install.components.select_type"), preset_options)
        choice = menu.display()
        
        if choice == -1:  # Cancelled
            return None
        elif choice == 0:  # Quick
            try:
                profile_path = PROJECT_ROOT / "profiles" / "quick.json"
                profile = config_manager.load_profile(profile_path)
                return profile["components"]
            except Exception:
                return ["core"]
        elif choice == 1:  # Minimal
            return ["core"]
        elif choice == 2:  # Custom
            print(f"\n{Colors.CYAN}{get_string('install.components.available_header')}{Colors.RESET}")
            component_menu = Menu(get_string("install.components.select_components"), menu_options, multi_select=True)
            selections = component_menu.display()
            
            if not selections:
                logger.warning(get_string("install.components.no_components_selected"))
                return None
            
            return [available_components[i] for i in selections]
        
        return None
        
    except Exception as e:
        logger.error(get_string("install.components.selection_error", e))
        return None


def display_installation_plan(components: List[str], registry: ComponentRegistry, install_dir: Path) -> None:
    """Display installation plan"""
    logger = get_logger()
    
    print(f"\n{Colors.CYAN}{Colors.BRIGHT}{get_string('install.plan.header')}{Colors.RESET}")
    print("=" * 50)
    
    # Resolve dependencies
    try:
        ordered_components = registry.resolve_dependencies(components)
        
        print(f"{Colors.BLUE}{get_string('install.plan.directory')}{Colors.RESET} {install_dir}")
        print(f"{Colors.BLUE}{get_string('install.plan.components')}{Colors.RESET}")
        
        total_size = 0
        for i, component_name in enumerate(ordered_components, 1):
            metadata = registry.get_component_metadata(component_name)
            if metadata:
                description = metadata.get("description", get_string("install.components.no_description"))
                print(f"  {i}. {component_name} - {description}")
                
                # Get size estimate if component supports it
                try:
                    instance = registry.get_component_instance(component_name, install_dir)
                    if instance and hasattr(instance, 'get_size_estimate'):
                        size = instance.get_size_estimate()
                        total_size += size
                except Exception:
                    pass
            else:
                print(f"  {i}. {component_name} - {get_string('install.plan.unknown_component')}")
        
        if total_size > 0:
            print(f"\n{Colors.BLUE}{get_string('install.plan.estimated_size')}{Colors.RESET} {format_size(total_size)}")
        
        print()
        
    except Exception as e:
        logger.error(get_string("install.plan.resolve_error", e))
        raise


def run_system_diagnostics(validator: Validator) -> None:
    """Run comprehensive system diagnostics"""
    logger = get_logger()
    
    print(f"\n{Colors.CYAN}{Colors.BRIGHT}{get_string('install.diagnostics.header')}{Colors.RESET}")
    print("=" * 50)
    
    # Run diagnostics
    diagnostics = validator.diagnose_system()
    
    # Display platform info
    print(f"{Colors.BLUE}{get_string('install.diagnostics.platform')}{Colors.RESET} {diagnostics['platform']}")
    
    # Display check results
    print(f"\n{Colors.BLUE}{get_string('install.diagnostics.checks')}{Colors.RESET}")
    all_passed = True
    
    for check_name, check_info in diagnostics['checks'].items():
        status = check_info['status']
        message = check_info['message']
        
        if status == 'pass':
            print(f"  ✅ {check_name}: {message}")
        else:
            print(f"  ❌ {check_name}: {message}")
            all_passed = False
    
    # Display issues and recommendations
    if diagnostics['issues']:
        print(f"\n{Colors.YELLOW}{get_string('install.diagnostics.issues')}{Colors.RESET}")
        for issue in diagnostics['issues']:
            print(f"  ⚠️  {issue}")
        
        print(f"\n{Colors.CYAN}{get_string('install.diagnostics.recommendations')}{Colors.RESET}")
        for recommendation in diagnostics['recommendations']:
            print(recommendation)
    
    # Summary
    if all_passed:
        print(f"\n{Colors.GREEN}{get_string('install.diagnostics.all_passed')}{Colors.RESET}")
    else:
        print(f"\n{Colors.YELLOW}{get_string('install.diagnostics.issues_found')}{Colors.RESET}")
    
    print(f"\n{Colors.BLUE}{get_string('install.diagnostics.next_steps')}{Colors.RESET}")
    if all_passed:
        print(f"  {get_string('install.diagnostics.next_steps_passed_1')}")
        print(f"  {get_string('install.diagnostics.next_steps_passed_2')}")
    else:
        print(f"  {get_string('install.diagnostics.next_steps_failed_1')}")
        print(f"  {get_string('install.diagnostics.next_steps_failed_2')}")
        print(f"  {get_string('install.diagnostics.next_steps_failed_3')}")


def perform_installation(components: List[str], args: argparse.Namespace) -> bool:
    """Perform the actual installation"""
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
            logger.error("No valid component instances created")
            return False
        
        # Register components with installer
        installer.register_components(list(component_instances.values()))
        
        # Resolve dependencies
        ordered_components = registry.resolve_dependencies(components)
        
        # Setup progress tracking
        progress = ProgressBar(
            total=len(ordered_components),
            prefix=get_string("install.perform.prefix"),
            suffix=""
        )
        
        # Install components
        logger.info(get_string("install.perform.installing", len(ordered_components)))
        
        config = {
            "force": args.force,
            "backup": not args.no_backup,
            "dry_run": args.dry_run
        }
        
        success = installer.install_components(ordered_components, config)
        
        # Update progress
        for i, component_name in enumerate(ordered_components):
            if component_name in installer.installed_components:
                progress.update(i + 1, get_string("install.perform.installed", component_name))
            else:
                progress.update(i + 1, get_string("install.perform.failed", component_name))
            time.sleep(0.1)  # Brief pause for visual effect
        
        progress.finish(get_string("install.perform.complete"))
        
        # Show results
        duration = time.time() - start_time
        
        if success:
            logger.success(get_string("install.perform.success", f"{duration:.1f}"))
            
            # Show summary
            summary = installer.get_installation_summary()
            if summary['installed']:
                logger.info(get_string("install.perform.installed_components", ', '.join(summary['installed'])))
            
            if summary['backup_path']:
                logger.info(get_string("install.perform.backup_created", summary['backup_path']))
                
        else:
            logger.error(get_string("install.perform.error", f"{duration:.1f}"))
            
            summary = installer.get_installation_summary()
            if summary['failed']:
                logger.error(get_string("install.perform.failed_components", ', '.join(summary['failed'])))
        
        return success
        
    except Exception as e:
        logger.exception(get_string("install.perform.unexpected_error", e))
        return False


def run(args: argparse.Namespace) -> int:
    """Execute installation operation with parsed arguments"""
    operation = InstallOperation()
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
                get_string("install.run.header"),
                get_string("install.run.subtitle")
            )
        
        # Handle special modes
        if args.list_components:
            registry = ComponentRegistry(PROJECT_ROOT / "setup" / "components")
            registry.discover_components()
            
            components = registry.list_components()
            if components:
                print(f"\n{Colors.CYAN}{get_string('install.components.available_header')}{Colors.RESET}")
                for component_name in components:
                    metadata = registry.get_component_metadata(component_name)
                    if metadata:
                        desc = metadata.get("description", get_string("install.components.no_description"))
                        category = metadata.get("category", get_string("install.components.unknown_category"))
                        print(f"  {component_name} ({category}) - {desc}")
                    else:
                        print(f"  {component_name} - {get_string('install.plan.unknown_component')}")
            else:
                print(get_string("install.run.no_components_found"))
            return 0
        
        # Handle diagnostic mode
        if args.diagnose:
            validator = Validator()
            run_system_diagnostics(validator)
            return 0
        
        # Create component registry and load configuration
        logger.info(get_string("install.run.initializing"))
        
        registry = ComponentRegistry(PROJECT_ROOT / "setup" / "components")
        registry.discover_components()
        
        config_manager = ConfigManager(PROJECT_ROOT / "config")
        validator = Validator()
        
        # Validate configuration
        config_errors = config_manager.validate_config_files()
        if config_errors:
            logger.error(get_string("install.run.config_validation_failed"))
            for error in config_errors:
                logger.error(f"  - {error}")
            return 1
        
        # Get components to install
        components = get_components_to_install(args, registry, config_manager)
        if not components:
            logger.error(get_string("install.run.no_components_selected"))
            return 1
        
        # Validate system requirements
        if not validate_system_requirements(validator, components):
            if not args.force:
                logger.error(get_string("install.run.reqs_not_met"))
                return 1
            else:
                logger.warning(get_string("install.run.reqs_not_met_force"))
        
        # Check for existing installation
        if args.install_dir.exists() and not args.force:
            if not args.dry_run:
                logger.warning(get_string("install.run.dir_exists", args.install_dir))
                if not args.yes and not confirm(get_string("install.run.confirm_update"), default=False):
                    logger.info(get_string("install.run.cancelled"))
                    return 0
        
        # Display installation plan
        if not args.quiet:
            display_installation_plan(components, registry, args.install_dir)
            
            if not args.dry_run:
                if not args.yes and not confirm(get_string("install.run.confirm_proceed"), default=True):
                    logger.info(get_string("install.run.cancelled"))
                    return 0
        
        # Perform installation
        success = perform_installation(components, args)
        
        if success:
            if not args.quiet:
                display_success(get_string("install.run.success"))
                
                if not args.dry_run:
                    print(f"\n{Colors.CYAN}{get_string('install.run.next_steps_header')}{Colors.RESET}")
                    print(get_string("install.run.next_steps_1"))
                    print(get_string("install.run.next_steps_2", args.install_dir))
                    print(get_string("install.run.next_steps_3"))
                    
            return 0
        else:
            display_error(get_string("install.run.failed"))
            return 1
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}{get_string('install.run.cancelled')}{Colors.RESET}")
        return 130
    except Exception as e:
        return operation.handle_operation_error("install", e)
