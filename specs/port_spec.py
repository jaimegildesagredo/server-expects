# -*- coding: utf-8 -*-

from expects import expect
from expects.testing import failure

from server_expects import *

from .constants import c


with describe('port'):
    with describe('be_accessible'):
        with it('passes if local tcp port is listening'):
            expect(int(c.A_LOCAL_LISTENING_TCP_PORT)).to(be_listening)

        with it('passes if local udp port is listening'):
            expect(int(c.A_LOCAL_LISTENING_UDP_PORT)).to(be_listening)

        with it('fails if local port is not listening'):
            with failure:
                expect(int(c.A_LOCAL_NOT_LISTENING_PORT)).to(be_listening)


#with describe('http'):
    #with describe('be_accessible'):
        #with it('passes if host is accessible on default port'):
            #expect(http(c.A_HTTP_LISTENING_HOST)).to(be_accessible)

        #with it('passes if host is accessible on specified port'):
            #expect(http(c.A_HTTP_LISTENING_HOST,
                        #port=int(c.A_HTTP_LISTENING_PORT))).to(be_accessible)

        #with it('passes if host is accessible on specified path'):
            #expect(http(c.A_HTTP_LISTENING_HOST,
                        #path=c.A_HTTP_EXISTENT_PATH)).to(be_accessible)

        #with it('fails if host is not accessible on default port'):
            #with failure:
                #expect(http(c.A_HTTP_NOT_LISTENING_HOST)).to(be_accessible)

        #with it('fails if host is not accessible on specified port'):
            #with failure:
                #expect(http(c.A_HTTP_LISTENING_HOST,
                            #port=int(c.A_HTTP_NOT_LISTENING_PORT))).to(be_accessible)

        #with it('fails if host is not accessible on specified path'):
            #with failure:
                #expect(http(c.A_HTTP_LISTENING_HOST,
                            #path=c.A_HTTP_NOT_EXISTENT_PATH)).to(be_accessible)
