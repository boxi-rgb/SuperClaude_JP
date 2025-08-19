import pytest
from pathlib import Path
from unittest.mock import MagicMock

from setup.core.registry import ComponentRegistry
from setup.base.component import Component

# --- Mock Component Classes (now with all abstract methods implemented) ---
class MockComponentA(Component):
    def get_metadata(self):
        return {"name": "component_a", "description": "Mock A", "version": "1.0"}
    def get_dependencies(self):
        return []
    def _install(self, config): return True
    def _post_install(self): return True
    def uninstall(self): return True
    def _get_source_dir(self): return Path("/fake/source")

class MockComponentB(Component):
    def get_metadata(self):
        return {"name": "component_b", "description": "Mock B", "version": "1.0"}
    def get_dependencies(self):
        return ["component_a"]
    def _install(self, config): return True
    def _post_install(self): return True
    def uninstall(self): return True
    def _get_source_dir(self): return Path("/fake/source")

class MockComponentC(Component):
    def get_metadata(self):
        return {"name": "component_c", "version": "1.0"}
    def get_dependencies(self):
        return ["component_d"]
    def _install(self, config): return True
    def _post_install(self): return True
    def uninstall(self): return True
    def _get_source_dir(self): return Path("/fake/source")

class MockComponentD(Component):
    def get_metadata(self):
        return {"name": "component_d", "version": "1.0"}
    def get_dependencies(self):
        return ["component_c"] # Circular dependency
    def _install(self, config): return True
    def _post_install(self): return True
    def uninstall(self): return True
    def _get_source_dir(self): return Path("/fake/source")

# --- Tests ---

def test_discover_components(mocker):
    """Test component discovery using mocks."""
    mocker.patch.object(Path, 'glob', return_value=[
        Path("mock_a.py"),
        Path("mock_b.py"),
    ])
    mocker.patch.object(Path, 'exists', return_value=True)

    def mock_import_module(name):
        mock_module = MagicMock()
        if name.endswith("mock_a"):
            mock_module.MockComponentA = MockComponentA
        elif name.endswith("mock_b"):
            mock_module.MockComponentB = MockComponentB
        return mock_module

    mocker.patch('importlib.import_module', side_effect=mock_import_module)

    registry = ComponentRegistry(Path("/fake/dir"))
    registry.discover_components()

    discovered = registry.list_components()
    assert sorted(discovered) == ["component_a", "component_b"]

def test_resolve_dependencies(mocker):
    """Test dependency resolution using mocks."""
    mocker.patch.object(Path, 'glob', return_value=[Path("mock_a.py"), Path("mock_b.py")])
    mocker.patch.object(Path, 'exists', return_value=True)

    def mock_import_module(name):
        mock_module = MagicMock()
        if name.endswith("mock_a"):
            mock_module.MockComponentA = MockComponentA
        elif name.endswith("mock_b"):
            mock_module.MockComponentB = MockComponentB
        return mock_module
    mocker.patch('importlib.import_module', side_effect=mock_import_module)

    registry = ComponentRegistry(Path("/fake/dir"))

    order = registry.resolve_dependencies(["component_b"])
    assert order == ["component_a", "component_b"]

def test_circular_dependency(mocker):
    """Test circular dependency detection using mocks."""
    mocker.patch.object(Path, 'glob', return_value=[Path("mock_c.py"), Path("mock_d.py")])
    mocker.patch.object(Path, 'exists', return_value=True)

    def mock_import_module(name):
        mock_module = MagicMock()
        if name.endswith("mock_c"):
            mock_module.MockComponentC = MockComponentC
        elif name.endswith("mock_d"):
            mock_module.MockComponentD = MockComponentD
        return mock_module
    mocker.patch('importlib.import_module', side_effect=mock_import_module)

    registry = ComponentRegistry(Path("/fake/dir"))
    with pytest.raises(ValueError, match="Circular dependency detected"):
        registry.resolve_dependencies(["component_c"])
