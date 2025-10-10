import click

from agio.core.events import emit
from agio.core.plugins.base_command import ACommandPlugin
from agio_launcher.application import app_hub


class LauncherCommand(ACommandPlugin):
    name = 'launch_cmd'
    command_name = "launch"
    arguments = [
        click.option("-n", "--app-name", help="App Name"),
        click.option("-v", "--app-version", help="App Version"),
        click.option("-m", "--app-mode", default='default', help="App Mode"),
    ]
    allow_extra_args = True

    def execute(self,
                app_name: str,
                app_version: str,
                app_mode: str = None,
                __extra_args__: list = None,
                **kwargs):
        if not app_name:
            raise click.BadOptionUsage('app-name', 'app-name not set')
        if not app_version:
            raise click.BadOptionUsage('app_version', 'app-version not set')
        return self.start_app(app_name, app_version, app_mode, __extra_args__, **kwargs)

    def start_app(self, app_name, app_version, app_mode, args, **kwargs):
        app = app_hub.get_app(app_name, app_version, mode=app_mode)
        emit('agio_launcher.start_app.app_created', payload={'app': app})
        # apply default args and envs
        if args:
            app.ctx.add_args(*args)
        # ready to start
        emit('agio_launcher.start_app.before_start', payload={'app': app})
        # starting...
        pid = app.start()
        # app started
        emit('agio_launcher.start_app.after_started', payload={'app': app, 'pid': pid})



