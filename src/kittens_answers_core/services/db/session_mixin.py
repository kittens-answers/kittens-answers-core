from sqlalchemy.ext.asyncio import AsyncSession


class SessionMixin:
    session: AsyncSession

    def delete_session(self) -> None:
        delattr(self, "session")
