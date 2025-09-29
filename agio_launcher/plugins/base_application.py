from __future__ import annotations

from pathlib import Path

from agio_launcher.application import application
from agio.core.plugins.base_plugin import APlugin
from agio.core.plugins.mixins import BasePluginClass
from agio_launcher.application.exceptions import ApplicationError


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
    bin_path: str = None

    def __str__(self):
        return self.mode_name

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.app_name}.{self.mode_name}>"

    def get_bin_basename(self, app: application.AApplication):
        if not self.bin_path:
            raise ApplicationError('Bin file name not set')
        bin_file_name = self.bin_path.format(version=app.version)
        return bin_file_name

    def get_executable(self, app: application.AApplication) -> str:
        bin_file_name = self.get_bin_basename(app)
        return Path(app.get_install_dir(), bin_file_name).as_posix()

    def get_launch_args(self, app: application.AApplication) -> tuple|list|None:
        """
        Modify args for current mode
        """
        return

    def get_launch_envs(self, app: application.AApplication) -> dict|None:
        """
        Modify envs for current mode
        """
        return

    def get_workdir(self, app: application.AApplication) -> str:
        """
        Modify workdir for current mode
        """
        return app.get_install_dir()

    def on_before_startup(self, app: application.AApplication) -> None:
        pass

    def on_after_startup(self, app: application.AApplication) -> None:
        pass

    def on_after_shutdown(self, app: application.AApplication) -> None:
        pass


