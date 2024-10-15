from uuid import UUID

from cq import Command, command_handler
from pydantic import SecretStr

from hundred.ctx.auth.commands._shared_logic import AuthSharedLogic
from hundred.ctx.auth.dto import Authenticated
from hundred.ctx.auth.ports import SessionRepository
from hundred.exceptions import Unauthorized
from hundred.services.datetime import DateTimeService
from hundred.services.hasher import Hasher


class RefreshCommand(Command):
    application_id: UUID
    session_token: SecretStr

    @property
    def raw_session_token(self) -> str:
        return self.session_token.get_secret_value()


@command_handler(RefreshCommand)
class RefreshHandler:
    __slots__ = (
        "datetime_service",
        "hasher",
        "session_repository",
        "shared_logic",
    )

    def __init__(
        self,
        datetime_service: DateTimeService,
        hasher: Hasher,
        session_repository: SessionRepository,
        shared_logic: AuthSharedLogic,
    ) -> None:
        self.datetime_service = datetime_service
        self.hasher = hasher
        self.session_repository = session_repository
        self.shared_logic = shared_logic

    async def handle(self, command: RefreshCommand) -> Authenticated:
        session = await self.session_repository.get(command.application_id)
        token = command.raw_session_token
        hashed_token = ""

        if (
            session is None
            or not session.user.is_active
            or not self.hasher.verify(token, hashed_token := session.raw_token)
        ):
            raise Unauthorized()

        if self.hasher.needs_rehash(hashed_token):
            session.token = SecretStr(self.hasher.hash(token))

        session.last_seen = self.datetime_service.utcnow()
        session.bump_version()
        await self.session_repository.save(session)

        access_token = self.shared_logic.new_access_token(session=session)
        return Authenticated(
            access_token=SecretStr(access_token),
            session_status=session.status,
        )
