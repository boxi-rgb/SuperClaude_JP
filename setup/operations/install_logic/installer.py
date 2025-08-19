"""
Core installation logic for the installation operation.
"""

import time
import argparse
from typing import List

from setup.base.installer import Installer
from setup.core.registry import ComponentRegistry
from setup.utils.ui import ProgressBar
from setup.utils.logger import get_logger
from setup.utils.localization import get_string
from setup import PROJECT_ROOT


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
