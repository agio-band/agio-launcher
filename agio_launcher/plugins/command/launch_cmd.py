from typing import Callable
import click

from agio.core.pkg import AWorkspaceManager
from agio.core.plugins.base_command import ACommandPlugin
from agio_launcher.application import app_hub


class LauncherCommand(ACommandPlugin):
    name = 'launch_cmd'
    command_name = "launch"
    arguments = [
        click.option("-a", "--app-name", help="App Name"),
        click.option("-v", "--version", help="App Version"),
        click.option("-m", "--mode", default='default', help="App Mode"),
    ]

    def execute(self,
                app_name: str = None,
                version: str = None,
                mode: str = None,
                **kwargs):
        if not app_name:
            raise click.BadOptionUsage('app-name', 'app-name not set')
        if not version:
            raise click.BadOptionUsage('version', 'version not set')
        app = app_hub.get_app(app_name, version, mode=mode)
        print('⭐️ Start app:', app)
        ctx = app.get_launch_context()
        print('CMD', ' '.join(ctx.command))


