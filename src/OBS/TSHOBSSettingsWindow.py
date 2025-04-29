from qtpy.QtCore import *
from qtpy.QtWidgets import *
from .OBSSettingsWidget import OBSSettingsWidget
from ..TSHHotkeys import TSHHotkeys


class TSHOBSSettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
