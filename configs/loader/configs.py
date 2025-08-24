import yaml
from pathlib import Path
from configs.config import Config


def load_config(environment) -> Config:
    root_dir = Path(__file__).resolve().parent.parent.parent
    config_path = root_dir / "configs" / "config.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if "environment" not in data or environment not in data["environment"]:
        raise ValueError(f"Environment '{environment}' not found in config")

    return Config(**data["environment"][environment])
