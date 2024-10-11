# Django
from django.core.management import call_command
from django.test import TestCase

# Alliance Auth
from allianceauth.tests.auth_utils import AuthUtils


class TestCommand(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = AuthUtils.create_user("User_1")
        cls.user_2 = AuthUtils.create_user("User_2")
        cls.user_3 = AuthUtils.create_user("User_3")

    def _refresh_from_db(self):
        self.user_1.refresh_from_db()
        self.user_2.refresh_from_db()
        self.user_3.refresh_from_db()

    def test_force_nightmode(self):
        self._refresh_from_db()
        self.assertFalse(self.user_1.profile.night_mode)
        self.assertFalse(self.user_2.profile.night_mode)
        self.assertFalse(self.user_3.profile.night_mode)

        call_command("eunicore_force_nightmode")

        self._refresh_from_db()
        self.assertTrue(self.user_1.profile.night_mode)
        self.assertTrue(self.user_2.profile.night_mode)
        self.assertTrue(self.user_3.profile.night_mode)
