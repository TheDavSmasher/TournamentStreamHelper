from qtpy.QtWidgets import *
from .SettingsWidget import SettingsWidget
from ..Helpers.TSHSettingsHelper import GenericSettingsWindow, SettingsGroup, SettingsItem
from ..TSHHotkeys import TSHHotkeys


class TSHSettingsWindow(GenericSettingsWindow[SettingsWidget]):
    def __init__(self, parent=None):
        settings: list[SettingsGroup] = [
            SettingsGroup(
                "General",
                SettingsWidget("general", [
                    SettingsItem("Enable profanity filter", "settings.general", "profanity_filter", "checkbox", True),
                    SettingsItem("Enable score control from the stage striking app",
                                 "settings.control_score_from_stage_strike", "control_score_from_stage_strike",
                                 "checkbox", True),
                    SettingsItem("Disable automatic set updating for the scoreboard", "settings.disable_autoupdate",
                                 "disable_autoupdate", "checkbox", False),
                    SettingsItem("Disable TSH file exporting", "settings.disable_export", "disable_export", "checkbox",
                                 False),
                    SettingsItem("Do not override existing values in local_players.csv (takes effect on next restart)",
                                 "settings.disable_overwrite", "disable_overwrite", "checkbox", False)
                ])
            ),
            SettingsGroup(
                "Hotkeys",
                SettingsWidget("hotkeys", TSHSettingsWindow.GetHotkeySettings()),
            ),
            SettingsGroup(
                "Bluesky",
                SettingsWidget("bsky_account", [
                    SettingsItem("Host server", "settings.bsky", "host", "textbox", "https://bsky.social"),
                    SettingsItem("Bluesky Handle", "settings.bsky", "username", "textbox", ""),
                    SettingsItem("Application Password", "settings.bsky", "app_password", "password", "",
                                 lambda: None,
                                 QApplication.translate(
                                     "settings.bsky",
                                     "You can get an app password by going into your Bluesky settings -> Privacy & Security") + "\n" +
                                 QApplication.translate(
                                     "settings.bsky",
                                     "Please note that said app password will be stored in plain text on your computer") + "\n\n" +
                                 QApplication.translate(
                                     "settings.bsky", "Do not use your regular account password!").upper())
                ])
            )
        ]
        super().__init__("Settings", settings, parent=parent)

    @staticmethod
    def GetHotkeySettings():
        hotkeySettings = [SettingsItem("Enable hotkeys", "settings.hotkeys", "hotkeys_enabled", "checkbox", True)]

        key_names = {
            "load_set": "Load set",
            "team1_score_up": "Team 1 score up",
            "team1_score_down": "Team 1 score down",
            "team2_score_up": "Team 2 score up",
            "team2_score_down": "Team 2 score down",
            "reset_scores": "Reset scores",
            "swap_teams": "Swap teams",
        }

        for _, (setting, value) in enumerate(TSHHotkeys.instance.keys.items()):
            hotkeySettings.append(SettingsItem(key_names[setting], "settings.hotkeys", setting, "hotkey", value, TSHHotkeys.instance.ReloadHotkeys))
        return hotkeySettings
