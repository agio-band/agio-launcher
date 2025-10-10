import logging

from agio.core.plugins.base_service import ServicePlugin, make_action
from agio.core.utils import launch_utils

logger = logging.getLogger(__name__)


class LauncherService(ServicePlugin):
    name = 'launcher'

    @make_action(menu_name='task.launcher', app_name='front')
    def launch(self, *args, task_id: str, app_name: str, app_version: str, app_mode: str = None, **kwargs):
        workspace_id = kwargs.get('workspace_id') # or ATask(task_id).project.workspace_id
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
        )

