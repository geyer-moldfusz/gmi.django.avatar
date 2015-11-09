from django.contrib.auth.models import User
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.files.storage import Storage
from django.test import LiveServerTestCase
from gmi.django.avatar.finder import AvatarFinder


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

    def test_list_returns_file_list(self):
        avatar_list = self.avatar_finder.list(None)
        avatar_item = list(avatar_list)[0]
        self.assertEqual(
            avatar_item[0],
            '855f96e983f1f8e8be944692b6f719fd54329826cb62e98015efee8e2e071dd4.jpg')
        self.assertIsInstance(avatar_item[1], Storage)
