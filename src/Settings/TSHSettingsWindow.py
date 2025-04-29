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
                    SettingsItem(),
                    SettingsItem(),
                    SettingsItem(),
                    SettingsItem(),
                    SettingsItem()
                ])
            ),
            SettingsGroup(
                "Hotkeys",
                SettingsWidget("hotkeys", [])
            ),
            SettingsGroup(
                "Bluesky",
                SettingsWidget("bsky_account", [
                    SettingsItem(),
                ])
            )
        ]
        super().__init__("Settings", settings, parent=parent)

    def UiMounted(self):
        # Add general settings
        generalSettings = [(
            QApplication.translate(
                "settings.general", "Enable profanity filter"),
            "profanity_filter",
            "checkbox",
            True
        ), (
            QApplication.translate(
                "settings.control_score_from_stage_strike", "Enable score control from the stage striking app"),
            "control_score_from_stage_strike",
            "checkbox",
            True
        ), (
            QApplication.translate(
                "settings.disable_autoupdate", "Disable automatic set updating for the scoreboard"),
            "disable_autoupdate",
            "checkbox",
            False
        ), (
            QApplication.translate(
                "settings.disable_export", "Disable TSH file exporting"),
            "disable_export",
            "checkbox",
            False
        ), (
            QApplication.translate(
                "settings.disable_overwrite",
                "Do not override existing values in local_players.csv (takes effect on next restart)"),
            "disable_overwrite",
            "checkbox",
            False
        )]

        # Add hotkey settings
        hotkeySettings = [(
            QApplication.translate("settings.hotkeys", "Enable hotkeys"),
            "hotkeys_enabled",
            "checkbox",
            True
        )]

        key_names = {
            "load_set": QApplication.translate("settings.hotkeys", "Load set"),
            "team1_score_up": QApplication.translate("settings.hotkeys", "Team 1 score up"),
            "team1_score_down": QApplication.translate("settings.hotkeys", "Team 1 score down"),
            "team2_score_up": QApplication.translate("settings.hotkeys", "Team 2 score up"),
            "team2_score_down": QApplication.translate("settings.hotkeys", "Team 2 score down"),
            "reset_scores": QApplication.translate("settings.hotkeys", "Reset scores"),
            "swap_teams": QApplication.translate("settings.hotkeys", "Swap teams"),
        }

        for i, (setting, value) in enumerate(TSHHotkeys.instance.keys.items()):
            hotkeySettings.append((
                key_names[setting],
                setting,
                "hotkey",
                value,
                TSHHotkeys.instance.ReloadHotkeys
            ))
            
        # Add Bluesky settings
        bskySettings = [(
            QApplication.translate(
                "settings.bsky", "Host server"),
            "host",
            "textbox",
            "https://bsky.social"
        ), (
            QApplication.translate(
                "settings.bsky", "Bluesky Handle"),
            "username",
            "textbox",
            ""
        ), (
            QApplication.translate(
                "settings.bsky", "Application Password"),
            "app_password",
            "password",
            "",
            None,
            QApplication.translate(
                "settings.bsky",
                "You can get an app password by going into your Bluesky settings -> Privacy & Security") + "\n" +
            QApplication.translate(
                "settings.bsky",
                "Please note that said app password will be stored in plain text on your computer") + "\n\n" +
            QApplication.translate(
                "settings.bsky", "Do not use your regular account password!").upper()
        )]


