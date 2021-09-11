import functools
import types
import warnings

from typing import Optional


def unsafe(function: types.FunctionType, message: Optional[str] = None):
    """
    Decorator form for marking a function as unsafe.

    The warning can be suppressed in the safe context with warnings.catch_warnings
    This should be used sparingly at most.

    Parameters
    ----------
    message : Optional[str]
        The optional message used to warn that the function is unsafe.
        Defaults to "<function_name> is unsafe for use" if not provided.

    Examples
    --------
    .. testsetup::

        from redbot.core.utils.safety import unsafe

    .. doctest::

        >>> humanize_list(['One', 'Two', 'Three'])
        'One, Two, and Three'
        >>> humanize_list(['One'])
        'One'
        >>> humanize_list(['omena', 'peruna', 'aplari'], style='or', locale='fi')
        'omena, peruna tai aplari'
    """

    def wrapper(func):
        @functools.wraps(func)
        def get_wrapped(*args, **kwargs):
            actual_message = message or f"{func.__name__} is unsafe for use"
            warnings.warn(actual_message, stacklevel=3, category=RuntimeWarning)
            return func(*args, **kwargs)

        return get_wrapped

    return wrapper


def warn_unsafe(function: types.FunctionType, message: Optional[str] = None):
    """
    Function form to mark function from dependencies as unsafe for use.

    The warning can be suppressed in safe contexts with warnings.catch_warnings
    This should be used sparingly at most.

    .. warning:: There is no check that a function has already been modified.
        This form should only be used in init, if you want to mark an internal function
        as unsafe, use the decorator form above.

    Parameters
    ----------
    function : types.FunctionType
        The function to mark as unsafe.
    message : Optional[str]
        The optional message used to warn that the function is unsafe.
        Defaults to "<function_name> is unsafe for use" if not provided.
    """

    def wrapper(func):
        @functools.wraps(func)
        def get_wrapped(*args, **kwargs):
            actual_message = message or f"{func.__name__} is unsafe for use"
            warnings.warn(actual_message, stacklevel=3, category=RuntimeWarning)
            return func(*args, **kwargs)

        return get_wrapped

    return wrapper(function)
