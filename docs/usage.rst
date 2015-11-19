.. _usage

Usage
=====

User model
----------

The gmi.django.avatar adds an avatar model to your users using an OneToOne
relationship. Here is an example how to get the static avatar URL for a given
user:

.. code-block:: python

  from django.contrib.auth.models import User
  
  john = User.objects.get(username='john')
  url = john.avatar.url(resolution=160)

If you are not sure if there is an avatar model for a given user, you can also
use the gmi.django.avatar.utils that return a default avatar image for a user
without a corresponding avatar model:

.. code-block:: python

  from django.contrib.auth.models import User
  import gmi.django.avatar.utils as utils
  
  john = User.objects.get(username='john')
  url = utils.get_avatar_url(john, resolution=160)


.. note::

  By default gmi.django.avatar manages the resolutions 80, 160 and 320.

It is also possible to test if the stored avatar image is still valid, or if a
user has changed their email address. If so, gmi.django.avatar serves the
default avatar until there is a new avatar fetched by ``collectstatic``.

.. code-block:: python

  from django.contrib.auth.models import User
  
  john = User.objects.get(username='john')
  john.avatar.outdated


Template tags
-------------

gmi.django.avatar adds a template tag to link to avatar images in Django templates.

.. code-block:: jinja

  {% load avatar_tags %}
  
  <img src={{ user|avatar_url:320 }} class="avatar" />
