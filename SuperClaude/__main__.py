#!/usr/bin/env python3
"""
SuperClaude Framework Management Hub
Unified entry point for all SuperClaude operations

Usage:
    SuperClaude install [options]
    SuperClaude update [options]
    SuperClaude uninstall [options]
    SuperClaude backup [options]
    SuperClaude --help
"""

import sys
import argparse
import subprocess
import difflib
from pathlib import Path
from typing import Dict, Callable


# Try to import utilities from the setup package
try:
    from .mcp_manager import MCPManager
    from .mcp_diagnostics import MCPDiagnostics
    from setup.utils.localization import get_string, set_language
    from setup.utils.ui import (
        display_header, display_info, display_success, display_error,
        display_warning, Colors
    )
    from setup.utils.logger import setup_logging, get_logger, LogLevel
    from setup import DEFAULT_INSTALL_DIR
except ImportError:
    # Provide minimal fallback functions and constants if imports fail
    class Colors:
        RED = YELLOW = GREEN = CYAN = RESET = ""

    def display_error(msg): print(f"[ERROR] {msg}")
    def display_warning(msg): print(f"[WARN] {msg}")
    def display_success(msg): print(f"[OK] {msg}")
    def display_info(msg): print(f"[INFO] {msg}")
    def display_header(title, subtitle): print(f"{title} - {subtitle}")
    def get_logger(): return None
    def setup_logging(*args, **kwargs): pass
    class LogLevel:
        ERROR = 40
        INFO = 20
        DEBUG = 10
    
    # Default install directory fallback
    DEFAULT_INSTALL_DIR = Path.home() / ".claude"


def create_global_parser() -> argparse.ArgumentParser:
    """Create shared parser for global flags used by all commands"""
    global_parser = argparse.ArgumentParser(add_help=False)

    global_parser.add_argument("--verbose", "-v", action="store_true",
                               help=get_string("global.verbose_help"))
    global_parser.add_argument("--quiet", "-q", action="store_true",
                               help=get_string("global.quiet_help"))
    global_parser.add_argument("--install-dir", type=Path, default=DEFAULT_INSTALL_DIR,
                               help=get_string("global.install_dir_help", DEFAULT_INSTALL_DIR))
    global_parser.add_argument("--dry-run", action="store_true",
                               help=get_string("global.dry_run_help"))
    global_parser.add_argument("--force", action="store_true",
                               help=get_string("global.force_help"))
    global_parser.add_argument("--yes", "-y", action="store_true",
                               help=get_string("global.yes_help"))

    return global_parser


