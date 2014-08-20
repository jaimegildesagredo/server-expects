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
            expect(deb(c.AN_INSTALLED_PACKAGE)).to(be_installed)

        with it('fails if package is no installed'):
            with failure:
                expect(deb(c.AN_UNINSTALLED_PACKAGE)).to(be_installed)


class _be_installed(Matcher):
    def _match(self, package):
        return package.is_installed


class deb(object):
    def __init__(self, name):
        self.name = name

    @property
    def is_installed(self):
        output = run(['apt-cache', 'policy', self.name], env=self.__apt_env)

        match = re.search('Installed: (?P<version>.+)', output)

        if match is not None:
            return match.group('version') != '(none)'

        return False

    @property
    def __apt_env(self):
        env = dict(os.environ)
        env['LANG'] = 'C'

        return env

def run(*args, **kwargs):
    return subprocess.check_output(*args, **kwargs)


be_installed = _be_installed()
