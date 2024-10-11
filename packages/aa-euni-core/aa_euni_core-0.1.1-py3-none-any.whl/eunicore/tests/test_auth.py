# Django
from django.test import TestCase

# Alliance Auth
from allianceauth.authentication.models import CharacterOwnership, UserProfile
from allianceauth.eveonline.models import EveCharacter
from allianceauth.tests.auth_utils import AuthUtils
from esi.models import Token

from ..auth.backends import EUniBackend


class TestAuth(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.unregistered_character = EveCharacter.objects.create(
            character_id=1,
            character_name="Unregistered Character",
            corporation_id=1,
            corporation_name="Corp",
            corporation_ticker="CORP",
        )
        cls.registered_character = EveCharacter.objects.create(
            character_id=2,
            character_name="Registered Character",
            corporation_id=1,
            corporation_name="Corp",
            corporation_ticker="CORP",
        )
        cls.reg_user = AuthUtils.create_user(
            "Registered_Character", disconnect_signals=True
        )
        AuthUtils.disconnect_signals()
        CharacterOwnership.objects.create(
            user=cls.reg_user, character=cls.registered_character, owner_hash="1"
        )
        UserProfile.objects.update_or_create(
            user=cls.reg_user, defaults={"main_character": cls.registered_character}
        )
        AuthUtils.connect_signals()

    def test_auth_registered_character(self):
        t = Token(
            character_id=self.registered_character.character_id,
            character_owner_hash="1",
        )
        user = EUniBackend().authenticate(token=t)
        self.assertEqual(user, self.reg_user)

    def test_auth_unregistered_character(self):
        t = Token(
            character_id=self.unregistered_character.character_id,
            character_name=self.unregistered_character.character_name,
            character_owner_hash="2",
        )
        user = EUniBackend().authenticate(token=t)
        self.assertNotEqual(user, self.reg_user)
        self.assertEqual(user.username, "Unregistered_Character")
        self.assertTrue(user.is_active)
        self.assertEqual(user.email, f"{user.id}@eveuniversity.org")
        self.assertEqual(user.profile.main_character, self.unregistered_character)
        self.assertTrue(user.profile.night_mode)
