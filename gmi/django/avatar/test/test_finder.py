from django.contrib.auth.models import User
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.test import LiveServerTestCase
from gmi.django.avatar.staticfiles.finders import AvatarFinder
from unittest.mock import MagicMock


class AvatarFinderTestCase(LiveServerTestCase):
    set_handler = StaticFilesHandler

    def setUp(self):
        john = User.objects.create_user(
            'john', 'john@example.com', 'apassword')
        john.save()
        paul = User.objects.create_user(
            'paul', 'paul@example.com', 'anotherpassword')
        paul.save()

        self.avatar_finder = AvatarFinder()

    def test_find_is_implemented(self):
        try:
            self.avatar_finder.find('foo')
        except Exception as e:
            self.assertNotIsInstance(e, NotImplementedError)
            pass

    def test_list_is_implemented(self):
        try:
            self.avatar_finder.list('pattern')
        except Exception as e:
            self.assertNotIsInstance(e, NotImplementedError)
            pass

    def test_collect_all_users(self):
        self.assertQuerysetEqual(
            self.avatar_finder.users,
            ['<User: john>', '<User: paul>'],
            ordered=False)

    def test_return_gravatar_urls(self):
        self.assertListEqual(
            ['foo', 'bar'],
            self.avatar_finder.find())
