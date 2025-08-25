from dataclasses import dataclass, field
from pydantic import Field
from pydantic_settings import BaseSettings
from configs.config import Config
from configs.loader.configs import load_config


class EnvSettings(BaseSettings):
    environment: str = Field(default="dev", alias="ENVIRONMENT")


@dataclass
class Settings:
    env_variables: EnvSettings = field(default_factory=EnvSettings)
    config: Config = field(init=False)

    def __post_init__(self):
        self.config = load_config(self.env_variables.environment)
