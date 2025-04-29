from qtpy.QtWidgets import *
from .OBSSettingsWidget import OBSSettingsWidget
from ..Helpers.TSHSettingsHelper import GenericSettingsWindow, SettingsGroup


class TSHOBSSettingsWindow(GenericSettingsWindow[OBSSettingsWidget]):
    def __init__(self, parent=None):
        settings: list[SettingsGroup] = [
            SettingsGroup(
                "Websocket Connection",
                OBSSettingsWidget(
                    "obs_auth",
                    []
                )
            )
        ]
        super().__init__("OBS Websocket Settings", settings, parent=parent)
