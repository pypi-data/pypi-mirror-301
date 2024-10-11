#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def get_install_requirements():
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        reqs = [x.strip() for x in f.read().splitlines()]
    reqs = [x for x in reqs if not x.startswith('#')]
    return reqs

setup(
    name='easycreditscoring',
    version='0.0.2',
    description='Simple library combining efficient credit scoring ML methods',
    author='miosipof',
    packages=find_packages(),
    install_requires=get_install_requirements(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    # test_suite='tests',
)