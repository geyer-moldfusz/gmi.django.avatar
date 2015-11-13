from django.contrib.auth.models import User
from django.test import TestCase
from gmi.django.avatar.models import Avatar


class AvatarModelTestCase(TestCase):
    def setUp(self):
        self.john = User.objects.create_user(
            'john', 'john@example.com', 'apassword')
        self.john.save()
        avatar = Avatar.objects.create(received_for='foobar', user=self.john)

    def test_avatar_extends_user(self):
        self.assertIsInstance(self.john.avatar, Avatar)

    def test_outdated_if_current(self):
        self.john.avatar.received_for = 'john@example.com'
        self.assertFalse(self.john.avatar.outdated)

    def test_outdated_if_not_current(self):
        self.john.avatar.received_for = 'foo'
        self.assertTrue(self.john.avatar.outdated)

    def test_updated(self):
        self.john.avatar.updated('test@example.com')
        self.assertEqual(self.john.avatar.received_for, 'test@example.com')
