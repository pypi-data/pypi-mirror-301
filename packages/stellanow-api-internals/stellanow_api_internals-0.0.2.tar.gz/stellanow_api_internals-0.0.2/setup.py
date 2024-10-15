"""
Copyright (C) 2022-2024 Stella Technologies (UK) Limited.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

import tomllib

from setuptools import find_packages, setup

from stellanow_api_internals._version import __version__


def get_install_requirements():
    try:
        # read my pipfile
        with open("Pipfile", "r") as fh:
            pipfile = fh.read()
        # parse the toml
        pipfile_toml = tomllib.loads(pipfile)
    except FileNotFoundError:
        return []
    # if the package's key isn't there then just return an empty list
    try:
        required_packages = pipfile_toml["packages"].items()
    except KeyError:
        return []
    # If a version/range is specified in the Pipfile honor it otherwise just list the package
    return ["{0}{1}".format(pkg, ver) if ver != "*" else pkg for pkg, ver in required_packages]


setup(
    name="stellanow_api_internals",
    description="Library for communicating with the internal API of StellaNow.",
    # long_description=open('README.public').read(),
    version=__version__,
    packages=find_packages(),
    python_requires=">=3.11",
    include_package_data=True,
    install_requires=get_install_requirements(),
)
