from agio.core.domains import AWorkspace
from agio.core.events import subscribe
from agio.core.pkg import AWorkspaceManager
from agio_launcher.application.application import AApplication


@subscribe('agio_launcher.start_app.app_created', raise_error=True)
def create_app_workspace(event, payload):
    app: AApplication = payload['app']
    # create workspace libs dir
    ws = AWorkspace.current()
    if not ws:
        raise Exception("No workspace defined")
    suffix = f"{app.name}-{app.version}"
    # create custom workspace
    ws_man = AWorkspaceManager.from_workspace(ws)
    ws_man.set_suffix(suffix)
    ws_man.install_or_update_if_needed()
    app.ctx.append_env_path(ws_man.get_site_packages_path())



