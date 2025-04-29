from typing import Callable

from qtpy.QtWidgets import *

from ..Helpers.TSHSettingsHelper import AbstractSettingsWidget, SettingsItem
from ..SettingsManager import SettingsManager


class OBSSettingsWidget(AbstractSettingsWidget):
    def CreateOtherSettings(self, setting: SettingsItem) -> tuple[QWidget, Callable[..., None]]:
        pass
