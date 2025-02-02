#!/usr/bin/env python3
# --------------------( LICENSE                           )--------------------
# Copyright (c) 2014-2022 Beartype authors.
# See "LICENSE" for further details.

'''
Project-wide **callable parameter tester utilities** (i.e., callables
introspectively validating and testing parameters accepted by arbitrary
callables).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                           }....................
from beartype.roar._roarexc import _BeartypeUtilCallableException
from beartype._util.func.utilfunccodeobj import get_func_codeobj
from beartype._data.datatyping import Codeobjable, TypeException
from collections.abc import Callable
from inspect import CO_VARARGS, CO_VARKEYWORDS
from typing import Dict

# See the "beartype.cave" submodule for further commentary.
__all__ = ['STAR_IMPORTS_CONSIDERED_HARMFUL']

# ....................{ PRIVATE                           }....................
_ARGS_DEFAULTS_KWONLY_EMPTY: Dict[str, object] = {}
'''
Empty dictionary suitable for use as the default dictionary mapping the name of
each optional keyword-only parameter accepted by a callable to the default
value assigned to that parameter.
'''

# ....................{ VALIDATORS                        }....................
#FIXME: Uncomment as needed.
# def die_unless_func_argless(
#     # Mandatory parameters.
#     func: Codeobjable,
#
#     # Optional parameters.
#     func_label: str = 'Callable',
#     exception_cls: Type[Exception] = _BeartypeUtilCallableException,
# ) -> None:
#     '''
#     Raise an exception unless the passed pure-Python callable is
#     **argument-less** (i.e., accepts *no* arguments).
#
#     Parameters
#     ----------
#     func : Codeobjable
#         Pure-Python callable, frame, or code object to be inspected.
#     func_label : str, optional
#         Human-readable label describing this callable in exception messages
#         raised by this validator. Defaults to ``'Callable'``.
#     exception_cls : type, optional
#         Type of exception to be raised if this callable is neither a
#         pure-Python function nor method. Defaults to
#         :class:`_BeartypeUtilCallableException`.
#
#     Raises
#     ----------
#     exception_cls
#         If this callable either:
#
#         * Is *not* callable.
#         * Is callable but is *not* pure-Python.
#         * Is a pure-Python callable accepting one or more parameters.
#     '''
#
#     # If this callable accepts one or more arguments, raise an exception.
#     if is_func_argless(
#         func=func, func_label=func_label, exception_cls=exception_cls):
#         assert isinstance(func_label, str), f'{repr(func_label)} not string.'
#         assert isinstance(exception_cls, type), (
#             f'{repr(exception_cls)} not class.')
#
#         raise exception_cls(
#             f'{func_label} {repr(func)} not argument-less '
#             f'(i.e., accepts one or more arguments).'
#         )


def die_unless_func_args_len_flexible_equal(
    # Mandatory parameters.
    func: Codeobjable,
    func_args_len_flexible: int,

    # Optional parameters.
    exception_cls: TypeException = _BeartypeUtilCallableException,
) -> None:
    '''
    Raise an exception unless the passed pure-Python callable accepts the
    passed number of **flexible parameters** (i.e., parameters passable as
    either positional or keyword arguments).

    Parameters
    ----------
    func : Codeobjable
        Pure-Python callable, frame, or code object to be inspected.
    func_args_len_flexible : int
        Number of flexible parameters to validate this callable as accepting.
    exception_cls : type, optional
        Type of exception to be raised if this callable is neither a
        pure-Python function nor method. Defaults to
        :class:`_BeartypeUtilCallableException`.

    Raises
    ----------
    exception_cls
        If this callable either:

        * Is *not* callable.
        * Is callable but is *not* pure-Python.
        * Is a pure-Python callable accepting either more or less than this
          Number of flexible parameters.
    '''
    assert isinstance(func_args_len_flexible, int)

    # Avoid circular import dependencies.
    from beartype._util.func.arg.utilfuncargget import (
        get_func_args_len_flexible)

    # Number of flexible parameters accepted by this callable.
    func_args_len_flexible_actual = get_func_args_len_flexible(
        func=func, exception_cls=exception_cls)

    # If this callable accepts more or less than this number of flexible
    # parameters, raise an exception.
    if func_args_len_flexible_actual != func_args_len_flexible:
        assert isinstance(exception_cls, type), (
            f'{repr(exception_cls)} not class.')
        raise exception_cls(
            f'Callable {repr(func)} flexible argument count '
            f'{func_args_len_flexible_actual} != {func_args_len_flexible}.'
        )

# ....................{ TESTERS ~ kind                    }....................
def is_func_argless(
    # Mandatory parameters.
    func: Codeobjable,

    # Optional parameters.
    exception_cls: TypeException = _BeartypeUtilCallableException,
) -> bool:
    '''
    ``True`` only if the passed pure-Python callable is **argument-less**
    (i.e., accepts *no* arguments).

    Parameters
    ----------
    func : Codeobjable
        Pure-Python callable, frame, or code object to be inspected.
    exception_cls : type, optional
        Type of exception to be raised in the event of fatal error. Defaults to
        :class:`_BeartypeUtilCallableException`.

    Returns
    ----------
    bool
        ``True`` only if the passed callable accepts *no* arguments.

    Raises
    ----------
    exception_cls
         If the passed callable is *not* pure-Python.
    '''

    # Code object underlying the passed pure-Python callable unwrapped.
    func_codeobj = get_func_codeobj(
        func=func, is_unwrapping=True, exception_cls=exception_cls)

    # Return true only if this callable accepts neither...
    return not (
        # One or more non-variadic arguments that are either standard or
        # keyword-only *NOR*...
        #
        # Note that both of the argument counts tested here ignore the
        # existence of variadic arguments, which is mildly frustrating... but
        # that's the backward-compatible hodgepodge that is the modern code
        # object for you.
        (func_codeobj.co_argcount + func_codeobj.co_kwonlyargcount > 0) or
        # One or more variadic arguments.
        is_func_arg_variadic(func_codeobj)
    )

