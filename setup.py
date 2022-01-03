# -*- coding: utf-8 -*-

import sys
import fastentrypoints
from setuptools import find_packages, setup
if not sys.version_info[0] == 3:
    sys.exit("Python 3 is required. Use: \'python3 setup.py install\'")

dependencies = ["icecream", "click"]

config = {
    "version": "0.1",
    "name": "bytestool",
    "url": "https://github.com/jakeogh/bytestool",
    "license": "ISC",
    "author": "Justin Keogh",
    "author_email": "github.com@v6y.net",
    "description": "functions for parsing bytes",
    "long_description": __doc__,
    "packages": find_packages(exclude=['tests']),
    "package_data": {"bytestool": ['py.typed']},
    "include_package_data": True,
    "zip_safe": False,
    "platforms": "any",
    "install_requires": dependencies,
    "entry_points": {
        "console_scripts": [
            "bytestool=bytestool.bytestool:cli",
        ],
    },
}

setup(**config)