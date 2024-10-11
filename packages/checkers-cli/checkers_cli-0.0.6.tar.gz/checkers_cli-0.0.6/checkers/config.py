from typing import Optional, Dict, Any
import os
import toml
from pydantic import BaseModel, ValidationError
from .exceptions import ConfigFileNotFoundException, ConfigFileInvalid


class Config(BaseModel):
    dbt_project_dir: str = os.getcwd()
    api_host: str = "https://www.getcheckers.com/api"
    checks: Dict[str, Dict[str, Any]] = dict()

    @property
    def manifest_path(self):
        return os.path.join(self.dbt_project_dir, "target", "manifest.json")

    def dump(self, out):
        with open(out, "w") as fh:
            toml.dump(self.model_dump(), fh)


def load_config(path: Optional[str] = None, **overrides) -> Config:
    if path is None:
        return Config(**overrides)
    elif not os.path.exists(path):
        raise ConfigFileNotFoundException(f"No config file found at {path}")
    else:
        raw_config = toml.load(open(path, "r"))

    raw_config.update(overrides)

    try:
        config = Config(**raw_config)
        return config
    except ValidationError as err:
        raise ConfigFileInvalid(str(err))
