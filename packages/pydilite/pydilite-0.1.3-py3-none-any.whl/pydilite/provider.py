from typing import Any, Optional, Type

from pydilite.exceptions import NotBoundedException


class Provider:
    """Dependency injection provider.
    Allows to bind and unbind classes to interfaces.
    """

    def __init__(self):
        self._bindings = {}

    def bind(
        self,
        interface: Optional[Type[Any]] = None,
        impl: Optional[Type[Any]] = None,
        lazy: bool = False,
    ) -> None:
        """Bind class to interface

        Args:
            interface (Optional[Type[Any]], optional): Interface to bound (abstract class or protocol). Defaults to None.
            impl (Optional[Type[Any]], optional): Implementation to bind to the interface. Defaults to None.
            lazy (bool, optional): Lazy initialization. Defaults to False.
        """

        if not lazy and impl is not None:
            impl = impl()

        self._bindings[interface] = impl

    def unbind(self, interface: Type[Any]) -> None:
        """Unbind interface if exists

        Args:
            interface (Type[Any]): Interface to unbound

        Raises:
            NotBoundedException: Raised if interface is not bounded
        """
        try:
            self._bindings.pop(interface)
        except KeyError:
            raise NotBoundedException(cls_name=interface.__class__.__name__)

    def clear_bindings(self) -> None:
        """Clear all bindings"""
        self._bindings = {}

    @property
    def bindings(self) -> dict:
        """Get all bindings

        Returns:
            dict: _description_
        """
        return self._bindings
