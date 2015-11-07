# -*- coding: utf-8 -*-

from expects import expect
from expects.testing import failure

from server_expects import *

from .constants import c


with describe('host'):
    with describe('be_reachable'):
        with it('passes if ip string is reachable'):
            expect(c.A_REACHABLE_IP).to(be_reachable)

        with it('passes if host string is reachable'):
            expect(c.A_REACHABLE_HOST).to(be_reachable)

        with it('passes if ip is reachable'):
            expect(host(c.A_REACHABLE_IP)).to(be_reachable)

        with it('fails if ip string is not reachable'):
            with failure:
                expect(c.AN_UNREACHABLE_IP).to(be_reachable)

        with it('fails if host string is not reachable'):
            with failure:
                expect(c.AN_UNREACHABLE_HOST).to(be_reachable)

        with it('fails if host string cannot be resolved'):
            with failure('cannot be resolved'):
                expect(c.AN_UNRESOLVABLE_HOST).to(be_reachable)

        with it('fails if host ip is not reachable'):
            with failure:
                expect(host(c.AN_UNREACHABLE_IP)).to(be_reachable)

        with it('passes if host is reachable'):
            expect(host(c.A_REACHABLE_HOST)).to(be_reachable)

        with it('fails if host is not reachable'):
            with failure:
                expect(host(c.AN_UNREACHABLE_HOST)).to(be_reachable)

        with it('fails if host cannot be resolved'):
            with failure('cannot be resolved'):
                expect(host(c.AN_UNRESOLVABLE_HOST)).to(be_reachable)
