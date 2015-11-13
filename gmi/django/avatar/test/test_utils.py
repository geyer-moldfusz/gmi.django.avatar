from django.contrib.auth.models import User
from django.test import TestCase
from gmi.django.avatar.models import Avatar
import gmi.django.avatar.utils as utils



class UtilsTestCase(TestCase):
    default_img = 'default.png'

    def setUp(self):
        pass

    def test_hash_email(self):
        self.assertEqual(
            utils.hash_email('foo@bar.baz'),
            '80c66bdd90ae7fd4378cef780422fe428ee7fb526301f7b236113c4ece3be146')

    def test_avatar_prefix(self):
        self.assertEqual(utils.get_avatar_prefix(120), 'avatar/120x120')

    def test_avatar_url(self):
        john = User.objects.create_user('john', 'john@example.com', 'password')
        avatar = Avatar.objects.create(user=john, received_for=john.email)
        self.assertEqual(
            utils.get_avatar_url(john, 120),
            'avatar/120x120/855f96e983f1f8e8be944692b6f719fd54329826cb62e98015efee8e2e071dd4')

    def test_avatar_url_empty_mail(self):
        john = User.objects.create_user('john', '', 'password')
        self.assertEqual(
            utils.get_avatar_url(john, 120), 'avatar/120x120/{}'.format(
                self.default_img))

    def test_avatar_url_outdated(self):
        john = User.objects.create_user('john', 'john@example.com', 'password')
        avatar = Avatar.objects.create(
            user=john, received_for='new@example.com')
        self.assertEqual(
            utils.get_avatar_url(john, 120), 'avatar/120x120/{}'.format(
                self.default_img))

    def test_avatar_url_without_avatar(self):
        john = User.objects.create_user('john', 'john@example.com', 'password')
        self.assertEqual(
            utils.get_avatar_url(john, 120), 'avatar/120x120/{}'.format(
                self.default_img))
