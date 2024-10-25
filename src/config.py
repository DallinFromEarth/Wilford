import json
import os
from pathlib import Path
from typing import Dict, Any


class ConfigurationError(Exception):
    pass

class Config:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Only initialize once
        if not Config._initialized:
            self.app_name = "wilford"
            self.config_dir = self._get_config_dir()
            self.config_file = self.config_dir / "config.json"
            self._config: Dict[str, Any] = {}
            self.load()
            Config._initialized = True

    @classmethod
    def get_instance(cls) -> 'Config':
        if cls._instance is None:
            cls._instance = Config()
        return cls._instance

    def get(self, key: str) -> Any:
        return self._config.get(key)

    def set(self, key: str, value: str):
        self._config[key] = value

    def _get_config_dir(self) -> Path:
        if os.name == 'nt':  # Windows
            base_dir = Path(os.path.expanduser('~')) / 'AppData' / 'Roaming'
        else:  # Unix-like
            base_dir = Path(os.path.expanduser('~')) / '.config'

        config_dir = base_dir / self.app_name
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir

    def load(self) -> None:
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    stored_config = json.load(f)
                    # Start with defaults
                    self.set_defaults()
                    # Update with stored values
                    self._config.update(stored_config)
            else:
                self.set_defaults()
                self.save()
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading config: {e}")
            print("Falling back to default configuration")
            self.set_defaults()
            self.save()

    def save(self) -> None:
        """Save current configuration to disk."""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2)
        except IOError as e:
            print(f"Error saving config: {e}")
            # Don't raise error, just notify user

    def set_defaults(self) -> None:
        """Set default configuration values."""
        self._config = {
            'downloads_dir': str(Path.home() / "Downloads" / "Wilford"),
            'skip_sustainings': True,
            'file_naming_convention': "speaker-date-title",
            'confirm_download': True,
            'confirm_load_links': True,
        }

    def to_string(self):
        config_string = ""
        for key in self._config.keys():
            config_string += f"{key} = {self._config[key]}\n"
        return config_string

    def keys(self):
        return self._config.keys()


def get_config() -> Config:
    """Get the global config instance."""
    return Config.get_instance()