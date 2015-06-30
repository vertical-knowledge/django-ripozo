from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
# from __future__ import unicode_literals

__author__ = 'Tim Martin'

from setuptools import setup

version = '1.0.1.dev0'

setup(
    author=__author__,
    author_email='tim.martin@vertical-knowledge.com',
    name='django-ripozo',
    version=version,
    packages=[
        'django_ripozo',
        'django_ripozo.migrations'
    ],
    # include_package_data=True,
    description=('Integrates ripozo with django for fast, '
                 'flexible Hypermedia, HATEOAS, and other REST apis'),
    install_requires=[
        'ripozo',
        'Django>=1.4',
        'six'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    tests_require=[
        'mock',
        'unittest2'
    ],
    test_suite='django_ripozo_tests',
    url='http://django-ripozo.readthedocs.org/'
)
