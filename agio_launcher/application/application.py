from __future__ import annotations
import os
from typing import Iterable

from agio_launcher.plugins import base_application


class AApplication:
    def __init__(self,
                 app_plugin: base_application.ApplicationPlugin,
                 app_mode_plugins: list[base_application.ApplicationModePlugin],
                 version: str,
                 config: dict[str, str],
                 ) -> None:
        self._app_plugin = app_plugin
        self._app_mode_plugins = {m.name for m in app_mode_plugins}
        self._version = version
        self._config = config
        self._envs = {}
        self._args = []

    def __str__(self):
        return f'Application({self.label} v{self._version})'

    def __repr__(self):
        return f"<Application('{self.name}', '{self._version}')"

    @property
    def label(self):
        return self._app_plugin.get_label()

    @property
    def name(self):
        return self._app_plugin.app_name

    @property
    def version(self):
        return self._version

    def is_configured(self) -> bool:
        ...

    @property
    def config(self) -> dict[str, str]:
        return self._config.copy()

    def get_envs(self) -> dict:
        return self._envs.copy()

    def set_envs(self, envs: dict[str, str]):
        if not isinstance(self._envs, dict):
            raise TypeError("envs must be a dict")
        self._envs = {str(k): str(v) for k, v in envs.items()}

    def add_env(self, key: str, value: str):
        self._envs[str(key).upper()] = str(value)

    def append_path_env(self, key: str, value: str):
        path_list = self._get_path_env(key)
        if path_list is not None:
            path_list.append(value)
        self._set_path_env(key, path_list)

    def prepend_path_env(self, key: str, value: str):
        path_list = self._get_path_env(key)
        if path_list is not None:
            path_list.insert(0, value)
        self._set_path_env(key, path_list)

    def _get_path_env(self, key: str):
        current = self._envs.get(str(key).upper())
        if current is None:
            current = []
        else:
            current = current.split(os.pathsep)
        return current

    def _set_path_env(self, key: str, value: list[str]):
        self._envs[str(key).upper()] = os.pathsep.join(value)

    @property
    def workdir(self):
        return self._workdir

    def set_workdir(self, workdir):
        if not os.path.exists(workdir):
            raise FileNotFoundError(workdir)
        self._workdir = workdir

    def start(
            self,
            args: Iterable = None,
            envs: dict = None,
            mode: str = None,
            workdir: str = None,
            **kwargs):
        pass

    def stop(self, **kwargs):
        pass

