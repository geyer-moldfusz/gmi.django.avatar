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
        return self.received_for is not self.user.email

#    @property
#    def url(self):
#        """
#        returns the Avatar image url for this user.
#        """
#        return utils.get_avatar_url(self.user, 160)

    def updated(self, email):
        """
        call when the Avatar image was updated for the given email address.
        """
        self.received_for = email
