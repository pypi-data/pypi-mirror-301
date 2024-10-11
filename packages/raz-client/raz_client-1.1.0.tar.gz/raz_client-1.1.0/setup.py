# Copyright (c) 2023 Cloudera, Inc.  All Rights Reserved.
# This software and any associated use of this software is governed exclusively
# by the Cloudera Standard License included in the accompanying LICENSE.txt file or found at
# https://www.cloudera.com/legal/terms-and-conditions/cloudera-standard-license/cloudera-standard-license-v9-2019-12-12.html.

from setuptools import find_packages
from setuptools import setup
import codecs
import os

README_FILE = 'README.md'
REQUIREMENTS_FILE = 'requirements.txt'
INIT_FILE = 'raz_client/__init__.py'

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

def get_requirements():
    """
    Gets the prerequisite requirements for the package.
    """
    requirements = read(REQUIREMENTS_FILE)
    return requirements.splitlines()


def get_classifiers():
    """
    Gets the classifiers for the package.
    """
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
    return classifiers

setup(
    name='raz_client',
    description='boto3 plugin for S3 Ranger authorization',
    long_description=read(README_FILE),
    long_description_content_type='text/markdown',
    keywords='raz boto3',
    author='Cloudera, Inc.',
    license='Cloudera Standard License',
    url='https://www.cloudera.com/',
    classifiers=get_classifiers(),
    version=os.getenv('PACKAGE_VERSION'),
    packages=find_packages(exclude=['raz_client/test']),
    include_package_data=True,
    install_requires=get_requirements(),
    python_requires='>=3'
)