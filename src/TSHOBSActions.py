from enum import Enum
from collections.abc import Callable
from .Helpers.TSHEnumHelper import SuperEnum
from .OBS.TSHOBSWebsockets import OBSWebsocketManager


class MetaOption(SuperEnum):
    CONFIRM = 0
    UNDO = 1
    REDO = 2
    RESTART = 3


class AppOption(SuperEnum):
    RPS = "rps"
    STAGE = "stage"
    STAGE_GENTLEMANS = "stage_gen"
    MATCH = "match"
    META = "meta", MetaOption


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
    instance: "OBSActions" = None

    def __init__(self):
        self.obs_ws = OBSWebsocketManager()
        self.commands: list[OBSCommand] = []

    def updateCommands(self, commands: list[OBSCommand]):
        self.commands = commands

    # data is either stage name or player number (0 for first, 1 for second)
    def emit(self, trigger: AppOption, data: str | int = None):
        filtered = [command for command in self.commands if command.trigger in trigger.enum_path]
        for command in filtered:
            result = command.command(data)
            match command.target:
                case OBSOption.SCENE:
                    self.obs_ws.set_scene(result)
                case OBSOption.FILTER:
                    obs_source, obs_filter, filter_enabled = result
                    self.obs_ws.set_filter_visibility(obs_source, obs_filter, filter_enabled)
                case OBSOption.SOURCE:
                    obs_scene, obs_source, source_visible = result
                    self.obs_ws.set_source_visibility(obs_scene, obs_source, source_visible)
                case OBSOption.TEXT:
                    obs_source, text = result
                    self.obs_ws.set_text(obs_source, text)
                case OBSOption.TRANSFORM:
                    obs_scene, obs_source, source_transform = result
                    self.obs_ws.set_source_transform(obs_scene, obs_source, source_transform)


OBSActions.instance = OBSActions()
