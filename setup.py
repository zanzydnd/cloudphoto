#!/usr/bin/env python
# -*- coding:utf-8 -*-

import setuptools
import re

with open("src/cloudphoto/__init__.py", "r") as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
    ).group(1)

with open("README.md", "r") as fd:
    long_description = fd.read()

setuptools.setup(
    name="cloudphoto",
    version=version,
    description="Cloudphoto - works with s3 (cloudlab itis assigment)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/zanzydnd/cloudphoto',
    classifiers=["Programming Language :: Python :: 3"],
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    include_package_data=True,
    install_requires=["Jinja2", "boto3"],
    entry_points={
        "console_scripts": [
            "cloudphoto=cloudphoto.bin.run:main",
        ]
    },
)
