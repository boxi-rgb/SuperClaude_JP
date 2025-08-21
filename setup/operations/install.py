"""
SuperClaude Installation Operation Module
This module serves as the entry point for the 'install' command.
It orchestrates the installation process by calling helpers from the
'install_logic' subpackage.
"""

import sys
import argparse
from pathlib import Path

# --- Local Imports ---
from .. import DEFAULT_INSTALL_DIR, PROJECT_ROOT
from . import OperationBase
from ..core.registry import ComponentRegistry
from ..managers.config_manager import ConfigManager
from ..core.validator import Validator
from ..utils.ui import display_header, display_success, display_error, display_info, display_warning, confirm, Colors
from ..utils.logger import get_logger
from ..utils.localization import get_string

# --- Refactored Logic Imports ---
from .install_logic.ui import (
    display_installation_plan,
    run_system_diagnostics,
)
from .install_logic.selector import get_components_to_install
from .install_logic.validator import validate_system_requirements
from .install_logic.installer import perform_installation


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
    parser.add_argument("--quick", action="store_true", help=get_string("install.parser.quick_help"))
    parser.add_argument("--minimal", action="store_true", help=get_string("install.parser.minimal_help"))
    parser.add_argument("--profile", type=str, help=get_string("install.parser.profile_help"))
    parser.add_argument("--components", type=str, nargs="+", help=get_string("install.parser.components_help"))
    
    # Installation options
    parser.add_argument("--no-backup", action="store_true", help=get_string("install.parser.no_backup_help"))
    parser.add_argument("--list-components", action="store_true", help=get_string("install.parser.list_components_help"))
    parser.add_argument("--diagnose", action="store_true", help=get_string("install.parser.diagnose_help"))
    
    return parser


def run(args: argparse.Namespace) -> int:
    """Execute installation operation with parsed arguments"""
    operation = InstallOperation()
    operation.setup_operation_logging(args)
    logger = get_logger()

    # ✅ Inserted validation code - This can stay here as a pre-check
    expected_home = Path.home().resolve()
    actual_dir = args.install_dir.resolve()
    if not str(actual_dir).startswith(str(expected_home)):
        display_error(f"\n[✗] {get_string('install.run.invalid_path_header')}")
        display_error(f"    {get_string('install.run.invalid_path_expected', expected_home)}")
        display_error(f"    {get_string('install.run.invalid_path_provided', actual_dir)}")
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
            display_header(get_string("install.run.header"), get_string("install.run.subtitle"))

        # Initialize core managers
        registry = ComponentRegistry(PROJECT_ROOT / "setup" / "components")
        validator = Validator()
        
        # Handle special modes (list-components, diagnose)
        if args.list_components:
            # This logic is simple enough to keep here or move to UI. Keep for now.
            registry.discover_components()
            components = registry.list_components()
            if components:
                display_info(f"\n{Colors.CYAN}{get_string('install.components.available_header')}{Colors.RESET}")
                for component_name in components:
                    metadata = registry.get_component_metadata(component_name)
                    if metadata:
                        desc = metadata.get("description", get_string("install.components.no_description"))
                        category = metadata.get("category", get_string("install.components.unknown_category"))
                        display_info(f"  {component_name} ({category}) - {desc}")
                    else:
                        display_info(f"  {component_name} - {get_string('install.plan.unknown_component')}")
            else:
                display_info(get_string("install.run.no_components_found"))
            return 0
        
        if args.diagnose:
            run_system_diagnostics(validator)
            return 0
        
        # --- Main Installation Workflow ---
        logger.info(get_string("install.run.initializing"))
        registry.discover_components()
        config_manager = ConfigManager(PROJECT_ROOT / "config")
        
        config_errors = config_manager.validate_config_files()
        if config_errors:
            logger.error(get_string("install.run.config_validation_failed"))
            for error in config_errors:
                logger.error(f"  - {error}")
            return 1
        
        components = get_components_to_install(args, registry, config_manager)
        if not components:
            logger.error(get_string("install.run.no_components_selected"))
            return 1
        
        if not validate_system_requirements(validator, components):
            if not args.force:
                logger.error(get_string("install.run.reqs_not_met"))
                return 1
            else:
                logger.warning(get_string("install.run.reqs_not_met_force"))
        
        if args.install_dir.exists() and not args.force and not args.dry_run:
            logger.warning(get_string("install.run.dir_exists", args.install_dir))
            if not args.yes and not confirm(get_string("install.run.confirm_update"), default=False):
                logger.info(get_string("install.run.cancelled"))
                return 0
        
        if not args.quiet:
            display_installation_plan(components, registry, args.install_dir)
            if not args.dry_run:
                if not args.yes and not confirm(get_string("install.run.confirm_proceed"), default=True):
                    logger.info(get_string("install.run.cancelled"))
                    return 0
        
        success = perform_installation(components, args)
        
        if success:
            if not args.quiet:
                display_success(get_string("install.run.success"))
                if not args.dry_run:
                    display_info(f"\n{Colors.CYAN}{get_string('install.run.next_steps_header')}{Colors.RESET}")
                    display_info(get_string("install.run.next_steps_1"))
                    display_info(get_string("install.run.next_steps_2", args.install_dir))
                    display_info(get_string("install.run.next_steps_3"))
            return 0
        else:
            display_error(get_string("install.run.failed"))
            return 1
            
    except KeyboardInterrupt:
        display_warning(f"\n{Colors.YELLOW}{get_string('install.run.cancelled')}{Colors.RESET}")
        return 130
    except Exception as e:
        return operation.handle_operation_error("install", e)
