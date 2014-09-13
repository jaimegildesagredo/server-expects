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


with describe('mysql'):
    with describe('be_accessible'):
        with it('passes if instance is accessible by root without password'):
            expect(mysql(c.A_MYSQL_LISTENING_HOST)).to(be_accessible)

        with it('passes if instance is accessible by root without password on port'):
            expect(mysql(c.A_MYSQL_LISTENING_HOST,
                         port=int(c.A_MYSQL_LISTENING_PORT))).to(be_accessible)

        with it('passes if instance is accessible by user and password'):
            expect(mysql(c.A_MYSQL_LISTENING_HOST,
                         user=c.A_MYSQL_EXISTENT_USER,
                         password=c.A_MYSQL_VALID_PASSWORD)).to(be_accessible)

        with it('passes if database is accessible by user and password'):
            expect(mysql(c.A_MYSQL_LISTENING_HOST,
                         user=c.A_MYSQL_EXISTENT_USER,
                         password=c.A_MYSQL_VALID_PASSWORD,
                         database=c.A_MYSQL_EXISTENT_DATABASE)).to(be_accessible)

        with it('fails if instance is not listening on specified host'):
            with failure:
                expect(mysql(c.A_MYSQL_NOT_LISTENING_HOST)).to(be_accessible)

        with it('fails if instance is not listening on specified port'):
            with failure:
                expect(mysql(c.A_MYSQL_LISTENING_HOST,
                             port=int(c.A_MYSQL_NOT_LISTENING_PORT))).to(be_accessible)

        with it('fails if instance is not accessible by user'):
            with failure:
                expect(mysql(c.A_MYSQL_LISTENING_HOST,
                             user=c.A_MYSQL_NONEXISTENT_USER)).to(be_accessible)

        with it('fails if instance is not accessible by user and password'):
            with failure:
                expect(mysql(c.A_MYSQL_LISTENING_HOST,
                             user=c.A_MYSQL_EXISTENT_USER,
                             password=c.A_MYSQL_INVALID_PASSWORD)).to(be_accessible)

        with it('fails if database does not exist'):
            with failure:
                expect(mysql(c.A_MYSQL_LISTENING_HOST,
                             user=c.A_MYSQL_EXISTENT_USER,
                             password=c.A_MYSQL_VALID_PASSWORD,
                             database=c.A_MYSQL_NONEXISTENT_DATABASE)).to(be_accessible)

        with it('fails if database is not accessible by user and password'):
            with failure:
                expect(mysql(c.A_MYSQL_LISTENING_HOST,
                             user=c.A_MYSQL_NONEXISTENT_USER,
                             password=c.A_MYSQL_VALID_PASSWORD,
                             database=c.A_MYSQL_EXISTENT_DATABASE)).to(be_accessible)
