"""
@project: tinigine
@author: kang 
@github: https://github.com/fsksf 
@since: 2021/2/12 8:17 AM
"""

import os
import codecs
from distutils.core import setup


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='tinigine',
    version=read('tinigine/VERSION.txt'),
    packages=['tinigine', 'tinigine.core', 'tinigine.utils', 'tinigine.samples'],
    author='fsksf',
    author_email='timeless.go@foxmail.com',
    description='tini engine',
    package_data={'': ['*.*']},
    include_package_data=True,
    url='https://github.com/fsksf/tinigine',
    entry_points={
        "console_scripts": [
            "tinigine = tinigine.__main__:entry"
        ]
    },
    install_requires=read('requirements.txt')
)