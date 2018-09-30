#!/usr/bin/env python3

from setuptools import setup


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    author='Filip Krestan',
    author_email='krestfi1@fit.cvut.cz',
    description='Flask application generating expected netowrk utilization profile based on historical data.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    name='network_profile',
    url='https://github.com/fkrestan/network_profile',
    version='0.0.1',
    packages=['network_profile'],
    install_requires=["fbprophet>=0.0.0", "flask>=1.0.0", "uwsgi>=2.0.0"],
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Education",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Security",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Networking",
    ),
)
