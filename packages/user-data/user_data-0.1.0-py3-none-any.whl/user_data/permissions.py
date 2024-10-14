import ctypes
from user_data.util import User

class UserPermissions:
    def __init__(self, user: User) -> None:
        """
        Initialize UserPermissions with a User instance.

        :param user: An instance of the User class.
        """
        self.user = user

    def is_admin(self) -> bool:
        """
        Check if the user has administrator privileges using ctypes.

        :return: True if the user is an admin, False otherwise.
        """
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            is_admin = False
        return is_admin

    def can_modify_system(self) -> bool:
        """
        Check if the user can modify system settings (requires admin).

        :return: True if the user can modify system, False otherwise.
        """
        return self.is_admin()

    def get_user_privileges(self) -> list[str]:
        """
        Return a list of user privileges based on admin status.

        :return: A list of privileges.
        """
        if self.is_admin():
            return ["modify_system", "access_sensitive_files", "manage_users"]
        else:
            return ["standard_access"]