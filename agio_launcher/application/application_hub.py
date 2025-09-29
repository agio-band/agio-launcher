from agio.core.utils import plugin_hub
from agio.core.settings import get_local_settings
from .application import AApplication


class ApplicationHub:
    def __init__(self):
        local_settings = get_local_settings()
        self.apps_config = local_settings.get('agio_launcher.applications')

    def get_app_settings(self, name, version):
        for app in self.apps_config:
            if app.name == name and app.version == version:
                return app.model_dump()
        raise Exception('Application settings for {} v{} not found'.format(name, version))

    def get_app(self, name: str, version: str, mode: str = None) -> AApplication:
        plugin, modes = self._find_plugins(name)
        app_config = self.get_app_settings(name, version) or {} # TODO error if empty
        return AApplication(plugin, modes, version, app_config, mode)

    def get_app_list(self):
        ...

    def set_app_install_dir(self, app_name: str, version: str):
        ...

    def add_app_config(self, app_name, app_version: str):
        ...


    @classmethod
    def _find_plugins(cls, name: str):
        hub = plugin_hub.APluginHub.instance()
        app_plugin = None
        for app_plugin in hub.get_plugins_by_type('application'):
            if app_plugin.name == name:
                break
        if not app_plugin:
            raise RuntimeError(f"Application plugin '{name}' not found")
        mode_plugins = []
        for mode_plugin in hub.get_plugins_by_type('application_mode'):
            if mode_plugin.app_name == name and mode_plugin.name:
                mode_plugins.append(mode_plugin)
        if not mode_plugins:
            raise RuntimeError(f"Application mods for app '{name}' not found")
        return app_plugin, mode_plugins