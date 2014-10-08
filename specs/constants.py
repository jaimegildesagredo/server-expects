# -*- coding: utf-8 -*-

import os


class Constants(object):
    def __init__(self, prefix):
        self._prefix = prefix

    def __getattr__(self, name):
        try:
            value = os.environ[self._prefix + '_' + name]
        except KeyError:
            raise AttributeError(name)

        if isinstance(value, bytes):
            value = value.decode('ascii')

        return value


c = Constants('TEST')
