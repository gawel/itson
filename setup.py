# -*- coding: utf-8 -*-
import os
from setuptools import setup
from setuptools import find_packages

version = '0.1.dev0'


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name='itson',
    version=version,
    description="itson package",
    long_description=read('README.rst'),
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='',
    author='Gael Pasgrimaud',
    author_email='gael@gawel.org',
    url='https://github.com/gawel/itson/',
    license='MIT',
    packages=find_packages(exclude=['docs', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'tinydb',
        'requests',
        'bottle',
        'gevent',
        'chaussette',
    ],
    extras_require={
        'test': [
            'pytest', 'webtest',
        ],
    },
    entry_points="""
    [console_scripts]
    itson = itson:main
    itson-cron = itson.cron:main
    """,
)
