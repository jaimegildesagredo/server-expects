# -*- coding: utf-8 -*-

from expects.matchers import Matcher

from .resources import (
    package as package_resource,
    host as host_resource,
    path as path_resource
)


class _be_installed(Matcher):
    def _match(self, package):
        return self._resource_for(package).is_installed

    def _resource_for(self, package):
        if hasattr(package, 'is_installed'):
            return package

        return package_resource(package)

    def _description(self, package):
        package = self._resource_for(package)

        message = super(_be_installed, self)._description(package)

        if package.version is not None:
            message += ' but {!r} version is installed'.format(package.current_version)

        if hasattr(package, 'failure_message'):
            message += package.failure_message

        return message


class _be_reachable(Matcher):
    def _match(self, host):
        return self._resource_for(host).is_reachable

    def _resource_for(self, host):
        if hasattr(host, 'is_reachable'):
            return host

        return host_resource(host)

    def _description(self, host):
        host = self._resource_for(host)

        message = super(_be_reachable, self)._description(host)

        if not host.is_resolvable:
            message += ' but cannot be resolved'

        return message


class _be_accessible(Matcher):
    def _match(self, instance):
        return instance.is_accessible


class _exists(Matcher):
    def _match(self, path):
        return self._resource_for(path).exists

    def _resource_for(self, path):
        if hasattr(path, 'exists'):
            return path

        return path_resource(path)


class _be_a_file(Matcher):
    def _match(self, path):
        return self._resource_for(path).is_a_file

    def _description(self, path):
        path = self._resource_for(path)

        message = super(_be_a_file, self)._description(path)

        if not path.exists:
            message += ' but does not exist'

        if path.is_a_directory:
            message += ' but is a directory'

        return message

    def _resource_for(self, path):
        if hasattr(path, 'exists'):
            return path

        return path_resource(path)


class _be_a_directory(Matcher):
    def _match(self, path):
        return self._resource_for(path).is_a_directory

    def _description(self, path):
        path = self._resource_for(path)

        message = super(_be_a_directory, self)._description(path)

        if not path.exists:
            message += ' but does not exist'

        if path.is_a_file:
            message += ' but is a file'

        return message

    def _resource_for(self, path):
        if hasattr(path, 'exists'):
            return path

        return path_resource(path)


class have_owner(Matcher):
    def __init__(self, expected):
        self._expected = expected

    def _match(self, path):
        return self._expected == self._resource_for(path).owner

    def _description(self, path):
        path = self._resource_for(path)

        message = super(have_owner, self)._description(path)

        if not path.exists:
            message += ' but does not exist'

        return message

    def _resource_for(self, path):
        if hasattr(path, 'exists'):
            return path

        return path_resource(path)


class have_group(Matcher):
    def __init__(self, expected):
        self._expected = expected

    def _match(self, path):
        return self._expected == self._resource_for(path).group

    def _description(self, path):
        path = self._resource_for(path)

        message = super(have_group, self)._description(path)

        if not path.exists:
            message += ' but does not exist'

        return message

    def _resource_for(self, path):
        if hasattr(path, 'exists'):
            return path

        return path_resource(path)


class have_mode(Matcher):
    def __init__(self, expected):
        self._expected = expected

    def _match(self, path):
        return self._expected == self._resource_for(path).mode

    def _description(self, path):
        path = self._resource_for(path)

        message = 'have mode {}'.format(oct(self._expected))

        if not path.exists:
            message += ' but does not exist'
        else:
            message += ' but was {}'.format(oct(path.mode))

        return message

    def _resource_for(self, path):
        if hasattr(path, 'exists'):
            return path

        return path_resource(path)


be_installed = _be_installed()
be_reachable = _be_reachable()
be_accessible = _be_accessible()
exists = _exists()
be_a_file = _be_a_file()
be_a_directory = _be_a_directory()

__all__ = [
    'be_installed',
    'be_reachable',
    'be_accessible',
    'exists',
    'be_a_file',
    'be_a_directory',
    'have_owner',
    'have_group',
    'have_mode'
]
