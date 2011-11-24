# -*- coding: utf8 -*-
from setuptools import setup, find_packages


setup(
    name='django-revisionfield',
    version='0.2.0',
    description = 'An model field that auto increments every time the model is'
                  ' saved',

    author='Bradley Ayers',
    author_email='bradley.ayers@gmail.com',
    license='Simplified BSD',
    url='https://github.com/bradleyayers/django-revisionfield/',

    packages=find_packages(),

    install_requires=['Django >=1.2'],
    tests_require=['Django >=1.2', 'Attest >=0.4', 'django-attest >=0.2.2'],

    test_loader='tests:loader',
    test_suite='tests.everything',

    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
