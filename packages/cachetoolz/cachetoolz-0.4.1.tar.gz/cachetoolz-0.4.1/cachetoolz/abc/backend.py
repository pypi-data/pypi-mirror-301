"""Abstract backend module."""

import logging
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import List, Optional

from ..log import get_logger


class BaseBackend:
    """
    Base abstract backend.

    Attributes
    ----------
    logger : logging.Logger
        Package logger.
    """

    def _separate_namespace(self, key: str) -> List[str]:
        """
        Separete the namespace with key_hash.

        Parameters
        ----------
        key : str
            Key with namespace and key_hash.

        Returns
        -------
        list[str]
            Separate namespace from cache identifier key.
        """
        return key.split(':')

    @property
    def logger(self) -> logging.Logger:
        """
        Get logger.

        Returns
        -------
        logging.Logger
            Package logger.
        """
        return get_logger()


class BackendABC(BaseBackend, ABC):
    """
    Abstract backend.

    Attributes
    ----------
    logger : logging.Logger
        Package logger.
    """

    @abstractmethod
    def get(self, key: str) -> Optional[str]:
        """
        Get a value if not expired.

        Parameters
        ----------
        key : str
            Cache identifier key.

        Returns
        -------
        with_cache : Any
            Value cached.
        without_cache : None
            If not exists or expired.
        """

    @abstractmethod
    def set(self, key: str, value: str, expires_at: timedelta) -> None:
        """
        Set a value with expires time.

        Parameters
        ----------
        key : str
            Cache identifier key.
        value : str
            Value to cache encoded.
        expires_at : datetime.timedelta
            Expiry time.
        """

    @abstractmethod
    def clear(self, namespace: str) -> None:
        """
        Clear a namespace.

        Parameters
        ----------
        namespace : str
            Namespace to cache.
        """


class AsyncBackendABC(BaseBackend, ABC):
    """
    Abstract async backend.

    Attributes
    ----------
    logger : logging.Logger
        Package logger.
    """

    @abstractmethod
    async def get(self, key: str) -> Optional[str]:
        """
        Get a value if not expired.

        Parameters
        ----------
        key : str
            Cache identifier key.

        Returns
        -------
        with_cache : Any
            Value cached.
        without_cache : None
            If not exists or expired.
        """

    @abstractmethod
    async def set(self, key: str, value: str, expires_at: timedelta) -> None:
        """
        Set a value with expires time.

        Parameters
        ----------
        key : str
            Ccache identifier key.
        value : str
            Value to cache encoded.
        expires_at : datetime.timedelta
            Expiry time.
        """

    @abstractmethod
    async def clear(self, namespace: str) -> None:
        """
        Clear a namespace.

        Parameters
        ----------
        namespace : str
            Namespace to cache.
        """
