from enum import Enum
from .Helpers.TSHEnumHelper import SuperEnum
from .OBS.TSHOBSWebsockets import OBSWebsocketManager


class MetaOptions(Enum):
    CONFIRM = 0
    UNDO = 1
    REDO = 2
    RESTART = 3
    GENTLEMANS = 4


class AppOption(SuperEnum):
    RPS = "rps"
    STAGE = "stage"
    MATCH = "match"
    META = "meta", MetaOptions


class OBSActions:
    def __init__(self):
        self.obs_ws = OBSWebsocketManager()

    def emit(self, option: AppOption, data=None):
        add = None
