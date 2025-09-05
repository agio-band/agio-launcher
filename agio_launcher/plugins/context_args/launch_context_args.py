from typing import Callable
import click

from agio.core.pkg import AWorkspaceManager
from agio.core.plugins.base_context_args import ContextArgsPlugin
from agio_launcher.application import app_hub


class LauncherContextArgs(ContextArgsPlugin):
    name = "launcher_args"
    args_prefix = "launcher"

    def get_args(self) -> list[Callable]:
        return [
            click.option("--app_name", default=None, help="App Name"),
            click.option("--app_version", default=None, help="App Version"),
            click.option("--app_mode", default='default', help="App Mode"),
            ]

    def execute(self,
                workspace: AWorkspaceManager,
                app_name: str = None, app_version: str = None, app_mode: str = None,
                **kwargs):
        if app_name:
            if not app_version:
                raise click.BadOptionUsage('app_version', 'app_version not set')
            app = app_hub.get_app(app_name, app_version)
            print('⭐️ Use app context:', app)


