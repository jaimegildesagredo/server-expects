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

def _run(*args, **kwargs):
    return subprocess.check_output(*args, **kwargs)

__all__ = ['deb']
