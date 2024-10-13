Whitespace
==========

.. image:: https://github.com/rzuckerm/whitespace-python/actions/workflows/makefile.yml/badge.svg
    :target: https://github.com/rzuckerm/whitespace-python/actions/workflows/makefile.yml
    :alt: Makefile CI

.. image:: https://img.shields.io/pypi/v/whitespace2.svg
    :target: https://pypi.org/project/whitespace2/
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/whitespace2
    :target: https://pypi.org/project/whitespace2/
    :alt: Python versions

.. image:: https://img.shields.io/pypi/wheel/whitespace2
    :target: https://pypi.org/project/whitespace2/
    :alt: Python wheel

An interpreter written in `Python <https://www.python.org/>`_ for the imperative, stack-based language called `Whitespace`_.
This is a fork of `<https://github.com/dwayne/whitespace-python>`_.

Installation
------------

To install, simply use pip (or `pipenv`_):

.. code-block:: bash

    $ pip install whitespace2

Usage
-----

Let :code:`program.ws` be any `Whitespace`_ program. To execute it, type:

.. code-block:: bash

    $ whitespace program.ws

You can find example `Whitespace`_ programs at `tests/fixtures <https://github.com/rzuckerm/whitespace-python/tree/master/test/fixtures>`_.

For example, here's the `factorial program <https://github.com/rzuckerm/whitespace-python/tree/master/test/fixtures/fact.ws>`_:

.. code-block:: bash

    $ whitespace fact.ws
    Enter a number: 40
    40! = 815915283247897734345611269596115894272000000000

Development
-----------

Recommended tools:

 - `poetry`_
 - `make <https://www.gnu.org/software/make/>`_

Clone the repository and install the dependencies:

.. code-block:: bash

    $ git clone git@github.com:rzuckerm/whitespace-python.git
    $ cd whitespace-python
    $ poetry env '<python-version>'
    $ poetry install

where `<python-version>` is the version of python that you have installed. This
must be at least python 3.8. Example for python 3.10:

.. code-block:: bash

    $ poetry env 3.10

You're now all set to begin development.

Formatting
----------

The code is formatted using `black`_.

Run the formatter:

.. code-block:: bash

    $ make format

Linting
-------

The code is linted using `black`_ and  `pylint`_.

Run the linters:

.. code-block:: bash

    $ make lint

Testing
-------

Tests are written using `pytest`_.

Run all tests.

.. code-block:: bash

    $ make test

Run a specific test module.

.. code-block:: bash

    $ make test PYTEST_ARGS="-vvl -m test.<my-module>"

Run a specific test case.

.. code-block:: bash

    $ make test PYTEST_ARGS="-vvl -k test.test_parser.ParserTestCase.test_it_parses_push"

Help
----

To get a list of make targets, run this:

.. code-block:: bash

    $ make help

References
----------

- `Whitespace tutorial <https://web.archive.org/web/20150618184706/http://compsoc.dur.ac.uk/whitespace/tutorial.php>`_

Credits
-------

Thanks to `Edwin Brady <https://edwinb.wordpress.com/>`_ and Chris Morris for designing/developing this programming language; they are also developers of the `Idris <https://en.wikipedia.org/wiki/Idris_(programming_language)>`_ programming language.

.. _Whitespace: https://en.wikipedia.org/wiki/Whitespace_(programming_language)
.. _pipenv: https://pipenv.pypa.io/en/stable/
.. _poetry: https://python-poetry.org/docs/
.. _pytest: https://docs.pytest.org/en/stable/
.. _black: https://black.readthedocs.io/en/stable/
.. _pylint: https://pylint.readthedocs.io/en/stable/
