.. _install:

Installation
============

Requirements
------------

- Python 3.4
- Django >1.8 (tested with Django 1.8, Django 1.7 may work,
  Django <1.7 is not supported)

For development checkouts you will also need

- git

Installation using Distribute and Pip
-------------------------------------

For now there is no final release. Installation using pip will be
supported as soon as there is a release.

Installation of development version from source
-----------------------------------------------

.. code-block:: console

    $ git clone http://github.com/geyer-moldfusz/gmi.django.avatar.git
    $ cd gmi.django.profile
    $ python3.4 setup.py install

Setup development environment
-----------------------------

The recommendet way to setup a development environment is to use
``virtualenv``, zc.buildout, the djangorecipe and the
mr.developer extension.

.. code-block:: console

    $ virtualenv --python=python3.4 django_project
    $ cd django_project
    $ ./bin/pip install zc.buildout

Create a buildout.cfg

XXX

.. code-block:: none

    [buildout]
    extensions = mr.developer
    parts = django
    
    sources = sources
    auto-checkout = *
    always-checkout = true
    
    [sources]
    gmi.django.avatar = git git@FIXME
    
    [django]
    recipe = djangorecipe
    project = my_project
    eggs =
        Django
        gmi.django.avatar
    
    control-script = django-admin
    settings = settings

Run buildout to checkout the sources and initialize an empty Django project.

.. code-block:: console

    $ ./bin/buildout

You will need to setup a Django project to use or hack the
gmi.django.profile application. If you have used the zc.buildout
based setup as described above, your Django settings file is
located at ./my_project/settings.py. Read setup for further
details. XXX
