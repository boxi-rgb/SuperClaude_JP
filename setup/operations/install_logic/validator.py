"""
System validation logic for the installation operation.
"""

from typing import List

from setup.core.validator import Validator
from setup.managers.config_manager import ConfigManager
from setup.utils.logger import get_logger
from setup.utils.localization import get_string
from setup.utils.ui import Colors
from setup import PROJECT_ROOT


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
