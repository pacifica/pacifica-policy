#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Setup and install the policy."""
from os import path
from setuptools import setup, find_packages


setup(
    name='pacifica-policy',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description='Pacifica Policy Service',
    url='https://github.com/pacifica/pacifica-policy/',
    long_description=open(path.join(
        path.abspath(path.dirname(__file__)),
        'README.md')).read(),
    long_description_content_type='text/markdown',
    author='David Brown',
    author_email='dmlb2000@gmail.com',
    packages=find_packages(include=['pacifica.*']),
    namespace_packages=['pacifica'],
    entry_points={
        'console_scripts': [
            'pacifica-policy=pacifica.policy.__main__:main',
            'pacifica-policy-cmd=pacifica.policy.admin_cmd:main'
        ],
    },
    install_requires=[
        'backports.functools_lru_cache',
        'cherrypy',
        'pacifica-namespace',
        'python-dateutil',
        'requests'
    ]
)
