# -*- coding: utf-8 -*-

import os
import re
import pwd
import grp
import socket
import subprocess


def package(*args, **kwargs):
    return deb(*args, **kwargs)


class deb(object):
    def __init__(self, name, version=None):
        self.name = name
        self.version = version
        self._cache = {}

    def __repr__(self):
        return 'deb(name={!r}, version={!r})'.format(
            self.name, self.version)

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
        output = _run(['apt-cache', 'policy', self.name])

        match = re.search('Installed: (?P<version>.+)', output)

        if match is not None:
            version = match.group('version')

            if version != '(none)':
                return version


class egg(object):
    def __init__(self, name, version=None, virtualenv=None):
        self.name = name
        self.version = version
        self.virtualenv = virtualenv
        self._cache = {}

    def __repr__(self):
        return 'egg(name={!r}, version={!r}, virtualenv={!r})'.format(
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

    def __repr__(self):
        return 'host(name={!r})'.format(self.name)

    @property
    def is_reachable(self):
        try:
            _run(['ping', '-w', '2', '-c', '2', self.name])
        except subprocess.CalledProcessError:
            return False

        return True

    @property
    def is_resolvable(self):
        try:
            socket.getaddrinfo(self.name, None)
        except socket.gaierror as e:
            if e.errno == socket.EAI_NONAME:
                return False

        return True


class mysql(object):
    def __init__(self, host, port=3306, user='root', password='', database=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def __repr__(self):
        return 'mysql(host={!r}, port={!r}, user={!r}, password={!r}, database={!r})'.format(
            self.host, self.port, self.user, self.password, self.database)

    @property
    def is_accessible(self):
        return self._connection is not None

    @property
    def _connection(self):
        import pymysql

        try:
            return pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                passwd=self.password,
                db=self.database)

        except pymysql.OperationalError:
            pass


class http(object):
    def __init__(self, host, port=80, path='', timeout=1):
        self.host = host
        self.port = port
        self.path = path
        self.timeout = timeout

    @property
    def is_accessible(self):
        import requests

        try:
            response = requests.get(self._uri, timeout=self.timeout)
        except requests.ConnectionError:
            return False

        return response.status_code == 200

    @property
    def _uri(self):
        return 'http://{host}:{port}/{path}'.format(
            host=self.host, port=self.port, path=self.path)

    def __repr__(self):
        return 'http(uri={uri})'.format(uri=self._uri)


class https(object):
    def __init__(self, host, port=443, path='', timeout=1):
        self.host = host
        self.port = port
        self.path = path
        self.timeout = timeout

    @property
    def is_accessible(self):
        import requests

        try:
            response = requests.get(self._uri, timeout=self.timeout)
        except requests.ConnectionError:
            return False

        return response.status_code == 200

    @property
    def _uri(self):
        return 'https://{host}:{port}/{path}'.format(
            host=self.host, port=self.port, path=self.path)

    def __repr__(self):
        return 'https(uri={uri})'.format(uri=self._uri)


class path(object):
    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return 'path({!r})'.format(self.path)

    @property
    def exists(self):
        return os.path.exists(self.path)

    @property
    def is_a_file(self):
        return os.path.isfile(self.path)

    @property
    def is_a_directory(self):
        return os.path.isdir(self.path)

    @property
    def owner(self):
        if self.exists:
            return pwd.getpwuid(os.stat(self.path).st_uid).pw_name

    @property
    def group(self):
        if self.exists:
            return grp.getgrgid(os.stat(self.path).st_gid).gr_name

    @property
    def mode(self):
        if self.exists:
            return os.stat(self.path).st_mode & 0o777


def _run(*args):
    env = dict(os.environ)
    env['LANG'] = 'C'

    kwargs = {
        'stderr': open(os.devnull, 'w'),
        'env': env
    }
    return subprocess.check_output(*args, **kwargs).decode('ascii')

__all__ = ['package', 'deb', 'egg', 'host', 'mysql', 'http', 'https', 'path']
