from datetime import timedelta
from uuid import UUID

from injection import injectable

from hundred.ctx.auth.aliases import AccessTokenLifespan
from hundred.ctx.auth.domain import Session
from hundred.ctx.auth.ports import SessionRepository
from hundred.exceptions import Forbidden
from hundred.services.authenticator import StatelessAuthenticator
from hundred.services.datetime import DateTimeService


@injectable
class AuthSharedLogic:
    __slots__ = (
        "__access_token_lifespan",
        "__authenticator",
        "__datetime_service",
        "__session_repository",
    )

    def __init__(
        self,
        *,
        access_token_lifespan: AccessTokenLifespan = timedelta(minutes=30),
        authenticator: StatelessAuthenticator,
        datetime_service: DateTimeService,
        session_repository: SessionRepository,
    ) -> None:
        self.__access_token_lifespan = access_token_lifespan
        self.__authenticator = authenticator
        self.__datetime_service = datetime_service
        self.__session_repository = session_repository

    async def check_session(self, application_id: UUID, claimant_id: UUID) -> Session:
        session = await self.__session_repository.get(application_id)

        if session is not None and session.is_owner(claimant_id):
            return session

        raise Forbidden()

    async def logout(self, application_id: UUID) -> None:
        await self.__session_repository.delete(application_id)

    def new_access_token(self, session: Session) -> str:
        expiration = self.__datetime_service.utcnow() + self.__access_token_lifespan
        return self.__authenticator.generate_token(
            data={
                "user_id": str(session.user.id),
                "session_status": session.status,
            },
            expiration=expiration,
        )
