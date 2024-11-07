import pathlib

import pkg_resources
import setuptools
from setuptools import setup

# loading requirements
try:
    from pip._internal.req import parse_requirements

    requirements = list(parse_requirements("requirements.txt", session='hack'))
    requirements = [r.requirement for r in requirements]
except AttributeError:
    with pathlib.Path("requirements.txt").open() as req:
        requirements = [str(r) for r in pkg_resources.parse_requirements(req)]

setup(
    name="cstr",
    version="1.0.0",
    description="",
    author="Planet Labs",
    include_package_data=True,
    test_suite="tests",
    install_requires=[
        "Click",
    ],
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    entry_points='''
        [console_scripts]
        cstr=cstr.cli:tool
    ''',
)
