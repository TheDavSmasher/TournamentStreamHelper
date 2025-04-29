from qtpy.QtWidgets import *
from .OBSSettingsWidget import OBSSettingsWidget
from ..Helpers.TSHSettingsHelper import GenericSettingsWindow, SettingsGroup


class TSHOBSSettingsWindow(GenericSettingsWindow[OBSSettingsWidget]):
    def __init__(self, parent=None):
        settings: list[SettingsGroup] = []
        super().__init__("OBS Websocket Settings", settings, parent=parent)
        self.selection_list = QListWidget()
        self.settings_stack = QStackedWidget()
