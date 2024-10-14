import unittest
import os
from unittest.mock import patch, MagicMock
from user_data.util import get_current_user_name, User
from user_data.permissions import UserPermissions
from user_data.settings import UserSettings

class TestUser(unittest.TestCase):
    @patch('users.util.get_current_user_name', return_value='testuser')
    def test_user_initialization(self, mock_get_user_name):
        user = User(get_current_user_name())
        self.assertEqual(user.username, 'testuser')

class TestUserPermissions(unittest.TestCase):
    def setUp(self):
        self.user = User('testuser')
        self.permissions = UserPermissions(self.user)

    @patch('ctypes.windll.shell32.IsUserAnAdmin', return_value=True)
    def test_is_admin(self, mock_is_admin):
        self.assertTrue(self.permissions.is_admin())

    @patch('ctypes.windll.shell32.IsUserAnAdmin', return_value=False)
    def test_is_not_admin(self, mock_is_admin):
        self.assertFalse(self.permissions.is_admin())

    def test_user_privileges(self):
        self.permissions.is_admin = MagicMock(return_value=True)
        self.assertEqual(self.permissions.get_user_privileges(), ["modify_system", "access_sensitive_files", "manage_users"])

        self.permissions.is_admin = MagicMock(return_value=False)
        self.assertEqual(self.permissions.get_user_privileges(), ["standard_access"])

class TestUserSettings(unittest.TestCase):
    @patch('users.util.User', return_value=MagicMock(username='testuser'))
    def setUp(self, mock_user):
        self.user = mock_user
        self.user_settings = UserSettings(self.user)

    def test_set_and_get_setting(self):
        self.user_settings.set_setting('theme', 'dark')
        self.assertEqual(self.user_settings.get_setting('theme'), 'dark')

    def test_load_settings(self):
        self.user_settings.set_setting('language', 'English')
        loaded_settings = self.user_settings.load_settings()
        self.assertIn('language', loaded_settings)
        self.assertEqual(loaded_settings['language'], 'English')

    def test_non_existent_setting(self):
        self.assertIsNone(self.user_settings.get_setting('nonexistent', default='default_value'))

if __name__ == '__main__':
    unittest.main()