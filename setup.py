from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

__author__ = 'Tim Martin'
__pkg_name__ = 'django-version'

from setuptools import setup, find_packages

version = '0.1.1'

setup(
    author=__author__,
    author_email='tim.martin@vertical-knowledge.com',
    name='django-ripozo',
    version=version,
    packages=find_packages(include=['django_ripozo', 'django_ripozo.*']),
    include_package_data=True,
    description=('Integrates ripozo with django for fast, '
                 'flexible Hypermedia, HATEOAS, and other REST apis'),
    install_requires=[
        'ripozo',
        'Django>=1.4',
        'six'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django :: 1.5',
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
        'ripozo-tests'
    ],
    test_suite='django_ripozo_tests'
)