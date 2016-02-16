from django.contrib.auth.models import User
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.files.storage import Storage
from django.test import LiveServerTestCase
from mock import Mock

from gmi.django.avatar.storage import GravatarUnknownError
import gmi.django.avatar.finder as finder

class AvatarFinderTestCase(LiveServerTestCase):
    set_handler = StaticFilesHandler

    def setUp(self):
        finder.GravatarStorage.load = Mock()
        finder.GravatarStorage.__repr__ = Mock()
        finder.GravatarStorage.__repr__.return_value = "GravatarStorage"

        john = User.objects.create_user(
            'john', 'john@example.com', 'apassword')
        john.save()
        paul = User.objects.create_user(
            'paul', 'paul@example.com', 'anotherpassword')
        paul.save()

        self.avatar_finder = finder.AvatarFinder()

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

    def test_list_returns_file_list(self):
        self.assertQuerysetEqual(
            self.avatar_finder.list(None), [
                "('855f96e983f1f8e8be944692b6f719fd54329826cb62e98015efee8e2e071dd4', GravatarStorage)",
                "('855f96e983f1f8e8be944692b6f719fd54329826cb62e98015efee8e2e071dd4', GravatarStorage)",
                "('855f96e983f1f8e8be944692b6f719fd54329826cb62e98015efee8e2e071dd4', GravatarStorage)",
                "('30e6eebb170988262e8c7d6b7a2e4a912ea780f09ea68fb97679fad3c3ee355b', GravatarStorage)",
                "('30e6eebb170988262e8c7d6b7a2e4a912ea780f09ea68fb97679fad3c3ee355b', GravatarStorage)",
                "('30e6eebb170988262e8c7d6b7a2e4a912ea780f09ea68fb97679fad3c3ee355b', GravatarStorage)"
            ])

    def test_list_handles_gravatar_unknown_error(self):
        finder.GravatarStorage.load.side_effect = GravatarUnknownError(
            'test@example.com')
        self.assertQuerysetEqual(self.avatar_finder.list(None), [])

    def test_list_raise_on_error(self):
        finder.GravatarStorage.load.side_effect = OSError()
        with self.assertRaises(OSError):
            next(self.avatar_finder.list(None))

    def test_list_updates_received_for(self):
        george = User.objects.create_user(
            'george', 'george@example.com', 'thirdpassword')
        george.save()
        list(self.avatar_finder.list(None))
        self.assertEqual(george.avatar.received_for, 'george@example.com')
