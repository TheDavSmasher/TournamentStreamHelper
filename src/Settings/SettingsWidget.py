from qtpy.QtWidgets import *

from ..Helpers.TSHSettingsHelper import AbstractSettingsWidget
from ..TSHHotkeys import TSHHotkeys
from ..SettingsManager import SettingsManager
import textwrap


class SettingsWidget(AbstractSettingsWidget):


    def AddSetting(self, name: str, setting: str, type: str, defaultValue, callback=lambda: None, tooltip=None):
        lastRow = self.layout().rowCount()

        self.layout().addWidget(QLabel(name), lastRow, 0)

        resetButton = QPushButton(
            QApplication.translate("settings", "Default"))

        if type == "checkbox":
            settingWidget = QCheckBox()
            settingWidget.setChecked(SettingsManager.Get(
                self.settingsBase+"."+setting, defaultValue))
            settingWidget.stateChanged.connect(
                lambda val=None: SettingsManager.Set(self.settingsBase+"."+setting, settingWidget.isChecked()))
            resetButton.clicked.connect(
                lambda bt=None, settingWidget=settingWidget:
                settingWidget.setChecked(defaultValue)
            )
        elif type == "hotkey":
            settingWidget = QKeySequenceEdit()
            settingWidget.keySequenceChanged.connect(
                lambda keySequence, settingWidget=settingWidget:
                settingWidget.setKeySequence(keySequence.toString().split(",")[
                    0]) if keySequence.count() > 0 else None
            )
            settingWidget.setKeySequence(SettingsManager.Get(
                self.settingsBase+"."+setting, defaultValue))
            settingWidget.keySequenceChanged.connect(
                lambda sequence=None, setting=setting: [
                    SettingsManager.Set(
                        self.settingsBase+"."+setting, sequence.toString()),
                    callback()
                ]
            )
            resetButton.clicked.connect(
                lambda bt=None, setting=setting, settingWidget=settingWidget: [
                    settingWidget.setKeySequence(defaultValue),
                    callback()
                ]
            )
        elif type == "textbox" or type == "password":
            settingWidget = QLineEdit()
            if type == "password":
                settingWidget.setEchoMode(QLineEdit.Password)
            settingWidget.textChanged.connect(
                lambda val=None: SettingsManager.Set(self.settingsBase+"."+setting, settingWidget.text()))
            settingWidget.setText(SettingsManager.Get(
                self.settingsBase+"."+setting, defaultValue))
            resetButton.clicked.connect(
                lambda bt=None, setting=setting, settingWidget=settingWidget: [
                    settingWidget.setText(defaultValue),
                    callback()
                ]
            )
        
        if tooltip:
            settingWidget.setToolTip('\n'.join(textwrap.wrap(tooltip, 40)))

        self.layout().addWidget(settingWidget, lastRow, 1)
        self.layout().addWidget(resetButton, lastRow, 2)
