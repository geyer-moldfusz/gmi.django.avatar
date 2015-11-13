from gmi.django.avatar.models import Avatar
import hashlib
import os


def hash_email(email):
    sha = hashlib.sha256()
    sha.update(bytearray(email, 'utf-8'))
    return sha.hexdigest()


def get_avatar_prefix(resolution):
    return os.path.join('avatar', '{}x{}'.format(resolution, resolution))


def get_avatar_url(user, resolution):
    if user.email:
        try:
            if not user.avatar.outdated:
                return os.path.join(
                    get_avatar_prefix(resolution), hash_email(user.email))
        except Avatar.DoesNotExist:
            pass

    return os.path.join(get_avatar_prefix(resolution), 'none')
