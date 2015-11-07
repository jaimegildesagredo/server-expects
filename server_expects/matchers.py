# -*- coding: utf-8 -*-

from expects.matchers import Matcher, default_matcher

from .resources import (
    package as package_resource,
    host as host_resource,
    path as path_resource
)


class _be_installed(Matcher):
    def _match(self, package):
        package = self._resource_for(package)
        reasons = []
        if package.version is not None:
            reasons.append('{!r} version is installed'.format(package.current_version))

        # TODO: This error could be from a raised exception
        #       instead of this obscure state.
        if hasattr(package, 'failure_message'):
            reasons.append(package.failure_message)

        return package.is_installed, reasons

    def _resource_for(self, package):
        if hasattr(package, 'is_installed'):
            return package

        return package_resource(package)


class _be_reachable(Matcher):
    def _match(self, host):
        host = self._resource_for(host)

        reasons = []
        if not host.is_resolvable:
            reasons.append('cannot be resolved')

        return host.is_reachable, reasons

    def _resource_for(self, host):
        if hasattr(host, 'is_reachable'):
            return host

        return host_resource(host)


class _be_accessible(Matcher):
    def _match(self, instance):
        return instance.is_accessible, []


class _exists(Matcher):
    def _match(self, path):
        return self._resource_for(path).exists, []

    def _resource_for(self, path):
        if hasattr(path, 'exists'):
            return path

        return path_resource(path)


class _be_a_file(Matcher):
    def _match(self, path):
        path = self._resource_for(path)

        reasons = []
        if not path.exists:
            reasons.append('does not exist')

        if path.is_a_directory:
            reasons.append('is a directory')

        return path.is_a_file, reasons

    def _resource_for(self, path):
        if hasattr(path, 'exists'):
            return path

        return path_resource(path)


class _be_a_directory(Matcher):
    def _match(self, path):
        path = self._resource_for(path)

        reasons = []
        if not path.exists:
            reasons.append('does not exist')

        if path.is_a_file:
            reasons.append('is a file')

        return path.is_a_directory, reasons

    def _resource_for(self, path):
        if hasattr(path, 'exists'):
            return path

        return path_resource(path)


class have_owner(Matcher):
    def __init__(self, expected):
        self._expected = expected

    def _match(self, path):
        path = self._resource_for(path)

        reasons = []
        if not path.exists:
            reasons.append('does not exist')

        return default_matcher(self._expected)._match(path.owner)[0], reasons

    def _resource_for(self, path):
        if hasattr(path, 'exists'):
            return path

        return path_resource(path)


class have_group(Matcher):
    def __init__(self, expected):
        self._expected = expected

    def _match(self, path):
        path = self._resource_for(path)

        reasons = []
        if not path.exists:
            reasons.append('does not exist')

        return default_matcher(self._expected)._match(path.group)[0], reasons

    def _resource_for(self, path):
        if hasattr(path, 'exists'):
            return path

        return path_resource(path)


class have_mode(Matcher):
    def __init__(self, expected):
        self._expected = expected

    def _match(self, path):
        path = self._resource_for(path)

        reasons = []
        if not path.exists:
            reasons.append('does not exist')
        else:
            reasons.append('has mode {}'.format(oct(path.mode)))

        return default_matcher(self._expected)._match(path.mode)[0], reasons

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
