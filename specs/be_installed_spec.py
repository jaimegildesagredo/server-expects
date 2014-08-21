# -*- coding: utf-8 -*-

import os
import re
import subprocess

from expects import expect
from expects.testing import failure
from expects.matchers import Matcher


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


class _be_installed(Matcher):
    def _match(self, package):
        return package.is_installed

    def _description(self, package):
        message = super(_be_installed, self)._description(package)

        if package.version is not None:
            message = 'but {!r} version is installed'.format(package.current_version)

        return message


class deb(object):
    def __init__(self, name, version=None):
        self.name = name
        self.version = version
        self._cache = {}

    @property
    def is_installed(self):
        if self.current_version is None:
            return False

        if self.version is None:
            return True

        return self.version == self.current_version

    @property
    def current_version(self):
        if not 'current_version' in self._cache:
            self._cache['current_version'] = self._get_current_version()
        return self._cache['current_version']

    def _get_current_version(self):
        output = run(['apt-cache', 'policy', self.name], env=self.__apt_env)

        match = re.search('Installed: (?P<version>.+)', output)

        if match is not None:
            version = match.group('version')

            if version != '(none)':
                return version

    @property
    def __apt_env(self):
        env = dict(os.environ)
        env['LANG'] = 'C'

        return env

def run(*args, **kwargs):
    return subprocess.check_output(*args, **kwargs)


be_installed = _be_installed()
