.. _setup:

Setup
=====

Installed apps
--------------

To use gmi.django.avatar you have to add it to your Django settings.

.. code-block:: none

    INSTALLED_APPS = (
        [...]
        'gmi.django.avatar',
    )


Fetch Avatar images
-------------------

To fetch Avatars for your users from Gravatar you have to run the
``collectstatic`` command from your manage.py.

.. caution::

  The GravatarStorage, that is used to access Gravatar, was only tested to
  store the received Avatar images with Django's StaticFilesStorage. It
  `should` work with other storage backends, but there be dragons.

It is recommendet to run the ``collectstatic`` command as a cron job to
regularely update the Avatar images and follow changes on the Gravatar source.
