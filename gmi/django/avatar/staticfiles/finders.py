from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
from gmi.django.avatar.storage import GravatarStorage
from libgravatar import Gravatar


class AvatarFinder(finders.BaseFinder):
    """
    A static files finder that tries to collect avatar images from external
    resources.
    """

    def __init__(self, *args, **kwargs):
        self.users = User.objects.all()
        super(AvatarFinder, self).__init__(*args, **kwargs)

    def find(self, path, all=False):
        pass

    def list(self, ignore_patterns):
        """
        List avatars for all users.
        """
        for user in self.users:
            for res in (80, 160, 320):
                yield user.email, GravatarStorage(user.email, resolution=res)
