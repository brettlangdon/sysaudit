from setuptools import setup
from distutils.core import Extension

setup(
    name="sysaudit",
    version="0.1.0",
    description="Backport module for sys.audit and sys.addaudithook from Python 3.8",
    author="Brett Langdon",
    author_email="me@brett.is",
    url="https://github.com/brettlangdon/sysaudit",
    ext_modules=[
        Extension(
            "sysaudit.csysaudit", sources=["sysaudit/_csysaudit.c"], optional=True
        ),
    ],
    packages=["sysaudit"],
)
