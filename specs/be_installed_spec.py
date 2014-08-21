# -*- coding: utf-8 -*-

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
    with context('deb package'):
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

    with context('egg package'):
        with it('passes if package is installed'):
            expect(egg(c.AN_INSTALLED_EGG_NAME)).to(be_installed)

        with it('passes if package version is installed'):
            expect(egg(c.AN_INSTALLED_EGG_NAME,
                       c.AN_INSTALLED_EGG_VERSION)).to(be_installed)

        with it('fails if package is not installed'):
            with failure:
                expect(egg(c.AN_UNINSTALLED_EGG)).to(be_installed)

        with it('fails if package with a different version is installed'):
            with failure('but {!r} version is installed'.format(c.AN_INSTALLED_EGG_VERSION)):
                expect(egg(c.AN_INSTALLED_EGG_NAME,
                           c.AN_UNINSTALLED_EGG_VERSION)).to(be_installed)
