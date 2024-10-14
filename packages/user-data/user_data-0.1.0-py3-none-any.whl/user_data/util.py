import os
from pathlib import Path

def get_current_user_name():
    """
    Returns the current logged-in user's username.
    """
    return os.getlogin()

class User:
    def __init__(self, username):
        self.username = username

    def _get_user_profile_base(self):
        """
        Returns the base user profile path based on the username.
        """
        return Path(f"C:/Users/{self.username}")

    # Method 1: AppData directory
    def get_appdata_directory(self):
        return self._get_user_profile_base() / 'AppData' / 'Roaming'

    # Method 2: Home directory
    def get_home_directory(self):
        return self._get_user_profile_base()

    # Method 3: Desktop directory
    def get_desktop_directory(self):
        return self._get_user_profile_base() / 'Desktop'

    # Method 4: Documents directory
    def get_documents_directory(self):
        return self._get_user_profile_base() / 'Documents'

    # Method 5: Downloads directory
    def get_downloads_directory(self):
        return self._get_user_profile_base() / 'Downloads'

    # Method 6: Music directory
    def get_music_directory(self):
        return self._get_user_profile_base() / 'Music'

    # Method 7: Pictures directory
    def get_pictures_directory(self):
        return self._get_user_profile_base() / 'Pictures'

    # Method 8: Videos directory
    def get_videos_directory(self):
        return self._get_user_profile_base() / 'Videos'

    # Method 9: Temp directory
    def get_temp_directory(self):
        return self._get_user_profile_base() / 'AppData' / 'Local' / 'Temp'

    # Method 10: LocalAppData directory
    def get_local_appdata_directory(self):
        return self._get_user_profile_base() / 'AppData' / 'Local'

    # Method 11: ProgramData directory (not user-specific but for compatibility)
    def get_program_data_directory(self):
        return Path(os.getenv('PROGRAMDATA'))

    # Method 12: User's username
    def get_username(self):
        return self.username

    # Method 13: SystemDrive
    def get_system_drive(self):
        return Path("C:/")

    # Method 14: ProgramFiles directory (global, not user-specific)
    def get_program_files_directory(self):
        return Path(os.getenv('ProgramFiles'))

    # Method 15: ProgramFiles (x86) directory
    def get_program_files_x86_directory(self):
        return Path(os.getenv('ProgramFiles(x86)'))

    # Method 16: SystemRoot (global)
    def get_system_root(self):
        return Path(os.getenv('SystemRoot'))

    # Method 17: User profile directory
    def get_user_profile_directory(self):
        return self._get_user_profile_base()

    # Method 18: User domain (if applicable)
    def get_user_domain(self):
        return os.getenv('USERDOMAIN')

    # Method 19: Processor architecture
    def get_processor_architecture(self):
        return os.getenv('PROCESSOR_ARCHITECTURE')

    # Method 20: Computer name
    def get_computer_name(self):
        return os.getenv('COMPUTERNAME')

    # Method 21: Windows directory
    def get_windows_directory(self):
        return Path(os.getenv('WINDIR'))

    # Method 22: Processor identifier
    def get_processor_identifier(self):
        return os.getenv('PROCESSOR_IDENTIFIER')

    # Method 23: Processor level
    def get_processor_level(self):
        return os.getenv('PROCESSOR_LEVEL')

    # Method 24: Processor revision
    def get_processor_revision(self):
        return os.getenv('PROCESSOR_REVISION')

    # Method 25: Home drive (based on username)
    def get_home_drive(self):
        return Path("C:/")

    # Method 26: Home path
    def get_home_path(self):
        return f"C:/Users/{self.username}"

    # Method 27: Number of processors
    def get_number_of_processors(self):
        return os.getenv('NUMBER_OF_PROCESSORS')

    # Method 28: Timezone
    def get_timezone(self):
        return os.getenv('TZ')

    # Method 29: All Users profile
    def get_all_users_profile(self):
        return Path(os.getenv('ALLUSERSPROFILE'))

    # Method 30: System temp directory
    def get_system_temp_directory(self):
        return Path(os.getenv('TEMP'))

    # Method 31: Common program files
    def get_common_program_files_directory(self):
        return Path(os.getenv('COMMONPROGRAMFILES'))

    # Method 32: Common program files (x86)
    def get_common_program_files_x86_directory(self):
        return Path(os.getenv('COMMONPROGRAMFILES(x86)'))

    # Method 33: Logon server
    def get_logon_server(self):
        return os.getenv('LOGONSERVER')

    # Method 34: System directory
    def get_system_directory(self):
        return Path(os.getenv('SystemRoot')) / 'System32'

    # Method 35: Roaming profile
    def get_roaming_profile(self):
        return self._get_user_profile_base() / 'AppData' / 'Roaming'

    # Method 36: Local Low directory
    def get_local_low_directory(self):
        return self._get_user_profile_base() / 'AppData' / 'LocalLow'

    # Method 37: OneDrive folder
    def get_onedrive_directory(self):
        return self._get_user_profile_base() / 'OneDrive'

    # Method 38: Internet cache directory
    def get_internet_cache_directory(self):
        return self._get_user_profile_base() / 'AppData' / 'Local' / 'Microsoft' / 'Windows' / 'INetCache'

    # Method 39: Cookies directory
    def get_cookies_directory(self):
        return self._get_user_profile_base() / 'AppData' / 'Roaming' / 'Microsoft' / 'Windows' / 'Cookies'

    # Method 40: Favourites directory
    def get_favourites_directory(self):
        return self._get_user_profile_base() / 'Favorites'

    # Method 41: Recent items directory
    def get_recent_items_directory(self):
        return self._get_user_profile_base() / 'AppData' / 'Roaming' / 'Microsoft' / 'Windows' / 'Recent'

    # Method 42: Printer spool directory
    def get_printer_spool_directory(self):
        return Path(os.getenv('SYSTEMROOT')) / 'System32' / 'spool'

    # Method 43: IP address
    def get_ip_address(self):
        import socket
        return socket.gethostbyname(socket.gethostname())

    # Method 44: Full name (environmental variable)
    def get_full_name(self):
        return os.getenv('USER')

    # Method 45: Saved games directory
    def get_saved_games_directory(self):
        return self._get_user_profile_base() / 'Saved Games'

    # Method 46: Links directory
    def get_links_directory(self):
        return self._get_user_profile_base() / 'Links'

    # Method 47: Searches directory
    def get_searches_directory(self):
        return self._get_user_profile_base() / 'Searches'

    # Method 48: Contacts directory
    def get_contacts_directory(self):
        return self._get_user_profile_base() / 'Contacts'

    # Method 49: Domain role (None if no domain)
    def get_user_domain_role(self):
        return os.getenv('USERDOMAIN_ROAMINGPROFILE')

    # Method 50: 3D Objects directory
    def get_3d_objects_directory(self):
        return self._get_user_profile_base() / '3D Objects'