from typing import Dict, Optional, Type

from pydilite.provider import Provider


class Container:
    """Dependency injection container.
    Allows to use several providers in the same application.

    """

    _providers: Dict[str, Provider] = {}

    @classmethod
    def set(cls: Type["Container"], provider: Provider, key: str = "default") -> None:
        """Set provider by key or default if none specified

        Args:
            cls (Type[&quot;Container&quot;]): Reference to container class
            provider (Provider): Provider instance
            key (str, optional): Provider key. Defaults to "default".
        """
        cls._providers[key] = provider

    @classmethod
    def get(cls: Type["Container"], key: str = "default") -> Optional[Provider]:
        """Get provider by key or default if none specified

        Args:
            cls (Type[&quot;Container&quot;]): Reference to container class
            key (str, optional): Key for the provider to recover. Defaults to "default".

        Returns:
            Optional[Provider]: Provider instance or None if not found
        """
        return cls._providers.get(key)

    @classmethod
    def clear(cls: Type["Container"], key: str = "default") -> None:
        """Celar the provider by key or default if none specified

        Args:
            cls (Type[&quot;Container&quot;]): Reference to container class
            key (str, optional): Key for the provider to clear. Defaults to "default".
        """
        if key in cls._providers:
            del cls._providers[key]
