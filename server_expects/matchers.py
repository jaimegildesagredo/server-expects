# -*- coding: utf-8 -*-

from expects.matchers import Matcher


class _be_installed(Matcher):
    def _match(self, package):
        return package.is_installed

    def _description(self, package):
        message = super(_be_installed, self)._description(package)

        if package.version is not None:
            message = 'but {!r} version is installed'.format(package.current_version)

        return message


be_installed = _be_installed()

__all__ = ['be_installed']
