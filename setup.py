# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

requirements = open('requirements.txt').read().splitlines()
long_description = open('README.rst').read()

setup(
    name='server-expects',
    version='0.1.0',
    description='Serverspec-like Expects matchers library',
    long_description=long_description,
    url='https://github.com/jaimegildesagredo/server-expects',
    author='Jaime Gil de Sagredo Luna',
    author_email='jaimegildesagredo@gmail.com',
    license='Apache 2.0',
    packages=find_packages(exclude=['specs', 'specs.*']),
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Apache Software License'
    ]
)
