"""
SuperClaude Backup Operation Module
Refactored from backup.py for unified CLI hub
"""

import sys
import time
import tarfile
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple
import argparse

from ..managers.settings_manager import SettingsManager
from ..utils.ui import (
    display_header, display_info, display_success, display_error, 
    display_warning, Menu, confirm, ProgressBar, Colors, format_size
)
from ..utils.logger import get_logger
from ..utils.localization import get_string
from .. import DEFAULT_INSTALL_DIR
from . import OperationBase


class BackupOperation(OperationBase):
    """Backup operation implementation"""
    
    def __init__(self):
        super().__init__("backup")


def register_parser(subparsers, global_parser=None) -> argparse.ArgumentParser:
    """Register backup CLI arguments"""
    parents = [global_parser] if global_parser else []
    
    parser = subparsers.add_parser(
        "backup",
        help=get_string("backup.parser.help"),
        description=get_string("backup.parser.description"),
        epilog="""
Examples:
  SuperClaude backup --create               # Create new backup
  SuperClaude backup --list --verbose       # List available backups (verbose)
  SuperClaude backup --restore              # Interactive restore
  SuperClaude backup --restore backup.tar.gz  # Restore specific backup
  SuperClaude backup --info backup.tar.gz   # Show backup information
  SuperClaude backup --cleanup --force      # Clean up old backups (forced)
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=parents
    )
    
    # Backup operations (mutually exclusive)
    operation_group = parser.add_mutually_exclusive_group(required=True)
    
    operation_group.add_argument(
        "--create",
        action="store_true",
        help=get_string("backup.parser.create_help")
    )
    
    operation_group.add_argument(
        "--list",
        action="store_true",
        help=get_string("backup.parser.list_help")
    )
    
    operation_group.add_argument(
        "--restore",
        nargs="?",
        const="interactive",
        help=get_string("backup.parser.restore_help")
    )
    
    operation_group.add_argument(
        "--info",
        type=str,
        help=get_string("backup.parser.info_help")
    )
    
    operation_group.add_argument(
        "--cleanup",
        action="store_true",
        help=get_string("backup.parser.cleanup_help")
    )
    
    # Backup options
    parser.add_argument(
        "--backup-dir",
        type=Path,
        help=get_string("backup.parser.backup_dir_help")
    )
    
    parser.add_argument(
        "--name",
        type=str,
        help=get_string("backup.parser.name_help")
    )
    
    parser.add_argument(
        "--compress",
        choices=["none", "gzip", "bzip2"],
        default="gzip",
        help=get_string("backup.parser.compress_help")
    )
    
    # Restore options
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help=get_string("backup.parser.overwrite_help")
    )
    
    # Cleanup options
    parser.add_argument(
        "--keep",
        type=int,
        default=5,
        help=get_string("backup.parser.keep_help")
    )
    
    parser.add_argument(
        "--older-than",
        type=int,
        help=get_string("backup.parser.older_than_help")
    )
    
    return parser


def get_backup_directory(args: argparse.Namespace) -> Path:
    """Get the backup directory path"""
    if args.backup_dir:
        return args.backup_dir
    else:
        return args.install_dir / "backups"


def check_installation_exists(install_dir: Path) -> bool:
    """Check if SuperClaude installation (v2 included) exists"""
    settings_manager = SettingsManager(install_dir)

    return settings_manager.check_installation_exists() or settings_manager.check_v2_installation_exists()


def get_backup_info(backup_path: Path) -> Dict[str, Any]:
    """Get information about a backup file"""
    info = {
        "path": backup_path,
        "exists": backup_path.exists(),
        "size": 0,
        "created": None,
        "metadata": {}
    }
    
    if not backup_path.exists():
        return info
    
    try:
        # Get file stats
        stats = backup_path.stat()
        info["size"] = stats.st_size
        info["created"] = datetime.fromtimestamp(stats.st_mtime)
        
        # Try to read metadata from backup
        if backup_path.suffix == ".gz":
            mode = "r:gz"
        elif backup_path.suffix == ".bz2":
            mode = "r:bz2"
        else:
            mode = "r"
        
        with tarfile.open(backup_path, mode) as tar:
            # Look for metadata file
            try:
                metadata_member = tar.getmember("backup_metadata.json")
                metadata_file = tar.extractfile(metadata_member)
                if metadata_file:
                    info["metadata"] = json.loads(metadata_file.read().decode())
            except KeyError:
                pass  # No metadata file
            
            # Get list of files in backup
            info["files"] = len(tar.getnames())
            
    except Exception as e:
        info["error"] = str(e)
    
    return info


def list_backups(backup_dir: Path) -> List[Dict[str, Any]]:
    """List all available backups"""
    backups = []
    
    if not backup_dir.exists():
        return backups
    
    # Find all backup files
    for backup_file in backup_dir.glob("*.tar*"):
        if backup_file.is_file():
            info = get_backup_info(backup_file)
            backups.append(info)
    
    # Sort by creation date (newest first)
    backups.sort(key=lambda x: x.get("created", datetime.min), reverse=True)
    
    return backups


def display_backup_list(backups: List[Dict[str, Any]]) -> None:
    """Display list of available backups"""
    print(f"\n{Colors.CYAN}{Colors.BRIGHT}{get_string('backup.list.header')}{Colors.RESET}")
    print("=" * 70)
    
    if not backups:
        print(f"{Colors.YELLOW}{get_string('backup.list.no_backups')}{Colors.RESET}")
        return
    
    print(f"{get_string('backup.list.name_header'):<30} {get_string('backup.list.size_header'):<10} {get_string('backup.list.created_header'):<20} {get_string('backup.list.files_header'):<8}")
    print("-" * 70)
    
    for backup in backups:
        name = backup["path"].name
        size = format_size(backup["size"]) if backup["size"] > 0 else get_string("backup.list.unknown")
        created = backup["created"].strftime("%Y-%m-%d %H:%M") if backup["created"] else get_string("backup.list.unknown")
        files = str(backup.get("files", get_string("backup.list.unknown")))
        
        print(f"{name:<30} {size:<10} {created:<20} {files:<8}")
    
    print()


def create_backup_metadata(install_dir: Path) -> Dict[str, Any]:
    """Create metadata for the backup"""
    metadata = {
        "backup_version": "3.0.0",
        "created": datetime.now().isoformat(),
        "install_dir": str(install_dir),
        "components": {},
        "framework_version": get_string("backup.list.unknown")
    }
    
    try:
        # Get installed components from metadata
        settings_manager = SettingsManager(install_dir)
        framework_config = settings_manager.get_metadata_setting("framework")
        
        if framework_config:
            metadata["framework_version"] = framework_config.get("version", get_string("backup.list.unknown"))
            
            if "components" in framework_config:
                for component_name in framework_config["components"]:
                    version = settings_manager.get_component_version(component_name)
                    if version:
                        metadata["components"][component_name] = version
    except Exception:
        pass  # Continue without metadata
    
    return metadata


def create_backup(args: argparse.Namespace) -> bool:
    """Create a new backup"""
    logger = get_logger()
    
    try:
        # Check if installation exists
        if not check_installation_exists(args.install_dir):
            logger.error(get_string("backup.create.no_installation", args.install_dir))
            return False
        
        # Setup backup directory
        backup_dir = get_backup_directory(args)
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate backup filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if args.name:
            backup_name = f"{args.name}_{timestamp}"
        else:
            backup_name = f"superclaude_backup_{timestamp}"
        
        # Determine compression
        if args.compress == "gzip":
            backup_file = backup_dir / f"{backup_name}.tar.gz"
            mode = "w:gz"
        elif args.compress == "bzip2":
            backup_file = backup_dir / f"{backup_name}.tar.bz2"
            mode = "w:bz2"
        else:
            backup_file = backup_dir / f"{backup_name}.tar"
            mode = "w"
        
        logger.info(get_string("backup.create.creating", backup_file))
        
        # Create metadata
        metadata = create_backup_metadata(args.install_dir)
        
        # Create backup
        start_time = time.time()
        
        with tarfile.open(backup_file, mode) as tar:
            # Add metadata file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                json.dump(metadata, temp_file, indent=2)
                temp_file.flush()
                tar.add(temp_file.name, arcname="backup_metadata.json")
                Path(temp_file.name).unlink()  # Clean up temp file
            
            # Add installation directory contents
            files_added = 0
            for item in args.install_dir.rglob("*"):
                if item.is_file() and item != backup_file:
                    try:
                        # Create relative path for archive
                        rel_path = item.relative_to(args.install_dir)
                        tar.add(item, arcname=str(rel_path))
                        files_added += 1
                        
                        if files_added % 10 == 0:
                            logger.debug(get_string("backup.create.added_files", files_added))
                            
                    except Exception as e:
                        logger.warning(get_string("backup.create.add_error", item, e))
        
        duration = time.time() - start_time
        file_size = backup_file.stat().st_size
        
        logger.success(get_string("backup.create.success", f"{duration:.1f}"))
        logger.info(get_string("backup.create.file", backup_file))
        logger.info(get_string("backup.create.files_archived", files_added))
        logger.info(get_string("backup.create.size", format_size(file_size)))
        
        return True
        
    except Exception as e:
        logger.exception(get_string("backup.create.failed", e))
        return False


def restore_backup(backup_path: Path, args: argparse.Namespace) -> bool:
    """Restore from a backup file"""
    logger = get_logger()
    
    try:
        if not backup_path.exists():
            logger.error(get_string("backup.restore.not_found", backup_path))
            return False
        
        # Check backup file
        info = get_backup_info(backup_path)
        if "error" in info:
            logger.error(get_string("backup.restore.invalid", info['error']))
            return False
        
        logger.info(get_string("backup.restore.restoring", backup_path))
        
        # Determine compression
        if backup_path.suffix == ".gz":
            mode = "r:gz"
        elif backup_path.suffix == ".bz2":
            mode = "r:bz2"
        else:
            mode = "r"
        
        # Create backup of current installation if it exists
        if check_installation_exists(args.install_dir) and not args.dry_run:
            logger.info(get_string("backup.restore.creating_backup"))
            # This would call create_backup internally
        
        # Extract backup
        start_time = time.time()
        files_restored = 0
        
        with tarfile.open(backup_path, mode) as tar:
            # Extract all files except metadata
            for member in tar.getmembers():
                if member.name == "backup_metadata.json":
                    continue
                
                try:
                    target_path = args.install_dir / member.name
                    
                    # Check if file exists and overwrite flag
                    if target_path.exists() and not args.overwrite:
                        logger.warning(get_string("backup.restore.skipping", target_path))
                        continue
                    
                    # Extract file
                    tar.extract(member, args.install_dir)
                    files_restored += 1
                    
                    if files_restored % 10 == 0:
                        logger.debug(get_string("backup.restore.restored_files", files_restored))
                        
                except Exception as e:
                    logger.warning(get_string("backup.restore.error", member.name, e))
        
        duration = time.time() - start_time
        
        logger.success(get_string("backup.restore.success", f"{duration:.1f}"))
        logger.info(get_string("backup.restore.files_restored", files_restored))
        
        return True
        
    except Exception as e:
        logger.exception(get_string("backup.restore.failed", e))
        return False


def interactive_restore_selection(backups: List[Dict[str, Any]]) -> Optional[Path]:
    """Interactive backup selection for restore"""
    if not backups:
        print(f"{Colors.YELLOW}{get_string('backup.restore.no_backups')}{Colors.RESET}")
        return None
    
    print(f"\n{Colors.CYAN}{get_string('backup.restore.select_header')}{Colors.RESET}")
    
    # Create menu options
    backup_options = []
    for backup in backups:
        name = backup["path"].name
        size = format_size(backup["size"]) if backup["size"] > 0 else get_string("backup.list.unknown")
        created = backup["created"].strftime("%Y-%m-%d %H:%M") if backup["created"] else get_string("backup.list.unknown")
        backup_options.append(f"{name} ({size}, {created})")
    
    menu = Menu(get_string("backup.restore.select_prompt"), backup_options)
    choice = menu.display()
    
    if choice == -1 or choice >= len(backups):
        return None
    
    return backups[choice]["path"]


def cleanup_old_backups(backup_dir: Path, args: argparse.Namespace) -> bool:
    """Clean up old backup files"""
    logger = get_logger()
    
    try:
        backups = list_backups(backup_dir)
        if not backups:
            logger.info(get_string("backup.cleanup.no_backups"))
            return True
        
        to_remove = []
        
        # Remove by age
        if args.older_than:
            from datetime import timedelta
            cutoff_date = datetime.now() - timedelta(days=args.older_than)
            for backup in backups:
                if backup["created"] and backup["created"] < cutoff_date:
                    to_remove.append(backup)
        
        # Keep only N most recent
        if args.keep and len(backups) > args.keep:
            # Sort by date and take oldest ones to remove
            backups.sort(key=lambda x: x.get("created", datetime.min), reverse=True)
            to_remove.extend(backups[args.keep:])
        
        # Remove duplicates
        to_remove = list({backup["path"]: backup for backup in to_remove}.values())
        
        if not to_remove:
            logger.info(get_string("backup.cleanup.no_backups"))
            return True
        
        logger.info(get_string("backup.cleanup.cleaning_up", len(to_remove)))
        
        for backup in to_remove:
            try:
                backup["path"].unlink()
                logger.info(get_string("backup.cleanup.removed", backup['path'].name))
            except Exception as e:
                logger.warning(get_string("backup.cleanup.error", backup['path'].name, e))
        
        return True
        
    except Exception as e:
        logger.exception(get_string("backup.cleanup.failed", e))
        return False


def run(args: argparse.Namespace) -> int:
    """Execute backup operation with parsed arguments"""
    operation = BackupOperation()
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
                get_string("backup.run.header"),
                get_string("backup.run.subtitle")
            )
        
        backup_dir = get_backup_directory(args)
        
        # Handle different backup operations
        if args.create:
            success = create_backup(args)
            
        elif args.list:
            backups = list_backups(backup_dir)
            display_backup_list(backups)
            success = True
            
        elif args.restore:
            if args.restore == "interactive":
                # Interactive restore
                backups = list_backups(backup_dir)
                backup_path = interactive_restore_selection(backups)
                if not backup_path:
                    logger.info(get_string("backup.run.restore_cancelled"))
                    return 0
            else:
                # Specific backup file
                backup_path = Path(args.restore)
                if not backup_path.is_absolute():
                    backup_path = backup_dir / backup_path
            
            success = restore_backup(backup_path, args)
            
        elif args.info:
            backup_path = Path(args.info)
            if not backup_path.is_absolute():
                backup_path = backup_dir / backup_path
            
            info = get_backup_info(backup_path)
            if info["exists"]:
                print(f"\n{Colors.CYAN}{get_string('backup.run.info_header')}{Colors.RESET}")
                print(f"{get_string('backup.run.info_file')} {info['path']}")
                print(f"{get_string('backup.run.info_size')} {format_size(info['size'])}")
                print(f"{get_string('backup.run.info_created')} {info['created']}")
                print(f"{get_string('backup.run.info_files')} {info.get('files', get_string('backup.list.unknown'))}")
                
                if info["metadata"]:
                    metadata = info["metadata"]
                    print(f"{get_string('backup.run.info_framework_version')} {metadata.get('framework_version', get_string('backup.list.unknown'))}")
                    if metadata.get("components"):
                        print(f"{get_string('backup.run.info_components')}")
                        for comp, ver in metadata["components"].items():
                            print(f"  {comp}: v{ver}")
            else:
                logger.error(get_string("backup.restore.not_found", backup_path))
                success = False
            success = True
            
        elif args.cleanup:
            success = cleanup_old_backups(backup_dir, args)
        
        else:
            logger.error(get_string("backup.run.no_op"))
            success = False
        
        if success:
            if not args.quiet and args.create:
                display_success(get_string("backup.run.create_success"))
            elif not args.quiet and args.restore:
                display_success(get_string("backup.run.restore_success"))
            return 0
        else:
            display_error(get_string("backup.run.failed"))
            return 1
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}{get_string('backup.run.cancelled')}{Colors.RESET}")
        return 130
    except Exception as e:
        return operation.handle_operation_error("backup", e)
