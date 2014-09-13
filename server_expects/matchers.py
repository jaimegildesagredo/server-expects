# -*- coding: utf-8 -*-

from expects.matchers import Matcher

from .resources import (
    package as package_resource,
    host as host_resource
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

be_installed = _be_installed()
be_reachable = _be_reachable()
be_accessible = _be_accessible()

__all__ = ['be_installed', 'be_reachable', 'be_accessible']
