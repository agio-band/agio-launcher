# launcher
#     list-app
#     add-app
#     delete-app
from pprint import pprint

from agio.core.plugins.base_command import ACommandPlugin, ASubCommand
from agio.core.settings import get_local_settings
from agio.core.utils  import plugin_hub
import click

from agio_launcher.application.application import AApplication


class ListAppCommand(ASubCommand):
    command_name = "ls"
    arguments = [
        click.option('-a', '--as-args', is_flag=True, help='Show as arguments'),
    ]

    def execute(self, as_args: bool):
        local_settings = get_local_settings()
        apps_config = sorted(local_settings.get('agio_launcher.applications'), key=lambda a: (a.name, a.version))
        if not apps_config:
            click.secho('No applications config found', fg='red')
        all_app_plugins = list(plugin_hub.APluginHub.instance().get_plugins_by_type('application'))
        if not all_app_plugins:
            click.secho('No app plugins found', fg='red')
        for app_plg in all_app_plugins:
            conf_list = [x for x in apps_config if x.name == app_plg.app_name]
            for c in conf_list:
                app = AApplication(app_plg, c.version, c)
                if as_args:
                    click.echo('--app-name {} --app-version {} --app-mode {}'.format(app.name, app.version, app.mode))
                else:
                    click.echo(f'{app}, install dir: {c.install_dir or "NOT-SET"}') # TODO make beauty


class AddAppCommand(ASubCommand):
    """
    Add application configuration to local config
    """
    command_name = "add"
    arguments = [
        click.option('-n', '--app-name',  required=True, help='Application name'),
        click.option('-v', '--app-version', required=True, help='Application version'),
        click.option('-i', '--installation-dir', required=True,
                     type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True),
                     help='Installation directory'),
    ]

    def execute(self, app_name, app_version, installation_dir):
        print('Adding app: "{}" v{}'.format(app_name, app_version))


class DelAppCommand(ASubCommand):
    """
    Add application configuration to local config
    """
    command_name = "del"
    arguments = [
        click.option('-n', '--app-name',  required=True, help='Application name'),
        click.option('-v', '--app-version', required=True, help='Application version'),
    ]

    def execute(self, app_name, app_version, installation_dir):
        print('Delete app: "{}" v{}'.format(app_name, app_version))


class LauncherToolsCommand(ACommandPlugin):
    name = "launcher_app_cmd"
    command_name = 'apps'
    subcommands = [ListAppCommand, AddAppCommand, DelAppCommand]


