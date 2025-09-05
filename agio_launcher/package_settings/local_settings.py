from agio.core.settings.package_settings import APackageSettings
from pydantic import BaseModel


class Application(BaseModel):
    name: str
    version: str
    install_dir: str


class LauncherSettings(APackageSettings):
    applications: list[Application] = ()