from django import template
from django.contrib.staticfiles.storage import staticfiles_storage

import gmi.django.avatar.utils as utils


register = template.Library()


@register.filter
def avatar_url(user, resolution=160):
    return staticfiles_storage.url(utils.get_avatar_url(user, resolution))
