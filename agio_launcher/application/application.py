from __future__ import annotations

from functools import cached_property
from pathlib import Path

from agio.core.utils.launch_utils import LaunchContext
from agio_launcher.application.exceptions import ApplicationError
from agio_launcher.plugins import base_application


class AApplication:
    def __init__(self,
                 app_plugin: base_application.ApplicationPlugin,
                 version: str,
                 config: dict[str, str],
                 ) -> None:
        self._app_plugin = app_plugin
        self._version = version
        self._config = config

    def __str__(self):
        return f'{self.label} v{self._version} ({self._app_plugin.app_mode})'

    def __repr__(self):
        return f"<Application('{self.name}', '{self._version}', mode={self._app_plugin.app_mode})"

    def get_launch_context(self) -> LaunchContext:
        executable = self.get_executable()
        if not executable:
            raise ApplicationError(f'{self.name} must define a executable')
        if not Path(executable).is_file():
            raise ApplicationError(f'Executable {self.name}/{executable} is not a file or not exists')
        ctx = LaunchContext(
            executable,
            args=self.get_launch_args(),
            env=self.get_launch_envs(),
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

    @property
    def mode(self):
        return self._app_plugin.app_mode

    @cached_property
    def config(self) -> dict[str, str]:
        return self._config.copy()

    def get_executable(self):
        return self._app_plugin.get_executable(self)

    def get_launch_envs(self):
        envs = self.config.get('env')
        return self._app_plugin.get_launch_envs(self, envs)

    def get_launch_args(self):
        default_args = self.config.get('arguments') or []
        return self._app_plugin.get_launch_args(self, default_args)

    def get_install_dir(self):
        path = self.config.get('install_dir')
        if not path:
            raise ApplicationError(f'{self.name} v{self.version} config must define an install dir')
        return path

