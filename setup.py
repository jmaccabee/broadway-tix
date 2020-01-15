from setuptools import setup, find_packages
import os
# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open


def parse_requirements():
    requirements = [
        line.strip() for line in local_file("requirements.txt").splitlines()
    ]
    to_install = [requirement for requirement in requirements if requirement]
    return to_install


def local_file(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read()


setup(
    name='broadway-tix',  # Required
    version='0.0.1',  # Required
    description='Tool for finding reasonable ticket prices for a show at scale',  # Optional
    long_description_content_type='text/markdown',  # Optional
    url='https://github.com/jmaccabee/broadway-tix',  # Optional
    author='jmaccabee',  # Optional
    classifiers=[
        # Developed using Python 3.6.5,
        # but it's likely to work with other versions
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(where='app'),  # Required
    install_requires=parse_requirements(),  # Optional
)
