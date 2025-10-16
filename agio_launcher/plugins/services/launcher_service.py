import logging
import traceback

from agio.core.plugins.base_service import ServicePlugin, make_action
from agio.core.utils import launch_utils
from agio.tools import qt
from agio_launcher.application.application import AApplication
from agio_launcher.application.tools import get_app_list
from agio_pipe.entities.task import ATask

logger = logging.getLogger(__name__)


class LauncherService(ServicePlugin):
    name = 'launcher'

    @make_action()
    def launch(self, *args, task_id: str, app_name: str, app_version: str, app_mode: str = None, **kwargs):
        try:
            task = ATask(task_id)
        except Exception as e:
            traceback.print_exc()
            qt.show_message_dialog('Task not found', 'Error', 'error')  # todo: replace with emit event
            return
        workspace_id = kwargs.get('workspace_id') or task.project.workspace_id
        if not workspace_id:
            raise ValueError(f'Workspace not set for project {task.project.name}')
        envs = {}
        cmd_args = [
            'launch',
            '--app-name', app_name,
            '--app-version', app_version,
        ]
        if app_mode:
            cmd_args.extend(['--app-mode', app_mode])
        if args:
            cmd_args.append('--')
            cmd_args.extend(args)
        if task_id:
            envs['AGIO_TASK_ID'] = task_id
        launch_utils.exec_agio_command(
            args=cmd_args,
            workspace=workspace_id,
            envs=envs,
            detached=True,
            new_console=True,
        )

    def collect_actions(self):
        # TODO: filter for project using settings
        apps: list[AApplication]  = get_app_list()
        items = []
        action_name = f'{self.name}.{self.launch.__name__}'
        for i, app in enumerate(sorted(apps, key=lambda a: (a.name, a.version))):
            label = f'{app.label} {app.version}'
            if app.mode_label:
                label += f' ({app.mode_label})'
            action_data = {
                # filters
                'action': action_name,
                'menu_name': 'task.launcher',
                'app_name': 'front',
                # action properties
                'name': 'launch',
                'label': label,
                'icon': app.icon,
                'order': i,
                'group': 'Applications',
                'kwargs': {
                    'app_name': app.name,
                    'app_version': app.version,
                    'app_mode': app.mode,
                },
                'args': (),
            }
            items.append(action_data)
        return items
