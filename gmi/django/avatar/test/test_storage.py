from django.core.files import File
from django.test import TestCase
from io import BufferedRandom, BytesIO
from unittest.mock import Mock
from urllib.error import HTTPError

import gmi.django.avatar.storage as storage


class GravatarStorageTestCase(TestCase):
    def setUp(self):
        storage.urlopen = Mock()
        storage.urlopen.return_value = BytesIO(b'foo')

        self.http_404 = HTTPError('dummy_url', 404, 'not found', None, None)
        self.http_500 = HTTPError('dummy_url', 500, 'server error', None, None)

        self.gravatar_storage = storage.GravatarStorage(
            email='test@example.com')

    def test_path_is_implemented(self):
        try:
            self.gravatar_storage.path('foo')
        except Exception as e:
            self.assertNotIsInstance(e, NotImplementedError)

    def test_open_is_implemented(self):
        try:
            self.gravatar_storage._open('foo')
        except Exception as e:
            self.assertNotIsInstance(e, AttributeError)

    def test_email(self):
        self.assertEqual(
            storage.GravatarStorage(email='test@example.com').email,
            'test@example.com')

    def test_resolution(self):
        gravatar_storage = storage.GravatarStorage(
            email='test@example.com', resolution=160)
        self.assertEqual(gravatar_storage._resolution, 160)

    def test_prefix(self):
        self.assertEqual(
            storage.GravatarStorage(email='test@example.com').prefix,
            'avatar/80x80')
        self.assertEqual(
            storage.GravatarStorage(
                email='test@example.com', resolution=160).prefix,
            'avatar/160x160')

    def test_temporary_file(self):
        self.gravatar_storage._open('foo')
        self.assertIsInstance(self.gravatar_storage._tmp, BufferedRandom)

    def test_path(self):
        self.assertEqual(
            self.gravatar_storage.path('foo'), 'gravatar|foo|80')

    def test_open(self):
        self.assertIsInstance(self.gravatar_storage._open('foo'), File)
        self.assertEqual(self.gravatar_storage._open('foo').read(), b'foo')

    def test_load(self):
        gravatar_storage = storage.GravatarStorage(email='test@example.com')
        gravatar_storage.load()
        self.assertEqual(gravatar_storage._tmp.read(), b'foo')

    def test_load_if_already_received(self):
        gravatar_storage = storage.GravatarStorage(email='test@example.com')
        gravatar_storage._tmp = BytesIO(b'baz')
        gravatar_storage._tmp.seek(0)
        gravatar_storage.load()
        self.assertEqual(gravatar_storage._tmp.read(), b'baz')

    def test_load_unknown(self):
        storage.urlopen.side_effect = self.http_404
        gravatar_storage = storage.GravatarStorage(email='test@example.com')
        with self.assertRaises(storage.GravatarUnknownError):
            gravatar_storage.load()

    def test_load_raise_on_HTTP_error(self):
        storage.urlopen.side_effect = self.http_500
        gravatar_storage = storage.GravatarStorage(email='test@example.com')
        with self.assertRaises(HTTPError):
            gravatar_storage.load()

    def test_receive(self):
        self.assertEqual(self.gravatar_storage._receive().read(), b'foo')

    def test_receive_unknown(self):
        storage.urlopen.side_effect = self.http_404
        gravatar_storage = storage.GravatarStorage(email='test@example.com')
        with self.assertRaises(HTTPError):
            gravatar_storage._receive()

    def test_empty(self):
        gravatar_storage = storage.GravatarStorage(email='test@example.com')
        gravatar_storage._open('foo')
        self.assertFalse(gravatar_storage.empty)

    def test_gravatar_unknown_error(self):
        with self.assertRaisesMessage(
            storage.GravatarUnknownError,
            'no Gravatar found for test@example.com') as context:
                raise storage.GravatarUnknownError(email='test@example.com')
        self.assertEqual(context.exception.email, 'test@example.com')
