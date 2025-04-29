from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, TypeVar, Generic

from qtpy.QtCore import *
from qtpy.QtWidgets import *


@dataclass
class SettingsItem:
    name: str
    context: str
    setting: str
    setting_type: str
    default_value: Any
    callback = lambda: None
    tooltip: str = None


class AbstractSettingsWidget(QWidget):
    def __init__(self, settingsBase="", settings: list[SettingsItem] = []):
        super().__init__()

        self.settingsBase = settingsBase

        layout = QGridLayout()
        layout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)

        self.setLayout(layout)

        for setting in settings:
            self.AddSetting(setting)

    @abstractmethod
    def AddSetting(self, setting: SettingsItem):
        pass


T = TypeVar('T', bound=AbstractSettingsWidget)


@dataclass
class SettingsGroup(Generic[T]):
    name: str
    widget: T
    context: str = "settings"


class GenericSettingsWindow(QDialog, Generic[T]):
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
