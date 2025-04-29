import textwrap
from dataclasses import dataclass
from typing import Any, Callable

from qtpy.QtCore import *
from qtpy.QtWidgets import *

from ..SettingsManager import SettingsManager


@dataclass
class SettingsItem:
    label: str
    context: str
    key: str
    settingType: str
    defaultValue: Any
    callback: Callable[[], None] = lambda: None
    tooltip: str = None


class SettingsWidget(QWidget):
    def __init__(self, settingsBase="", settings: list[SettingsItem] = None):
        super().__init__()

        if settings is None:
            settings = []

        self.settingsBase = settingsBase

        layout = QGridLayout()
        layout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)

        self.setLayout(layout)

        for setting in settings:
            self.AddSetting(setting)

    def SetSetting(self, key: str, default):
        SettingsManager.Set(self.settingsBase + "." + key, default)

    def GetSetting(self, setting: SettingsItem):
        return SettingsManager.Get(self.settingsBase + "." + setting.key, setting.defaultValue)

    def AddSetting(self, setting: SettingsItem):
        lastRow = self.layout().rowCount()

        self.layout().addWidget(
            QLabel(QApplication.translate(setting.context, setting.label)), lastRow, 0)

        resetButton = QPushButton(QApplication.translate("settings", "Default"))

        match setting.settingType:
            case "checkbox":
                settingWidget = QCheckBox()
                settingWidget.setChecked(self.GetSetting(setting))
                settingWidget.stateChanged.connect(
                    lambda val=None: self.SetSetting(setting.key, settingWidget.isChecked()))
                resetButton.clicked.connect(
                    lambda bt=None: settingWidget.setChecked(setting.defaultValue))
            case "hotkey":
                settingWidget = QKeySequenceEdit()
                settingWidget.setKeySequence(self.GetSetting(setting))
                settingWidget.keySequenceChanged.connect(
                    lambda keySequence:
                    settingWidget.setKeySequence(keySequence.toString().split(",")[
                        0]) if keySequence.count() > 0 else None
                )
                settingWidget.keySequenceChanged.connect(
                    lambda sequence=None: [
                        self.SetSetting(setting.key, sequence.toString()),
                        setting.callback()
                    ]
                )
                resetButton.clicked.connect(
                    lambda bt=None: [
                        settingWidget.setKeySequence(setting.defaultValue),
                        setting.callback()
                    ]
                )
            case "textbox" | "password":
                settingWidget = QLineEdit()
                if setting.settingType == "password":
                    settingWidget.setEchoMode(QLineEdit.EchoMode.Password)
                settingWidget.setText(self.GetSetting(setting))
                settingWidget.textChanged.connect(
                    lambda val=None: self.SetSetting(setting.key, settingWidget.text()))
                resetButton.clicked.connect(
                    lambda bt=None: [
                        settingWidget.setText(setting.defaultValue),
                        setting.callback()
                    ]
                )
            case _:
                raise Exception("Invalid setting type")

        if setting.tooltip:
            settingWidget.setToolTip('\n'.join(textwrap.wrap(setting.tooltip, 40)))

        self.layout().addWidget(settingWidget, lastRow, 1)
        self.layout().addWidget(resetButton, lastRow, 2)


@dataclass
class SettingsGroup:
    name: str
    widget: SettingsWidget
    context: str = "settings"


class GenericSettingsWindow(QDialog):
    def __init__(self, window_name: str, settings: list[SettingsGroup], parent=None):
        super().__init__(parent=parent)
        self.window_name = window_name
        self.selection_list = QListWidget()
        self.settings_stack = QStackedWidget()
        self.settings = settings

    def UiMounted(self):
        self.setWindowTitle(QApplication.translate("Settings", self.window_name))

        self.selection_list.currentRowChanged.connect(self.on_selection_changed)

        # Create a scroll area for the settings stack
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.settings_stack)

        # Create a splitter for the selection and settings
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.selection_list)
        splitter.addWidget(scroll_area)

        # Set the layout for the dialog
        layout = QVBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)

        for settingGroup in self.settings:
            item = QListWidgetItem(QApplication.translate(settingGroup.context, settingGroup.name))
            widget = settingGroup.widget
            item.setData(Qt.ItemDataRole.UserRole, widget)
            self.selection_list.addItem(item)

            # Add the setting widget to the stack
            self.settings_stack.addWidget(widget)

        self.resize(1000, 500)
        QApplication.processEvents()
        splitter.setSizes([200, self.width() - 200])

    def on_selection_changed(self, index: int):
        # Get the selected item and its associated widget
        item = self.selection_list.item(index)
        widget = item.data(Qt.ItemDataRole.UserRole)

        # Set the current widget in the stack
        self.settings_stack.setCurrentWidget(widget)
