# -*- coding: utf-8 -*-

from expects.matchers import Matcher

from .resources import package as package_resource


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
            message = 'but {!r} version is installed'.format(package.current_version)

        if hasattr(package, 'failure_message'):
            message += package.failure_message

        return message


be_installed = _be_installed()

__all__ = ['be_installed']
