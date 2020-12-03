#!/usr/bin/env python

import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

package_dir={'': 'src'}
packages = setuptools.find_packages(where='src')

install_requires = [
    'numpy',
    'matplotlib'
]

setuptools.setup(name='interactive_plotter',
                 version='0.1',
                 author='Dmitry Yershov',
                 author_email='dmitry.s.yershov@gmail.com',
                 description='Library for interactive plotting using matplotlib',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/dyershov/interactive-plotter",
                 package_dir=package_dir,
                 packages=packages,
                 install_requires=install_requires
                 )

