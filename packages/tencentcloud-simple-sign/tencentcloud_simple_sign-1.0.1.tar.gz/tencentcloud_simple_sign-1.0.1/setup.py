#!/usr/bin/env python

"""
distutils/setuptools install script.
"""
import os
from setuptools import setup, find_packages

import simple_sign

ROOT = os.path.dirname(__file__)

setup(
    name='tencentcloud-simple-sign',
    version=simple_sign.__version__,
    description='Tencent Cloud Simple Sign SDK for Python',
    author='Tencent Cloud',
    url='https://github.com/TencentCloud/simple-auth-sign-python',
    maintainer_email="tencentcloudapi@tencent.com",
    scripts=[],
    packages=find_packages(exclude=["examples*"]),
    license="Apache License 2.0",
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