def create_parser():
    """Create the main CLI parser and attach subcommand parsers"""
    global_parser = create_global_parser()

    parser = argparse.ArgumentParser(
        prog="SuperClaude",
        description="SuperClaude Framework Management Hub - Unified CLI",
        epilog="""
Examples:
  SuperClaude install --dry-run
  SuperClaude update --verbose
  SuperClaude backup --create
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[global_parser]
    )

    parser.add_argument("--version", action="version", version="SuperClaude v3.0.0")

    subparsers = parser.add_subparsers(
        dest="operation",
        title="Operations",
        description="Framework operations to perform"
    )

    return parser, subparsers, global_parser


def setup_global_environment(args: argparse.Namespace) -> None:
    """Set up logging and shared runtime environment based on args"""
    # Determine log level
    if args.quiet:
        level = LogLevel.ERROR
    elif args.verbose:
        level = LogLevel.DEBUG
    else:
        level = LogLevel.INFO

    # Define log directory unless it's a dry run
    log_dir = args.install_dir / "logs" if not args.dry_run else None
    setup_logging("superclaude_hub", log_dir=log_dir, console_level=level)

    # Log startup context
    logger = get_logger()
    if logger:
        logger.debug(f"SuperClaude called with operation: {getattr(args, 'operation', 'None')}")
        logger.debug(f"Arguments: {vars(args)}")


def get_operation_modules() -> Dict[str, str]:
    """Return supported operations and their descriptions"""
    ops = {
        "install": "Install SuperClaude framework components",
        "update": "Update existing SuperClaude installation",
        "uninstall": "Remove SuperClaude installation",
        "backup": "Backup and restore operations",
        "add_mcp": "Install a new MCP server on-demand",
        "diagnose_mcp": "Run diagnostics for MCP server issues"
    }
    # Try to use localization if available, but fall back to the hardcoded descriptions
    try:
        # These keys exist in the .json locale files
        ops["install"] = get_string("op.install")
        ops["update"] = get_string("op.update")
        ops["uninstall"] = get_string("op.uninstall")
        ops["backup"] = get_string("op.backup")
        # For our new commands, we can keep the hardcoded description as a fallback
        ops["add_mcp"] = get_string("op.add_mcp", "Install a new MCP server on-demand")
        ops["diagnose_mcp"] = get_string("op.diagnose_mcp", "Run diagnostics for MCP server issues")
    except NameError:
        # This block will be hit if get_string isn't defined, which is fine.
        pass
    return ops


def run_add_mcp(args: argparse.Namespace) -> int:
    """Run the add_mcp operation."""
    manager = MCPManager()
    if not args.mcp_names:
        display_warning("No MCP server names provided. Listing available servers.")
        manager.list_mcps()
        return 0

    success_count = 0
    for name in args.mcp_names:
        success, message = manager.install_mcp(name)
        if success:
            display_success(message)
            success_count += 1
        else:
            display_error(message)

    if success_count == len(args.mcp_names):
        return 0  # All successful
    elif success_count > 0:
        return 2 # Partial success
    else:
        return 1 # All failed


def register_add_mcp_parser(subparsers, global_parser):
    """Register the parser for the 'add_mcp' command."""
    parser = subparsers.add_parser(
        "add_mcp",
        help="Install a new MCP server on-demand",
        parents=[global_parser]
    )
    parser.add_argument(
        "mcp_names",
        nargs='*',
        help="The name(s) of the MCP server(s) to install."
    )
    parser.set_defaults(run_func=run_add_mcp)


def load_operation_module(name: str):
    """Try to dynamically import an operation module"""
    try:
        return __import__(f"setup.operations.{name}", fromlist=[name])
    except ImportError as e:
        logger = get_logger()
        if logger:
            logger.error(f"Module '{name}' failed to load: {e}")
        return None


def run_diagnose_mcp(args: argparse.Namespace) -> int:
    """Run the diagnose_mcp operation."""
    diagnostics = MCPDiagnostics()
    diagnostics.run()
    return 0


def register_diagnose_mcp_parser(subparsers, global_parser):
    """Register the parser for the 'diagnose_mcp' command."""
    parser = subparsers.add_parser(
        "diagnose_mcp",
        help="Run a series of checks to troubleshoot MCP server issues.",
        parents=[global_parser]
    )
    parser.set_defaults(run_func=run_diagnose_mcp)


def register_operation_parsers(subparsers, global_parser) -> Dict[str, Callable]:
    """Register subcommand parsers and map operation names to their run functions"""
    operations = {}

    # Define all commands and their handlers
    command_handlers = {
        "add_mcp": {"parser": register_add_mcp_parser, "runner": run_add_mcp},
        "diagnose_mcp": {"parser": register_diagnose_mcp_parser, "runner": run_diagnose_mcp},
    }

    all_known_ops = get_operation_modules()

    for name, desc in all_known_ops.items():
        if name in command_handlers:
            # Handle locally defined commands
            handler = command_handlers[name]
            handler["parser"](subparsers, global_parser)
            operations[name] = handler["runner"]
        else:
            # Handle dynamically loaded commands
            module = load_operation_module(name)
            if module and hasattr(module, 'register_parser') and hasattr(module, 'run'):
                module.register_parser(subparsers, global_parser)
                operations[name] = module.run

    return operations


def main() -> int:
    """Main entry point"""
    try:
        # Set language
        try:
            set_language('ja')
        except NameError:
            pass

        parser, subparsers, global_parser = create_parser()
        operations = register_operation_parsers(subparsers, global_parser)
        args = parser.parse_args()

        # Setup global context (logging, install path, etc.)
        setup_global_environment(args)
        logger = get_logger()

        # No operation provided? Show help manually unless in quiet mode
        if not getattr(args, 'operation', None):
            if not args.quiet:
                display_header(get_string("main.title"), get_string("main.subtitle"))
                print(f"{Colors.CYAN}{get_string('main.available_operations')}{Colors.RESET}")
                for op, desc in get_operation_modules().items():
                    print(f"  {op:<12} {desc}")
            return 0

        # Handle unknown operations and suggest corrections
        if args.operation not in operations:
            close = difflib.get_close_matches(args.operation, operations.keys(), n=1)
            suggestion = f"Did you mean: {close[0]}?" if close else ""
            if logger:
                logger.error(f"Unknown operation: '{args.operation}'. {suggestion}")
            display_error(f"Unknown operation: '{args.operation}'. {suggestion}")
            return 1

        # Execute operation
        run_func = operations.get(args.operation)

        if not run_func:
            if logger:
                logger.error(f"No run function found for operation '{args.operation}'.")
            display_error(f"No run function found for operation '{args.operation}'.")
            return 1

        if logger:
            logger.info(f"Executing operation: {args.operation}")
        return run_func(args)

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Operation cancelled by user{Colors.RESET}")
        if logger:
            logger.warning("Operation cancelled by user.")
        return 130
    except Exception as e:
        logger = get_logger()
        if logger:
            logger.exception(f"Unhandled error: {e}")
        print(f"{Colors.RED}[ERROR] {e}{Colors.RESET}")
        return 1


# Entrypoint guard
if __name__ == "__main__":
    sys.exit(main())
    

