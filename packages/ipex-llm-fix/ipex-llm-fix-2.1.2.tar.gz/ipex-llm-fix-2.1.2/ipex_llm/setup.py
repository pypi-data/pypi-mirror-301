import os
import re
from setuptools import setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """    
    return "2.1.1"


def get_long_description(long_description_file):
    with open(long_description_file) as f:
        long_description = f.read()

    return long_description


version = get_version('ipex-llm-fix')


setup(
    name='ipex-llm-fix',
    version=version,
    url='https://github.com/intel-analytics/ipex-llm',
    license='Apache-2.0 license',
    author='Intel',
    author_email='dep36@qq.com',
    description='ipex-llm fix version',
    long_description="ipex-llm fix",
    long_description_content_type='text/markdown',
    packages=['ipex-llm-fix'],
    zip_safe=False,
    platforms='any',
    install_requires=[       
    ],
    classifiers=[     
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
   
)
