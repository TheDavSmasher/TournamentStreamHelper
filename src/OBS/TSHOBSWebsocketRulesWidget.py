from PySide6.QtWidgets import QWidget
from ..TSHOBSActions import OBSActions


class OBSWebsocketRulesWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.obsActions = OBSActions.instance
