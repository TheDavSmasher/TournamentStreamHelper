from qtpy.QtWidgets import *
from ..SettingsManager import SettingsManager
import textwrap


class OBSSettingsWidget(QWidget):
    def __init__(self, settingsBase="", settings=[]):
        super().__init__()

        self.settingsBase = settingsBase
