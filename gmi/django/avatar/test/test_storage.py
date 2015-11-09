from django.core.files import File
from django.test import TestCase
from io import BufferedRandom, BytesIO
from unittest.mock import Mock

import gmi.django.avatar.storage as storage


class GravatarStorageTestCase(TestCase):
    def setUp(self):
        storage.urllib.request.urlopen = Mock()
        storage.urllib.request.urlopen.return_value = BytesIO(b'foo')

        self.gravatar_storage = storage.GravatarStorage(
            email='test@example.com')

    def test_path_is_implemented(self):
        try:
            self.gravatar_storage.path('foo')
        except Exception as e:
            self.assertNotIsInstance(e, NotImplementedError)
            pass

    def test_open_is_implemented(self):
        try:
            self.gravatar_storage._open('foo')
        except Exception as e:
            self.assertNotIsInstance(e, AttributeError)
            pass

    def test_email(self):
        self.assertEqual(
            storage.GravatarStorage(email='test@example.com')._email,
            'test@example.com')

    def test_resolution(self):
        self.assertEqual(
            storage.GravatarStorage(email='test@example.com')._resolution, 80)
        self.assertEqual(
            storage.GravatarStorage(
                email='test@example.com', resolution=160)._resolution, 160)

    def test_prefix(self):
        self.assertEqual(
            storage.GravatarStorage(email='test@example.com').prefix,
            'avatar/80x80')
        self.assertEqual(
            storage.GravatarStorage(
                email='test@example.com', resolution=160).prefix,
            'avatar/160x160')

    def test_temporary_file(self):
        self.assertIsInstance(self.gravatar_storage._tmp, BufferedRandom)

    def test_path(self):
        self.assertEqual(
            self.gravatar_storage.path('foo'),
            'temporary file - avatar for foo 80')

    def test_open(self):
        self.assertIsInstance(self.gravatar_storage._open('foo'), File)
        self.assertEqual(self.gravatar_storage._tmp.read(), b'foo')

    def test_open_if_already_received(self):
        gravatar_storage = storage.GravatarStorage(email='test@example.com')
        gravatar_storage.__empty__ = False
        gravatar_storage._tmp = BytesIO(b'baz')
        gravatar_storage._tmp.seek(0)
        gravatar_storage._open('foo')
        self.assertEqual(gravatar_storage._tmp.read(), b'baz')

    def test_receive(self):
        self.gravatar_storage._receive()
        self.assertEqual(self.gravatar_storage._tmp.read(), b'foo')

    def test_empty(self):
        gravatar_storage = storage.GravatarStorage(email='test@example.com')
        self.assertTrue(gravatar_storage.empty)
        gravatar_storage._open('foo')
        self.assertFalse(gravatar_storage.empty)
