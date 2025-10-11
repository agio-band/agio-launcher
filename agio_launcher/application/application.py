from __future__ import annotations

from functools import cached_property
from pathlib import Path

from pydantic import BaseModel

from agio.core.events import emit
from agio.core.utils.launch_utils import LaunchContext
from agio.core.utils.process_utils import start_process
from agio_launcher.application.exceptions import ApplicationError, ApplicationNotFoundError
from agio_launcher.plugins import base_application_plugin


class AApplication:
    """Wrapper class for any app plugin"""
    default_python_version = None

    def __init__(self,
                 app_plugin: base_application_plugin.ApplicationPlugin,
                 version: str,
                 config: dict[str, str],
                 ) -> None:
        self._app_plugin = app_plugin
        self._version = version
        if isinstance(config, BaseModel):
            config = config.model_dump()
        self._config = config
        self.ctx = self._create_launch_context()

    def __str__(self):
        return f'{self.label} v{self._version} ({self._app_plugin.app_mode})'

    def __repr__(self):
        return f"<Application('{self.name}', '{self._version}', mode={self._app_plugin.app_mode})"

    def _create_launch_context(self) -> LaunchContext:
        executable = self.get_executable()
        if not executable:
            raise ApplicationError(f'{self.name} must define a executable')
        if not Path(executable).is_file():
            raise ApplicationError(f'Executable {self.name}/{executable} is not a file or not exists')
        ctx = LaunchContext(
            executable,
            args=self.get_default_launch_args(),
            env=self.get_default_launch_envs(),
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

    def get_python_version(self):
        from agio_launcher.application import app_hub

        # from config
        version = self.config.get('python_version')
        if not version:
            try:
                py_app = app_hub.get_app(self.name, self.version, mode='python')
                cmd = [py_app.get_executable(), '-V']
                version = start_process(cmd, get_output=True, new_console=False).split()[-1]
                return version
            except ApplicationNotFoundError:
                return self.default_python_version

    def get_default_launch_envs(self):
        config_envs = self._config.get('env') or {}
        plugin_envs = self._app_plugin.get_launch_envs(self, config_envs)
        app_envs = dict(
            **config_envs,
            **(plugin_envs or {}),
            AGIO_APP_NAME=self.name,
            AGIO_APP_VERSION=self.version,
            AGIO_APP_MODE=self.mode,
            AGIO_APP_EXECUTABLE=self.get_executable(),
        )
        return app_envs

    def get_default_launch_args(self):
        default_args = self.config.get('arguments') or []
        return self._app_plugin.get_launch_args(self, default_args)

    def get_install_dir(self):
        path = self.config.get('install_dir')
        if not path:
            raise ApplicationError(f'{self.name} v{self.version} config must define an install dir')
        return path

    def before_start(self):
        pass

    def start(self, **kwargs):
        """
        PID equal None is app is started as detached
        """
        import click

        ### DEBUG INFO ###########################################################
        click.secho("Not Implemented", fg='red')
        print('⭐️ Start app:', self)
        print('CMD:', end=' ')
        click.secho(' '.join(self.ctx.command), fg='green')
        envs = self.get_default_launch_envs()
        if envs:
            click.secho('=== App Environments: ===================', fg='yellow')
            for k, v in sorted(envs.items()):
                print(f"{k}={v}")
        click.secho('=========================================', fg='yellow')

        ##########################################################################

        emit('agio_launcher.application.before_start', payload={'app': self})
        self._app_plugin.on_before_startup(self)
        start_process(self.ctx.command, env=self.ctx.envs, **kwargs)
        self._app_plugin.on_after_startup(self)
