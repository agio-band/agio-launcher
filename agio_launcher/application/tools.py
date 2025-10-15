import logging

from agio.core.settings import get_local_settings
from agio.core.utils  import plugin_hub
from agio_launcher.application.application import AApplication


logger = logging.getLogger(__name__)


def get_app_list():
    local_settings = get_local_settings()
    apps_config = sorted(local_settings.get('agio_launcher.applications'), key=lambda a: (a.name, a.version))
    if not apps_config:
        return
    all_app_plugins = list(plugin_hub.APluginHub.instance().get_plugins_by_type('application'))
    if not all_app_plugins:
        logger.warning('No plugins found for any applications')
        return
    for app_plg in all_app_plugins:
        conf_list = [x for x in apps_config if x.name == app_plg.app_name]
        for c in conf_list:
            yield AApplication(app_plg, c.version, c)
