from django.core.files import File
from django.core.files.storage import Storage
from libgravatar import Gravatar
from tempfile import TemporaryFile
import os
import urllib.request

class GravatarStorage(Storage):
    """
    A storage class to access Gravatar resources.
    """
    def __init__(self, email, resolution=80):
        """
        Creates a new GravatarStorage for a specific avatar and a given
        resolution. The avatar is stored in a temporary file.
        """
        self.__empty__ = True

        self._tmp = TemporaryFile()
        self._email = email
        self._resolution = resolution

        self.prefix = os.path.join(
            'avatar', '{}x{}'.format(resolution, resolution))

    def path(self, name):
        return(
            'gravatar|{}|{}'.format(name, self._resolution))

    @property
    def empty(self):
        """
        Checks if there are already downloaded avatar data.
        """
        return self.__empty__

    def _open(self, name, mode='rb'):
        """
        Returns a File object, downloads the avatar if neccessary.
        """
        if self.empty:
            self._receive()
        return File(self._tmp)

    def _receive(self):
        g = Gravatar(self._email)
        response = urllib.request.urlopen(
            g.get_image(
                size=self._resolution,
                default='retro',
                use_ssl=True))

        # XXX this is not thread safe
        if self.empty:
            self._tmp.write(response.read())
            self._tmp.seek(0)
            self.__empty__ = False
