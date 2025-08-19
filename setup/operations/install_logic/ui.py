"""
UI-related functions for the installation operation.
"""

from pathlib import Path
from typing import List, Optional

from setup.core.registry import ComponentRegistry
from setup.managers.config_manager import ConfigManager
from setup.core.validator import Validator
from setup.utils.ui import Menu, Colors, format_size
from setup.utils.logger import get_logger
from setup.utils.localization import get_string
from setup import PROJECT_ROOT


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