# ....................{ TESTERS ~ kind : variadic         }....................
def is_func_arg_variadic(func: Codeobjable) -> bool:
    '''
    ``True`` only if the passed pure-Python callable accepts any **variadic
    parameters** and thus either variadic positional arguments (e.g.,
    "*args") or variadic keyword arguments (e.g., "**kwargs").

    Parameters
    ----------
    func : Union[Callable, CodeType, FrameType]
        Pure-Python callable, frame, or code object to be inspected.

    Returns
    ----------
    bool
        ``True`` only if the passed callable accepts either:

        * Variadic positional arguments (e.g., "*args").
        * Variadic keyword arguments (e.g., "**kwargs").

    Raises
    ----------
    _BeartypeUtilCallableException
         If the passed callable is *not* pure-Python.
    '''

    # Return true only if this callable declares either...
    #
    # We can't believe it's this simple, either. But it is.
    return (
        # Variadic positional arguments *OR*...
        is_func_arg_variadic_positional(func) or
        # Variadic keyword arguments.
        is_func_arg_variadic_keyword(func)
    )


def is_func_arg_variadic_positional(func: Codeobjable) -> bool:
    '''
    ``True`` only if the passed pure-Python callable accepts variadic
    positional arguments (e.g., "*args").

    Parameters
    ----------
    func : Union[Callable, CodeType, FrameType]
        Pure-Python callable, frame, or code object to be inspected.

    Returns
    ----------
    bool
        ``True`` only if the passed callable accepts variadic positional
        arguments.

    Raises
    ----------
    _BeartypeUtilCallableException
         If the passed callable is *not* pure-Python.
    '''

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # CAUTION: Synchronize with the iter_func_args() iterator.
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # Code object underlying the passed pure-Python callable unwrapped.
    func_codeobj = get_func_codeobj(func=func, is_unwrapping=True)

    # Return true only if this callable declares variadic positional arguments.
    return func_codeobj.co_flags & CO_VARARGS != 0


def is_func_arg_variadic_keyword(func: Codeobjable) -> bool:
    '''
    ``True`` only if the passed pure-Python callable accepts variadic
    keyword arguments (e.g., "**kwargs").

    Parameters
    ----------
    func : Union[Callable, CodeType, FrameType]
        Pure-Python callable, frame, or code object to be inspected.

    Returns
    ----------
    bool
        ``True`` only if the passed callable accepts variadic keyword
        arguments.

    Raises
    ----------
    _BeartypeUtilCallableException
         If the passed callable is *not* pure-Python.
    '''

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # CAUTION: Synchronize with the iter_func_args() iterator.
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # Code object underlying the passed pure-Python callable unwrapped.
    func_codeobj = get_func_codeobj(func=func, is_unwrapping=True)

    # Return true only if this callable declares variadic keyword arguments.
    return func_codeobj.co_flags & CO_VARKEYWORDS != 0

# ....................{ TESTERS ~ name                    }....................
#FIXME: *THIS TESTER IS HORRIFYINGLY SLOW*, thanks to a naive implementation
#deferring to the slow iter_func_args() iterator. A substantially faster
#get_func_arg_names() getter should be implemented instead and this tester
#refactored to call that getter. How? Simple:
#    def get_func_arg_names(func: Callable) -> Tuple[str]:
#        # A trivial algorithm for deciding the number of arguments can be
#        # found at the head of the iter_func_args() iterator.
#        args_len = ...
#
#        # One-liners for great glory.
#        return func.__code__.co_varnames[:args_len] # <-- BOOM
def is_func_arg_name(func: Callable, arg_name: str) -> bool:
    '''
    ``True`` only if the passed pure-Python callable accepts an argument with
    the passed name.

    Caveats
    ----------
    **This tester exhibits worst-case time complexity** ``O(n)`` **for** ``n``
    **the total number of arguments accepted by this callable,** due to
    unavoidably performing a linear search for an argument with this name is
    this callable's argument list. This tester should thus be called sparingly
    and certainly *not* repeatedly for the same callable.

    Parameters
    ----------
    func : Callable
        Pure-Python callable to be inspected.
    arg_name : str
        Name of the argument to be searched for.

    Returns
    ----------
    bool
        ``True`` only if that callable accepts an argument with this name.

    Raises
    ----------
    _BeartypeUtilCallableException
         If the passed callable is *not* pure-Python.
    '''
    assert isinstance(arg_name, str), f'{arg_name} not string.'

    # Avoid circular import dependencies.
    from beartype._util.func.arg.utilfuncargiter import iter_func_args

    # Return true only if...
    return any(
        # This is the passed name...
        arg_meta.name == arg_name
        # For the name of any parameter accepted by this callable.
        for arg_meta in iter_func_args(func)
    )
