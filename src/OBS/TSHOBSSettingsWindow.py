from .TSHOBSWebsocketRulesWidget import OBSWebsocketRulesWidget
from ..Helpers.TSHSettingsHelper import GenericSettingsWindow, SettingsGroup, SettingsItem, SettingsWidget


class TSHOBSSettingsWindow(GenericSettingsWindow):
    def __init__(self, parent=None):
        settings: list[SettingsGroup] = [
            SettingsGroup(
                "Websocket Connection",
                SettingsWidget(
                    "obs_auth",
                    [
                        SettingsItem("Enable OBS Websockets", "settings.obs", "obs_enable", "checkbox", True),
                        SettingsItem("OBS Host", "settings.obs", "obs_host", "textbox", "localhost"),
                        SettingsItem("OBS Port", "settings.obs", "obs_port", "textbox", "4455"),
                        SettingsItem("OBS Password", "settings.obs", "obs_password", "password", ""),
                        SettingsItem("OBS Auto-reconnect Timer", "settings.obs", "obs_auto_reconnect_timer", "integer", 0),
                    ]
                )
            ),
            SettingsGroup(
                "Websocket Rules",
                OBSWebsocketRulesWidget(),
            )
        ]
        super().__init__("OBS Websocket Settings", settings, parent=parent)
