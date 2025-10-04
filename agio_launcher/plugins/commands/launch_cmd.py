import click

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
            raise click.BadOptionUsage('app_version', 'app-version/v not set')
        app = app_hub.get_app(app_name, app_version, mode=app_mode)
        ctx = app.get_launch_context()
        if __extra_args__:
            ctx.add_args(*__extra_args__)
        # TODO
            click.secho("Not Implemented", fg='red')
            print('⭐️ Start app:', app)
            print('CMD', ' '.join(ctx.command))
            print('Environments: -------------------')
            for k, v in sorted(app.get_launch_envs().items()):
                print(k, '=', v)
            print('---------------------------------')


