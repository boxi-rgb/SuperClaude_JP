"""
Component selection logic for the installation operation.
"""

import argparse
from typing import List, Optional

from setup.core.registry import ComponentRegistry
from setup.managers.config_manager import ConfigManager
from setup.utils.logger import get_logger
from setup.utils.localization import get_string
from setup import PROJECT_ROOT

# Import from the new UI module
from .ui import interactive_component_selection


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
