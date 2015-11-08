from setuptools import setup, find_packages
import sys, os

version = '0.1'

requires = [
    'Django',
    'setuptools'
]

setup(name='gmi.django.avatar',
      version=version,
      description="Collect avatars for registered users from external resources.",
      long_description="""\
XXX long description""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='django avatar',
      author='Stefan Walluhn',
      author_email='stefan@neuland.io',
      url='',
      license='GPLv3',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      namespace_packages=['gmidjango'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
