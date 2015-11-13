from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
from libgravatar import Gravatar
import os

from gmi.django.avatar.models import Avatar
from gmi.django.avatar.storage import GravatarStorage, GravatarUnknownError
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
                # create storage, try to get an Gravatar image
                storage = GravatarStorage(user.email, resolution=res)
                try:
                    storage.load()
                except GravatarUnknownError:
                    continue
                yield hash_email(user.email), storage

                # If we are here, the Gravatar image has been saved to a static
                # storage, so we register the email address to correspond with
                # a valid image.

                # XXX we have to check for dry_runs
                try:
                    user.avatar.updated(storage.email)
                except Avatar.DoesNotExist:
                    avatar = Avatar.objects.create(
                        user=user, received_for=storage.email)
