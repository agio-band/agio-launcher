from agio.core.utils import plugin_hub
from agio.core.settings import get_local_settings
from agio.core.utils.singleton import Singleton
from .application import AApplication
from .exceptions import ApplicationNotFoundError
from ..plugins import base_application_plugin


class ApplicationHub(metaclass=Singleton):
    def __init__(self):
        local_settings = get_local_settings()
        self.apps_config = local_settings.get('agio_launcher.applications')

    def get_app(self, name: str, version: str, mode: str = None) -> AApplication:
        plugin = self.find_plugin(name, mode)
        if not plugin:
            raise ApplicationNotFoundError(f"Plugin '{name}/{mode}' not found")
        app_config = self.get_app_settings(name, version) or {} # TODO error if empty
        return AApplication(plugin, version, app_config)

    def get_app_settings(self, name: str, version: str) -> dict:
        for app in self.apps_config:
            if app.name == name and app.version == version:
                return app.model_dump()
        raise Exception('Application settings for {} v{} not found'.format(name, version))

    @classmethod
    def find_plugin(cls, name: str, mode: str = None) -> base_application_plugin.ApplicationPlugin:
        for plg in cls.find_app_plugins(name):
            if plg.app_mode == mode:
                return plg

    @classmethod
    def find_app_plugins(cls, name: str):
        hub = plugin_hub.APluginHub.instance()
        for app_plugin in hub.get_plugins_by_type('application'):
            if app_plugin.app_name == name:
                yield app_plugin
