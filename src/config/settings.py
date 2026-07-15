import json
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class AppConfig:
    model_path: str = "assets/models/yolov8n.pt"
    confidence_threshold: float = 0.5
    iou_threshold: float = 0.45
    notifications_enabled: bool = True
    theme: str = "dark"
    save_screenshots: bool = True
    screenshot_dir: str = "data/screenshots"
    database_path: str = "data/database/cheating_alerts.db"
    video_output_fps: int = 30

class ConfigManager:
    _instance = None
    _config_file = Path("assets/default_config.json")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance.config = AppConfig()
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        self._create_directories()
        self.load_config()

    def _create_directories(self) -> None:
        directories = [
            "assets/models",
            self.config.screenshot_dir,
            Path(self.config.database_path).parent,
            "data/videos",
            "data/logs"
        ]
        for dir_path in directories:
            Path(dir_path).mkdir(parents=True, exist_ok=True)

    def load_config(self) -> None:
        if not self._config_file.parent.exists():
            self._config_file.parent.mkdir(parents=True, exist_ok=True)

        if self._config_file.exists():
            try:
                with open(self._config_file, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    for key, value in data.items():
                        if hasattr(self.config, key):
                            setattr(self.config, key, value)
            except Exception:
                pass
        else:
            self.save_config()

    def save_config(self) -> None:
        try:
            with open(self._config_file, "w", encoding="utf-8") as file:
                json.dump(asdict(self.config), file, indent=4)
        except Exception:
            pass

config_manager = ConfigManager()