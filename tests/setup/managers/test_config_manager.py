import pytest
import json
from pathlib import Path

try:
    from setup.managers.config_manager import ConfigManager, ValidationError
except ImportError:
    pass

# --- Mock Data ---

MOCK_FEATURES = {
    "components": {
        "core": {
            "name": "core", "version": "1.0", "description": "Core files",
            "category": "core", "enabled": True, "required_tools": ["git"]
        },
        "commands": {
            "name": "commands", "version": "1.0", "description": "Slash commands",
            "category": "commands", "enabled": True, "dependencies": ["core"]
        },
        "disabled_feature": {
            "name": "disabled_feature", "version": "1.0", "description": "A disabled feature",
            "category": "extra", "enabled": False
        }
    }
}

MOCK_REQUIREMENTS = {
    "python": {"min_version": "3.8"},
    "disk_space_mb": 100,
    "external_tools": {
        "git": {"command": "git --version"}
    }
}

MOCK_PROFILE = {
    "name": "Test Profile",
    "components": ["core", "commands"]
}

# --- Fixtures ---

@pytest.fixture
def mock_config_dir(tmp_path: Path) -> Path:
    """Creates a temporary config directory with mock files."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()

    (config_dir / "features.json").write_text(json.dumps(MOCK_FEATURES))
    (config_dir / "requirements.json").write_text(json.dumps(MOCK_REQUIREMENTS))

    return config_dir

@pytest.fixture
def mock_profile_path(tmp_path: Path) -> Path:
    """Creates a temporary profile file."""
    profile_path = tmp_path / "profiles"
    profile_path.mkdir()
    profile_file = profile_path / "test_profile.json"
    profile_file.write_text(json.dumps(MOCK_PROFILE))
    return profile_file

# --- Tests ---

def test_load_features_success(mock_config_dir: Path):
    manager = ConfigManager(mock_config_dir)
    features = manager.load_features()
    assert features == MOCK_FEATURES

def test_load_requirements_success(mock_config_dir: Path):
    manager = ConfigManager(mock_config_dir)
    reqs = manager.load_requirements()
    assert reqs == MOCK_REQUIREMENTS

def test_load_profile_success(mock_config_dir: Path, mock_profile_path: Path):
    manager = ConfigManager(mock_config_dir)
    profile = manager.load_profile(mock_profile_path)
    assert profile == MOCK_PROFILE

def test_get_enabled_components(mock_config_dir: Path):
    manager = ConfigManager(mock_config_dir)
    enabled = manager.get_enabled_components()
    assert sorted(enabled) == ["commands", "core"]

def test_get_requirements_for_components(mock_config_dir: Path):
    manager = ConfigManager(mock_config_dir)
    reqs = manager.get_requirements_for_components(["core"])
    assert "git" in reqs["external_tools"]

    reqs = manager.get_requirements_for_components(["commands"])
    assert "git" not in reqs.get("external_tools", {})

def test_caching_behavior(mock_config_dir: Path, mocker):
    manager = ConfigManager(mock_config_dir)
    json_load_spy = mocker.spy(json, 'load')

    manager.load_features()
    manager.load_features()

    assert json_load_spy.call_count == 1

    manager.clear_cache()
    manager.load_features()
    assert json_load_spy.call_count == 2

def test_file_not_found_error(tmp_path: Path):
    manager = ConfigManager(tmp_path)

    with pytest.raises(FileNotFoundError):
        manager.load_features()

    with pytest.raises(FileNotFoundError):
        manager.load_requirements()

    with pytest.raises(FileNotFoundError):
        manager.load_profile(tmp_path / "nonexistent.json")

def test_invalid_json_error(mock_config_dir: Path):
    (mock_config_dir / "features.json").write_text("{ not_json }")

    manager = ConfigManager(mock_config_dir)
    with pytest.raises(ValidationError, match="Invalid JSON in"):
        manager.load_features()
