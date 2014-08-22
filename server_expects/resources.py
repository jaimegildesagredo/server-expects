# -*- coding: utf-8 -*-

import os
import re
import subprocess


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
        output = _run(['apt-cache', 'policy', self.name], env=self.__apt_env)

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


class egg(object):
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
        for name, version in self._installed:
            if name == self.name:
                return version

    @property
    def _installed(self):
        output = _run([self._pip, 'freeze'])

        for line in output.splitlines():
            if not line.startswith('#'):
                yield self._parse_requirement(line)

    @property
    def _pip(self):
        for path in ('/usr/local/bin/pip', '/usr/bin/pip'):
            if os.path.exists(path):
                break

        return path

    def _parse_requirement(self, line):
        if '-e' in line:
            name, version = line.split('#egg=')[1].split('-', 1)
        else:
            name, version = line.split('==')

        return name.lower(), version

def _run(*args, **kwargs):
    return subprocess.check_output(*args, **kwargs)

__all__ = ['deb', 'egg']
