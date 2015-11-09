from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
from libgravatar import Gravatar
import os

from gmi.django.avatar.storage import GravatarStorage
from gmi.django.avatar.utils import hash_email


class AvatarFinder(finders.BaseFinder):
    """
    A static files finder that tries to collect avatar images from external
    resources.
    """

    def __init__(self, *args, **kwargs):
        self.users = User.objects.all()
        super(AvatarFinder, self).__init__(*args, **kwargs)

    def find(self, path, all=False):
        """
        Serve from STATIC_ROOT, even in DEBUG mode. See also:
            https://docs.djangoproject.com/en/1.8/ref/contrib/staticfiles/#static-file-development-view
        """
        matches = []

        root, path = os.path.split(path)
        for user in self.users:
            if hash_email(user.email) == path:
                # XXX this is a realy dirty hack!
                match = os.path.join(settings.STATIC_ROOT, root, path)
                if not all:
                    return match
                matches.append(match)
        return matches


    def list(self, ignore_patterns):
        """
        List avatars for all users.
        """
        for user in self.users:
            for res in (80, 160, 320):
                yield hash_email(user.email), \
                      GravatarStorage(user.email, resolution=res)
