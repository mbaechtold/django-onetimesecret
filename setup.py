#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['onetimesecret', 'onetimesecret.migrations']

package_data = \
{'': ['*'],
 'onetimesecret': ['static/*',
                   'static/onetimesecret/*',
                   'static/onetimesecret/css/*',
                   'static/onetimesecret/images/*',
                   'templates/*',
                   'templates/onetimesecret/*']}

install_requires = \
['django-bootstrap4',
 'django-extensions',
 'cryptography',
 'django-model-utils',
 'pytz']

setup(name='django-onetimesecret',
      version='2018.1',
      description='django-onetimesecret',
      author='Martin Baechtold',
      author_email='nomail@localhost',
      url='https://github.com/mbaechtold/django-onetimesecret',
      packages=packages,
      package_data=package_data,
      install_requires=install_requires,
      python_requires='>=3.6',
     )