# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

from expects import expect
from expects.testing import failure

from server_expects import *


class Constants(object):
    def __init__(self, prefix):
        self._prefix = prefix

    def __getattr__(self, name):
        try:
            return os.environ[self._prefix + '_' + name]
        except KeyError:
            raise AttributeError(name)


c = Constants('TEST')


with describe('be_installed'):
    with it('passes if package is installed'):
        expect(c.AN_INSTALLED_PACKAGE_NAME).to(be_installed)

    with it('fails if package is not installed'):
        with failure:
            expect(c.AN_UNINSTALLED_PACKAGE).to(be_installed)

    with describe('package'):
        with it('passes if package is installed'):
            expect(package(c.AN_INSTALLED_PACKAGE_NAME)).to(be_installed)

        with it('passes if package version is installed'):
            expect(package(c.AN_INSTALLED_PACKAGE_NAME,
                           c.AN_INSTALLED_PACKAGE_VERSION)).to(be_installed)

        with it('fails if package is not installed'):
            with failure:
                expect(package(c.AN_UNINSTALLED_PACKAGE)).to(be_installed)

    with describe('deb'):
        with it('passes if package is installed'):
            expect(deb(c.AN_INSTALLED_DEB_NAME)).to(be_installed)

        with it('passes if package version is installed'):
            expect(deb(c.AN_INSTALLED_DEB_NAME,
                       c.AN_INSTALLED_DEB_VERSION)).to(be_installed)

        with it('fails if package is not installed'):
            with failure:
                expect(deb(c.AN_UNINSTALLED_DEB)).to(be_installed)

        with it('fails if package with a different version is installed'):
            with failure('but {!r} version is installed'.format(c.AN_INSTALLED_DEB_VERSION)):
                expect(deb(c.AN_INSTALLED_DEB_NAME,
                           c.AN_UNINSTALLED_DEB_VERSION)).to(be_installed)

    with describe('egg'):
        with it('passes if package is installed'):
            expect(egg(c.AN_INSTALLED_EGG_NAME)).to(be_installed)

        with it('passes if package version is installed'):
            expect(egg(c.AN_INSTALLED_EGG_NAME,
                       c.AN_INSTALLED_EGG_VERSION)).to(be_installed)

        with it('passes if editable package is installed'):
            expect(egg(c.AN_INSTALLED_EDITABLE_EGG_NAME)).to(be_installed)

        with it('passes if package is installed in virtualenv'):
            expect(egg(c.A_VIRTUALENV_INSTALLED_EGG,
                       virtualenv=c.A_VIRTUALENV_PATH)).to(be_installed)

        with it('fails if package is not installed'):
            with failure:
                expect(egg(c.AN_UNINSTALLED_EGG)).to(be_installed)

        with it('fails if package with a different version is installed'):
            with failure('but {!r} version is installed'.format(c.AN_INSTALLED_EGG_VERSION)):
                expect(egg(c.AN_INSTALLED_EGG_NAME,
                           c.AN_UNINSTALLED_EGG_VERSION)).to(be_installed)

        with it('fails if package is not installed in virtualenv'):
            with failure:
                expect(egg(c.A_VIRTUALENV_UNINSTALLED_EGG,
                           virtualenv=c.A_VIRTUALENV_PATH)).to(be_installed)

        with it('fails if virtualenv does not exist'):
            with failure('but {} not found'.format(_pip_path(c.A_NONEXISTENT_VIRTUALENV_PATH))):
                expect(egg(c.A_VIRTUALENV_INSTALLED_EGG,
                           virtualenv=c.A_NONEXISTENT_VIRTUALENV_PATH)).to(be_installed)


def _pip_path(prefix):
    return os.path.join(prefix, 'bin', 'pip')
