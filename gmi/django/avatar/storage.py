from django.core.files import File
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from libgravatar import Gravatar
from tempfile import TemporaryFile
import os
import urllib.request

import gmi.django.avatar.utils as utils

try:
    from urllib.error import HTTPError
    from urllib.request import urlopen
except ImportError:
    from urllib2 import HTTPError
    from urllib2 import urlopen


@deconstructible
class GravatarStorage(Storage):
    """
    A storage class to access Gravatar resources.
    """
    def __init__(self, email, resolution=80):
        """
        Creates a new GravatarStorage for a specific avatar and a given
        resolution. The avatar is stored in a temporary file.
        """
        self._email = email
        self._resolution = resolution

        self.prefix = utils.get_avatar_prefix(resolution)

    def path(self, name):
        return(
            'gravatar|{}|{}'.format(name, self._resolution))

    @property
    def email(self):
        return self._email

    @property
    def empty(self):
        """
        Checks if there are already downloaded avatar data.
        """
        return not hasattr(self, '_tmp')

    def load(self):
        """
        Loads a Gravatar image to temporary file. Raises a GravatarUnkownError
        in case there is no Avatar for the given email.
        """
        if self.empty:
            # XXX this is not thread safe
            try:
                tmp = self._receive()
            except HTTPError as e:
                if not e.getcode() == 404:
                    raise e
                raise GravatarUnknownError(self._email)

            self._tmp = TemporaryFile()
            self._tmp.write(tmp.read())
            self._tmp.seek(0)

    def _open(self, name, mode='rb'):
        """
        Returns a File object, downloads the avatar if neccessary. May raise
        HTTPError in case of connection failure.
        """
        self.load()
        return File(self._tmp)

    def _receive(self):
        """
        Downloads a Gravatar image. May raise an HTTPError.
        """
        g = Gravatar(self._email)
        response = urlopen(g.get_image(
            size=self._resolution,
            default='404',
            use_ssl=True))
        return response


class GravatarUnknownError(Exception):

    def __init__(self, email):
        self.email = email

    def __str__(self):
        return 'no Gravatar found for {}'.format(self.email)
