# -*- coding: utf-8 -*-

import os

from expects import expect
from expects.testing import failure

from server_expects import *


class Constants(object):
    def __init__(self, prefix):
        self._prefix = prefix

    def __getattr__(self, name):
        try:
            return os.environ[self._prefix + '_' + name]
        except KeyError:
            raise AttributeError(name)


c = Constants('TEST')


with describe('https'):
    with describe('be_accessible'):
        with it('passes if host is accessible on default port'):
            expect(https(c.A_HTTPS_LISTENING_HOST)).to(be_accessible)

        with it('passes if host is accessible on specified port'):
            expect(https(c.A_HTTPS_LISTENING_HOST,
                        port=int(c.A_HTTPS_LISTENING_PORT))).to(be_accessible)

        with it('passes if host is accessible on specified path'):
            expect(https(c.A_HTTPS_LISTENING_HOST,
                        path=c.A_HTTPS_EXISTENT_PATH)).to(be_accessible)

        with it('fails if host is not accessible on default port'):
            with failure:
                expect(https(c.A_HTTPS_NOT_LISTENING_HOST)).to(be_accessible)

        with it('fails if host is not accessible on specified port'):
            with failure:
                expect(https(c.A_HTTPS_LISTENING_HOST,
                            port=int(c.A_HTTPS_NOT_LISTENING_PORT))).to(be_accessible)

        with it('fails if host is not accessible on specified path'):
            with failure:
                expect(https(c.A_HTTPS_LISTENING_HOST,
                            path=c.A_HTTPS_NOT_EXISTENT_PATH)).to(be_accessible)
