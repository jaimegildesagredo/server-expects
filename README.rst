==============
Server Expects
==============

.. image:: https://img.shields.io/pypi/v/server-expects.svg
    :target: https://pypi.python.org/pypi/server-expects
    :alt: Latest version

.. image:: https://img.shields.io/pypi/dm/server-expects.svg
    :target: https://pypi.python.org/pypi/server-expects
    :alt: Number of PyPI downloads

.. image:: https://secure.travis-ci.org/jaimegildesagredo/server-expects.svg?branch=master
    :target: http://travis-ci.org/jaimegildesagredo/server-expects

Server-Expects is a `Serverpec <http://serverspec.org/>`_-like matchers library for the `Expects <https://github.com/jaimegildesagredo/expects>`_ assertion library. It provides matchers for testing server infrastructure.

Installation
============

You can install the last stable release from PyPI using *pip* or *easy_install*.

.. code-block:: bash

    $ pip install server-expects

Also you can install the latest sources from *Github*.

.. code-block:: bash

     $ pip install -e git+git://github.com/jaimegildesagredo/server-expects.git#egg=server-expects

Usage
=====

Just import the ``expect`` callable and the Server-Expects matchers and start writing assertions.

.. code-block:: python

    from expects import expect
    from server_expects import *

    expect('python').to(be_installed)

Matchers
========

TODO

Specs
=====

To run the specs you should install the testing requirements and then run ``mamba``.

.. code-block:: bash

    $ python setup.py develop
    $ pip install --upgrade -r test-requirements.txt
    $ mamba

License
=======

The Server-Expects is released under the `Apache2 license <http://www.apache.org/licenses/LICENSE-2.0.html>`_.
