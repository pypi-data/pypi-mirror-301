import os
import configparser
from user_data.util import User

class UserSettings:
    def __init__(self, user: User) -> None:
        """
        Initialize UserSettings with a User instance.

        :param user: An instance of the User class.
        """
        self.user = user
        # Define the settings file path
        self.settings_file = os.path.join(f"C:/Users/{self.user.username}", "settings.ini")
        # Create a ConfigParser object
        self.config = configparser.ConfigParser()
        # Read existing settings
        self.config.read(self.settings_file)

    def load_settings(self) -> dict:
        """
        Load settings from the INI file.

        :return: A dictionary of settings.
        """
        settings = {}
        if os.path.exists(self.settings_file):
            self.config.read(self.settings_file)
            for section in self.config.sections():
                for key, value in self.config.items(section):
                    settings[key] = value
        return settings

    def save_settings(self, settings: dict) -> None:
        """
        Save settings to the INI file.

        :param settings: A dictionary of settings to save.
        """
        if not self.config.has_section('UserPreferences'):
            self.config.add_section('UserPreferences')
        
        for key, value in settings.items():
            self.config.set('UserPreferences', key, str(value))
        
        with open(self.settings_file, 'w') as f:
            self.config.write(f)

    def get_setting(self, key: str, default: str = None) -> str:
        """
        Get a specific setting by key. Returns default if not found.

        :param key: The setting key to retrieve.
        :param default: The default value to return if the key is not found.
        :return: The value of the setting.
        """
        settings = self.load_settings()
        return settings.get(key, default)

    def set_setting(self, key: str, value: str) -> None:
        """
        Set a specific setting by key.

        :param key: The setting key to set.
        :param value: The value to set for the setting.
        """
        settings = self.load_settings()
        settings[key] = value
        self.save_settings(settings)