import inspect
import sys
import threading
from functools import wraps
from typing import Any, Dict, Callable, Tuple, List

from pydilite.container import Container
from pydilite.exceptions import AlreadyInjectedException, ProviderNotConfiguredException
from pydilite.provider import Provider

test_frameworks: List[str] = [
    "pytest",
    "unittest",
    "nose2",
    "nose",
    "tox",
    "doctest",
    "unittest2",
    "twisted.trial",
]

_lock = threading.RLock()


def configure(
    provider: Provider,
    key: str = "default",
) -> None:
    """Configure provider to container

    Args:
        provider (Provider): The provider to configure
        key (str, optional): Key to assign to the provider. Defaults to "default".

    Raises:
        AlreadyInjectedException: launched if the provider is already configured
    """

    with _lock:
        if Container.get(key=key):
            raise AlreadyInjectedException

        Container.set(provider=provider, key=key)


def configure_after_clear(
    provider: Provider,
    key: str = "default",
) -> None:
    """Clear the existing provider and configure a new provider

    Args:
        provider (Provider): the provider to configure
        key (str, optional): key for the provider. Defaults to "default".
    """
    with _lock:
        if Container.get(key=key):
            clear()

        Container.set(provider=provider, key=key)


def clear(key: str = "default") -> None:
    """Clear the provider with the specified key

    Args:
        key (str, optional): provider key. Defaults to "default".
    """
    _container = Container

    with _lock:
        _container.clear(key=key)


def inject(**params: Dict[str, Any]):
    """Dependency injector decorator"""

    def inner_func(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(*args: Tuple[Any, ...], **kwargs: Dict[str, Any]):
            # TODO: Allow to manage multiple providers
            _provider = Container.get()
            if _provider:
                if not params:
                    _auto_inject(_provider, func, kwargs)
                else:
                    _manual_inject(params, kwargs)
            else:
                # Allow direct injection in tests
                if all(framework not in sys.modules for framework in test_frameworks):
                    raise ProviderNotConfiguredException

            if inspect.iscoroutinefunction(func):

                async def _inject(*args: Tuple[Any, ...], **kwargs: Dict[str, Any]):
                    return await func(*args, **kwargs)

            else:

                def _inject(*args: Tuple[Any, ...], **kwargs: Dict[str, Any]):
                    return func(*args, **kwargs)

            return _inject(*args, **kwargs)

        return wrapper

    return inner_func


def _auto_inject(
    provider: Any,
    func: Callable[..., Any],
    kwargs: Dict[str, Any],
):
    """Injects dependency automatically from the provider

    Args:
        provider (Any): _description_
        func (Callable[..., Any]): _description_
        kwargs (Dict[str, Any]): _description_
    """
    annotations = inspect.getfullargspec(func).annotations
    for k, v in annotations.items():
        if v in provider.bindings and k not in kwargs:
            _inject_replacement(k, provider.bindings[v], kwargs)


def _manual_inject(
    params: Dict[str, Any],
    kwargs: Dict[str, Any],
):
    """Injects dependency manually from the decorator parameters

    Args:
        params (Dict[str, Any]): _description_
        kwargs (Dict[str, Any]): _description_
    """
    for k, v in params.items():
        _inject_replacement(k, v, kwargs)


def _inject_replacement(
    key: str,
    replacement: Any,
    kwargs: Dict[str, Any],
):
    """Injects the replacement into the kwargs to later return the implemented class instance

    Args:
        key (str): _description_
        replacement (Any): _description_
        kwargs (Dict[str, Any]): _description_
    """
    if inspect.isclass(replacement):
        replacement = replacement()
    kwargs[key] = replacement


__all__ = [
    "Provider",
    "configure",
    "configure_after_clear",
    "inject",
]
