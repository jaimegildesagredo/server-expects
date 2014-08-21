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
            expect(deb(c.AN_INSTALLED_PACKAGE_NAME)).to(be_installed)

        with it('passes if package version is installed'):
            expect(deb(c.AN_INSTALLED_PACKAGE_NAME,
                       c.AN_INSTALLED_PACKAGE_VERSION)).to(be_installed)

        with it('fails if package is not installed'):
            with failure:
                expect(deb(c.AN_UNINSTALLED_PACKAGE)).to(be_installed)

        with it('fails if package with a different version is installed'):
            with failure('but {!r} version is installed'.format(c.AN_INSTALLED_PACKAGE_VERSION)):
                expect(deb(c.AN_INSTALLED_PACKAGE_NAME,
                           c.AN_UNINSTALLED_PACKAGE_VERSION)).to(be_installed)
