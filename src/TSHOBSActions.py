from enum import Enum
from collections.abc import Callable
from .Helpers.TSHEnumHelper import SuperEnum
from .OBS.TSHOBSWebsockets import OBSWebsocketManager


class MetaOptions(SuperEnum):
    CONFIRM = 0
    UNDO = 1
    REDO = 2
    RESTART = 3


class AppOption(SuperEnum):
    RPS = "rps"
    STAGE = "stage"
    STAGE_GENTLEMANS = "stage_gen"
    MATCH = "match"
    META = "meta", MetaOptions


class OBSOption(Enum):
    SCENE = 0
    FILTER = 1
    SOURCE = 2
    TEXT = 3
    TRANSFORM = 4


class OBSCommand:
    def __init__(self, appOption: AppOption, obsOptions: OBSOption, command: Callable = None):
        self.trigger = appOption
        self.target = obsOptions
        self.command = command


class OBSActions:
    def __init__(self):
        self.obs_ws = OBSWebsocketManager()

    def emit(self, option: AppOption, data=None):
        add = None
