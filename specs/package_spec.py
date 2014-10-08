# -*- coding: utf-8 -*-

from expects import expect
from expects.testing import failure

from server_expects import *

from .constants import c


with describe('package'):
    with describe('be_installed'):
        with it('passes if package string is installed'):
            expect(c.AN_INSTALLED_PACKAGE_NAME).to(be_installed)

        with it('fails if package string is not installed'):
            with failure:
                expect(c.AN_UNINSTALLED_PACKAGE).to(be_installed)

        with it('passes if package is installed'):
            expect(package(c.AN_INSTALLED_PACKAGE_NAME)).to(be_installed)

        with it('passes if package version is installed'):
            expect(package(c.AN_INSTALLED_PACKAGE_NAME,
                           c.AN_INSTALLED_PACKAGE_VERSION)).to(be_installed)

        with it('fails if package is not installed'):
            with failure:
                expect(package(c.AN_UNINSTALLED_PACKAGE)).to(be_installed)
