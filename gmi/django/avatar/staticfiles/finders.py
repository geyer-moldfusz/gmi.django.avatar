from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
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
        """
        Cycles all users and tries to download an avatar image.
        """
        import pdb; pdb.set_trace()

    def list(self, ignore_patterns):
        return ['foo']
