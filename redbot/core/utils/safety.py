import functools
import types
import warnings
from typing import Optional


def _get_wrapper(message):
    def inner(func):
        @functools.wraps(func)
        def get_wrapped(*args, **kwargs):
            actual_message = message or f"{func.__name__} is unsafe for use"
            warnings.warn(actual_message, stacklevel=3, category=RuntimeWarning)
            return func(*args, **kwargs)

        return get_wrapped

    return inner


def unsafe(message: Optional[str] = None):
    """
    Decorator form for marking a function as unsafe.
    Execution will still continue as normal, but with a warning.

    Parameters
    ----------
    message : Optional[str]
        The message included in the warning. Defaults to
        "[function_name] is unsafe for use"

    Returns
    -------
    types.FunctionType
        The wrapper for the decorator.

    Example
    -------

    .. code-block:: python

        @unsafe(message="This function isn't safe, use function2 instead")
        def function(*args, **kwargs) -> str:
            ...
    """

    return _get_wrapper(message)


def warn_unsafe(f: types.FunctionType, message: Optional[str] = None):
    """
    Function to mark function from dependencies as unsafe for use.
    Execution will still continue as normal, but with a warning.

    .. warning::
        There is no check that a function has already been modified.
        This form should only be used in init, if you want to mark an internal function
        as unsafe, use the decorator form above.

    Parameters
    ----------
    f : types.FunctionType
        The function to warn as unsafe for use.
    message : Optional[str]
        The message included in the warning. Defaults to
        "[function_name] is unsafe for use"

    Returns
    -------
    f : types.FunctionType
        The original function, which will now warn when used.

    Example
    -------

    .. code-block:: python

        def _function(*args, **kwargs) -> str:
            ...

        function = warn_unsafe(_function, "This function isn't safe, use function2 instead")
    """
    wrapper = _get_wrapper(message)
    return wrapper(f)
