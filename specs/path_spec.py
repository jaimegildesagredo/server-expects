# -*- coding: utf-8 -*-

from expects import expect
from expects.testing import failure

from server_expects import *

from .constants import c

with describe('path'):
    with describe('exists'):
        with it('passes if file path exists'):
            expect(c.AN_EXISTENT_FILE_PATH).to(exists)

        with it('passes if directory path exists'):
            expect(c.AN_EXISTENT_DIRECTORY_PATH).to(exists)

        with it('fails if path does not exist'):
            with failure:
                expect(c.A_NOT_EXISTENT_PATH).to(exists)

    with describe('be_a_file'):
        with it('passes if path is a file'):
            expect(c.AN_EXISTENT_FILE_PATH).to(be_a_file)

        with it('fails if path is a directory'):
            with failure(' but is a directory'):
                expect(c.AN_EXISTENT_DIRECTORY_PATH).to(be_a_file)

        with it('fails if path does not exist'):
            with failure(' but does not exist'):
                expect(c.A_NOT_EXISTENT_PATH).to(be_a_file)

    with describe('be_a_directory'):
        with it('passes if path is a directory'):
            expect(c.AN_EXISTENT_DIRECTORY_PATH).to(be_a_directory)

        with it('fails if path is a file'):
            with failure(' but is a file'):
                expect(c.AN_EXISTENT_FILE_PATH).to(be_a_directory)

        with it('fails if path does not exist'):
            with failure(' but does not exist'):
                expect(c.A_NOT_EXISTENT_PATH).to(be_a_directory)
