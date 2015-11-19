from django.contrib.auth.models import User
from django.db import models


class Avatar(models.Model):
    user = models.OneToOneField(User)
    received_for = models.EmailField(blank=True)

    @property
    def outdated(self):
        """
        checks if the email address was updated and the received Avatar is
        outdated.
        """
        return self.received_for != self.user.email

    def updated(self, email):
        """
        call when the Avatar image was updated for the given email address.
        """
        self.received_for = email

    def url(self, resolution):
        import gmi.django.avatar.utils as utils
        return utils.get_avatar_url(self.user, resolution)
