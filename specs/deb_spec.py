# -*- coding: utf-8 -*-

from expects import expect
from expects.testing import failure

from server_expects import *

from .constants import c


with describe('deb'):
    with describe('be_installed'):
        with it('passes if package is installed'):
            expect(deb(c.AN_INSTALLED_DEB_NAME)).to(be_installed)

        with it('passes if package version is installed'):
            expect(deb(c.AN_INSTALLED_DEB_NAME,
                       c.AN_INSTALLED_DEB_VERSION)).to(be_installed)

        with it('fails if package is not installed'):
            with failure:
                expect(deb(c.AN_UNINSTALLED_DEB)).to(be_installed)

        with it('fails if package with a different version is installed'):
            with failure('{!r} version is installed'.format(c.AN_INSTALLED_DEB_VERSION)):
                expect(deb(c.AN_INSTALLED_DEB_NAME,
                           c.AN_UNINSTALLED_DEB_VERSION)).to(be_installed)
