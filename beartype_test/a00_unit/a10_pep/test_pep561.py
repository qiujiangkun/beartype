#!/usr/bin/env python3
# --------------------( LICENSE                           )--------------------
# Copyright 2014-2021 by Cecil Curry.
# See "LICENSE" for further details.

'''
**Beartype** `PEP 561`_ **unit tests.**

This submodule unit tests `PEP 561`_ support implemented in the :mod:`beartype`
package.

.. _PEP 561:
   https://www.python.org/dev/peps/pep-0561
'''

# ....................{ IMPORTS                           }....................
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WARNING: To raise human-readable test errors, avoid importing from
# package-specific submodules at module scope.
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# ....................{ TESTS                             }....................
def test_pep561_pytyped() -> None:
    '''
    Test `PEP 561`_ support implemented in the :mod:`beartype` package by
    asserting that this package provides the ``py.typed`` file required by
    `PEP 561`_.

    Note that this unit test exercises a necessary but *not* sufficient
    condition for this package to comply with `PEP 561`_. The comparable
    :mod:`beartype_test.a90_func.pep.test_pep561` submodule defines a
    functional test exercising the remaining necessary condition: **the
    absence of static type-checking errors across this package.**

    .. _PEP 561:
       https://www.python.org/dev/peps/pep-0561
    '''

    # Defer heavyweight imports.
    import beartype
    from beartype._util.py.utilpymodule import get_module_filename
    from pathlib import Path

    # Concrete platform-agnostic path encapsulating the absolute filename of
    # the "beartype.__init__" submodule.
    #
    # Note that we intentionally do *NOT* obtain this file via the
    # test-specific "beartype_test._util.path.pytpathproject" submodule. Why?
    # Because we want to test that the "py.typed" file is actually being
    # installed with the "beartype" package, wherever that package may
    # currently be installed (e.g., to a "tox"-isolated venv).
    BEARTYPE_INIT_FILENAME = Path(get_module_filename(beartype))

    # Concrete platform-agnostic path encapsulating the absolute dirname of
    # the "beartype" package.
    BEARTYPE_DIRNAME = BEARTYPE_INIT_FILENAME.parent

    # Concrete platform-agnostic path encapsulating the "py.typed" file
    # bundled with the "beartype" package.
    #
    # Note that this path has *NOT* been validated to exist yet.
    BEARTYPE_INIT_FILE = BEARTYPE_DIRNAME.joinpath('py.typed')

    # Assert this file exists.
    assert BEARTYPE_INIT_FILE.is_file()