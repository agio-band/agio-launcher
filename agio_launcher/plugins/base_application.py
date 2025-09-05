from __future__ import annotations

from agio_launcher.application import application
from agio.core.plugins.base_plugin import APlugin
from agio.core.plugins.mixins import BasePluginClass


class ApplicationPlugin(BasePluginClass, APlugin):
    plugin_type = 'application'
    app_group: str = None
    app_name: str = None
    icon: str = None
    label: str = None
    required_attrs = {'app_group', 'app_name'}

    def get_label(self):
        return self.label or self.app_name.title()

    def get_launch_envs(self):
        ...

    def get_user_prefs_dir(self):
        ...

    def get_install_dir(self):
        ...

    def install_required_libs(self):
        ...


class ApplicationModePlugin(BasePluginClass, APlugin):
    plugin_type = 'application_mode'

    app_name: str = None
    mode_name = None
    icon: str = None
    required_attrs = {'app_name', 'mode_name'}

    def get_executable(self, install_dir: str) -> str:
        raise NotImplementedError

    def get_args(self, default_args: list = None) -> tuple|list:
        """
        Modify args for current mode
        """
        return default_args

    def get_launch_envs(self, default_envs: dict = None) -> dict:
        """
        Modify envs for current mode
        """
        return default_envs

    def get_workdir(self, default_workdir: str) -> str:
        """
        Modify workdir for current mode
        """
        return default_workdir

    def on_before_startup(self, app: application.AApplication) -> None:
        pass

    def on_after_startup(self, app: application.AApplication) -> None:
        pass

    def on_after_shutdown(self, app: application.AApplication) -> None:
        pass


