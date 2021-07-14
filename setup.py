# Based on https://github.com/lRomul/argus/blob/37c1cade3b82a9bffc289894458d80cf1720532d/setup.py
import os
import io
import re
from setuptools import setup, find_packages


def read(*names, **kwargs):
    with io.open(os.path.join(os.path.dirname(__file__), *names),
                 encoding=kwargs.get("encoding", "utf8")) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="battery-handyman",
    version=find_version("battery_handyman", "__init__.py"),
    author="Nikolay Veld",
    author_email="novel8mail@gmail.com",
    url="https://github.com/NickVeld/battery_handyman",
    description="A customizable battery saving application.",
    long_description=read("README.rst"),
    long_description_content_type="text/x-rst",
    license="Apache 2.0",
    script=["bin/battery_handyman"],
    packages=find_packages(exclude=("tests", "tests.*",)),
    zip_safe=True,
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Other Audience",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Natural Language :: English",
        "Topic :: Desktop Environment",
        "Topic :: Home Automation",
        "Topic :: System",
        "Topic :: System :: Hardware",
        "Topic :: Utilities",
    ],
    install_requires=read("requirements.txt").split(),
)
