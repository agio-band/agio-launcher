from __future__ import annotations

from pathlib import Path

from agio.core.utils.launch_utils import LaunchContext
from agio_launcher.application.exceptions import ApplicationError
from agio_launcher.plugins import base_application


class AApplication:
    def __init__(self,
                 app_plugin: base_application.ApplicationPlugin,
                 app_mode_plugins: list[base_application.ApplicationModePlugin],
                 version: str,
                 config: dict[str, str],
                 mode: str = None
                 ) -> None:
        self._app_plugin = app_plugin
        self._app_mode_plugins = {m.mode_name: m for m in app_mode_plugins}
        self._version = version
        self._config = config
        self._current_mode = None
        self.set_mode(mode or 'default')

    def __str__(self):
        return f'{self.label} v{self._version} ({self.mode_name})'

    def __repr__(self):
        return f"<Application('{self.name}', '{self._version}', mode={self.mode_name})"

    @property
    def mode(self):
        return self._current_mode

    @property
    def mode_name(self):
        return self._current_mode.mode_name

    def set_mode(self, mode: str):
        if mode not in self._app_mode_plugins:
            raise ApplicationError(f'Invalid mode {mode!r} for app {self.name}')
        self._current_mode = self._app_mode_plugins[mode]

    def get_launch_context(self) -> LaunchContext:
        executable = self.get_executable()
        if not executable:
            raise ApplicationError(f'{self.name} must define a executable')
        if not Path(executable).is_file():
            raise ApplicationError(f'Executable {self.name}/{executable} is not a file or not exists')
        ctx = LaunchContext(
            executable,
            self.mode.get_launch_args(self),
            env=self.mode.get_launch_envs(self),
        )
        return ctx

    @property
    def label(self):
        return self._app_plugin.get_label()

    @property
    def name(self):
        return self._app_plugin.app_name

    @property
    def version(self):
        return self._version

    def get_mode_plugin(self, mode_name: str):
        if mode_name not in self._app_mode_plugins:
            raise ApplicationError(f'Invalid mode {mode_name!r} for app {self.name}')
        return self._app_mode_plugins[mode_name]

    @property
    def config(self) -> dict[str, str]:
        return self._config.copy()

    def get_executable(self):
        return self.mode.get_executable(self)

    def get_launch_envs(self):
        envs = self.config.get('env')
        return envs

    def get_launch_args(self):
        default_args = self.config.get('arguments') or []
        return default_args

    def get_install_dir(self):
        path = self.config.get('install_dir')
        if not path:
            raise ApplicationError(f'{self.name} v{self.version} must define an install dir')
        return path

