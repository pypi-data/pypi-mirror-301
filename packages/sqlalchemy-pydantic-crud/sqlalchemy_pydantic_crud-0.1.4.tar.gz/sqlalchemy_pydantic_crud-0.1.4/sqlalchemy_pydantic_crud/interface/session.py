from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession


class SessionProviderInterface(Protocol):
    def session(self) -> AsyncSession:
        raise NotImplementedError