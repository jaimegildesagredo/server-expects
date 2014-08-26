# -*- coding: utf-8 -*-

import os
import re
import subprocess


def package(*args, **kwargs):
    return deb(*args, **kwargs)


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
    def __init__(self, name, version=None, virtualenv=None):
        self.name = name
        self.version = version
        self.virtualenv = virtualenv
        self._cache = {}

    def __repr__(self):
        return 'egg(name={}, version={}, virtualenv={})'.format(
            self.name, self.version, self.virtualenv)

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
        try:
            output = _run([self._pip, 'freeze'])
        except OSError:
            self.failure_message = ' but {} not found'.format(self._pip)
        else:
            for line in output.splitlines():
                if not line.startswith('#'):
                    yield self._parse_requirement(line)

    @property
    def _pip(self):
        if self.virtualenv is not None:
            return os.path.join(self.virtualenv, 'bin', 'pip')

        for path in ('/usr/local/bin/pip', '/usr/bin/pip'):
            if os.path.exists(path):
                break

        return path

    def _parse_requirement(self, line):
        if line.startswith('-e'):
            name, version = line.split('#egg=')[1].split('-', 1)
        else:
            name, version = line.split('==')

        return name.lower(), version


class host(object):
    def __init__(self, name):
        self.name = name

    @property
    def is_reachable(self):
        try:
            _run(['ping', '-w', '2', '-c', '2', self.name])
            return True
        except subprocess.CalledProcessError as error:
            if error.returncode == 2:
                self.failure_message = ' but cannot resolve name'

            return False


def _run(*args, **kwargs):
    kwargs.setdefault('stderr', open(os.devnull, 'w'))

    return subprocess.check_output(*args, **kwargs)

__all__ = ['package', 'deb', 'egg', 'host']
