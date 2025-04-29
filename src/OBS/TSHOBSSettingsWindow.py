from .OBSSettingsWidget import OBSSettingsWidget
from ..Helpers.TSHSettingsHelper import GenericSettingsWindow, SettingsGroup, SettingsItem


class TSHOBSSettingsWindow(GenericSettingsWindow[OBSSettingsWidget]):
    def __init__(self, parent=None):
        settings: list[SettingsGroup] = [
            SettingsGroup(
                "Websocket Connection",
                OBSSettingsWidget(
                    "obs_auth",
                    [
                        SettingsItem("OBS Host", "settings.obs", "obs_host", "textbox", "localhost"),
                        SettingsItem("OBS Port", "settings.obs", "obs_port", "textbox", "4455"),
                        SettingsItem("OBS Password", "settings.obs", "obs_password", "password", ""),
                    ]
                )
            ),
            SettingsGroup(
                "Websocket Rules",
                OBSSettingsWidget(
                    "obs_rules",
                    [
                        SettingsItem("Add OBS Rule", "settings.obs", "obs_rule", "creator", None)
                    ]
                )
            )
        ]
        super().__init__("OBS Websocket Settings", settings, parent=parent)
