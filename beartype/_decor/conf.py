#!/usr/bin/env python3
# --------------------( LICENSE                           )--------------------
# Copyright (c) 2014-2021 Beartype authors.
# See "LICENSE" for further details.

'''
**Beartype decorator configuration API** (i.e., enumerations, classes,
singletons, and other attributes enabling external callers to selectively
configure the :func:`beartype` decorator on a fine-grained per-decoration call
basis).

Most of the public attributes defined by this private submodule are explicitly
exported to external callers in our top-level :mod:`beartype.__init__`
submodule. This private submodule is *not* intended for direct importation by
downstream callers.
'''

# ....................{ IMPORTS                           }....................
from enum import (
    Enum,
    auto as next_enum_member_value,
    unique as die_unless_enum_member_values_unique,
)

# ....................{ ENUMERATIONS                      }....................
#FIXME: Unit test us up, please.
@die_unless_enum_member_values_unique
class BeartypeStrategy(Enum):
    '''
    Enumeration of all kinds of **container type-checking strategies** (i.e.,
    competing procedures for type-checking items of containers passed to or
    returned from :func:`beartype.beartype`-decorated callables, each with
    concomitant benefits and disadvantages with respect to runtime complexity
    and quality assurance).

    Strategies are intentionally named according to `conventional Big O
    notation <Big O_>`__ (e.g., :attr:`BeartypeStrategy.On` enables the
    ``O(n)`` strategy). Strategies are established per-decoration at the
    fine-grained level of callables decorated by the :func: `beartype.beartype`
    decorator by either:

    * Calling a high-level convenience decorator establishing that strategy
      (e.g., :func:`beartype.conf.beartype_On`, enabling the ``O(n)`` strategy
      for all callables decorated by that decorator).
    * Setting the :attr:`BeartypeConfiguration.strategy` variable of the
      :attr:`BeartypeConfiguration` object passed as the optional ``conf``
      parameter to the lower-level core :func: `beartype.beartype` decorator.

    Strategies enforce and guarantee their corresponding runtime complexities
    (e.g., ``O(n)``) across all type checks performed for all callables
    enabling those strategies. For example, a callable decorated with the
    :attr:`BeartypeStrategy.On` strategy will exhibit linear runtime complexity
    as its type-checking overhead.

    .. _Big O:
       https://en.wikipedia.org/wiki/Big_O_notation

    Attributes
    ----------
    O0 : EnumMemberType
        **No-time strategy** (i.e, disabling type-checking for a callable by
        reducing :func:`beartype.beartype` to the identity decorator for that
        callable). Although currently useless, this strategy will usefully
        allow end users to selectively prevent callables from being
        type-checked by our as-yet-unimplemented import hook. When implemented,
        that hook will type-check *all* callables in a given package by
        default. Some means is needed to prevent that from happening for select
        callables. This is that means.
    O1 : EnumMemberType
        **Constant-time strategy** (i.e., our default ``O(1)`` strategy
        type-checking a single randomly selected item of a container that you
        currently enjoy). Since this is the default, this strategy need *not*
        be explicitly configured.
    Ologn : EnumMemberType
        **Logarithmic-time strategy** (i.e., an ``O(lgn)` strategy
        type-checking a randomly selected number of items ``j`` of a container
        ``obj`` such that ``j = len(obj)``. This strategy is **currently
        unimplemented.** (*To be implemented by a future beartype release.*)
    On : EnumMemberType
        **Linear-time strategy** (i.e., an ``O(n)`` strategy type-checking
        *all* items of a container. This strategy is **currently
        unimplemented.** (*To be implemented by a future beartype release.*)
    '''

    O0 = next_enum_member_value()
    O1 = next_enum_member_value()
    Ologn = next_enum_member_value()
    On = next_enum_member_value()

# ....................{ CLASSES                           }....................
#FIXME: *INSUFFICIENT.* Critically, we also *MUST* declare a __new__() method
#to enforce memoization. A new "BeartypeConfiguration" instance is instantiated
#*ONLY* if no existing instance with the same settings has been previously
#instantiated; else, an existing cached instance is reused. This is essential,
#as the @beartype decorator itself memoizes on the basis of this instance. See
#the following StackOverflow post for the standard design pattern:
#    https://stackoverflow.com/a/13054570/2809027
#
#Note, however, that there's an intriguing gotcha:
#    "When you define __new__, you usually do all the initialization work in
#     __new__; just don't define __init__ at all."
#
#Why? Because if you define both __new__() and __init__() then Python
#implicitly invokes *BOTH*, even if the object returned by __new__() has
#already been previously initialized with __init__(). This is a facepalm
#moment, although the rationale does indeed make sense. Ergo, we *ONLY* want to
#define __new__(); the existing __init__() should simply be renamed __new__()
#and generalized from there to support caching.
#FIXME: Unit test us up, please.
#FIXME: Document us up, please.
class BeartypeConfiguration(object):
    '''
    * An `is_debug` boolean instance variable. When enabled, `@beartype`
      emits debugging information for the decorated callable – including
      the code for the wrapper function dynamically generated by
      `@beartype` that type-checks that callable.
    * A `strategy` instance variable whose value must be a
      `BeartypeStrategy` enumeration member. This is how you notify
      `@beartype` of which strategy to apply to each callable.
    '''

    is_debug: bool
    strategy: BeartypeStrategy

    def __init__(
       self,
       is_debug: bool = False,
       strategy: BeartypeStrategy = BeartypeStrategy.O1,
    ) -> None:

        #FIXME: Implement actual validation, please.
        if not isinstance(is_debug, bool):
            raise ValueError()
        if not isinstance(strategy, BeartypeStrategy):
            raise ValueError()

        self.is_debug = is_debug
        self.strategy = strategy

# ....................{ SINGLETONS                        }....................
#FIXME: Unit test us up, please.
#FIXME: Document us up, please. Note this attribute is intentionally *NOT*
#exported from "beartype.__init__".
BEAR_CONF_DEFAULT = BeartypeConfiguration()