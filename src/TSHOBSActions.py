from enum import Enum
from .Helpers.TSHEnumHelper import SuperEnum
from .OBS.TSHOBSWebsockets import OBSWebsocketManager


class MetaOptions(SuperEnum):
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


class OBSOption(Enum):
    SCENE = 0
    FILTER = 1
    SOURCE = 2
    TEXT = 3
    TRANSFORM = 4


class OBSCommand:
    def __init__(self, appOption: AppOption, obsOptions: OBSOption, data=None):
        self.trigger = appOption
        self.target = obsOptions
        self.data = data


class OBSActions:
    def __init__(self):
        self.obs_ws = OBSWebsocketManager()

    def emit(self, option: AppOption, data=None):
        add = None
