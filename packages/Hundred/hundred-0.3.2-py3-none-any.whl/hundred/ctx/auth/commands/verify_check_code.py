from uuid import UUID

from cq import Command, command_handler
from pydantic import SecretStr

from hundred.ctx.auth.commands._shared_logic import AuthSharedLogic
from hundred.ctx.auth.dto import Authenticated
from hundred.ctx.auth.ports import SessionRepository
from hundred.exceptions import Unauthorized
from hundred.services.datetime import DateTimeService
from hundred.services.hasher import Hasher


class VerifyCheckCodeCommand(Command):
    application_id: UUID
    claimant_id: UUID
    code: SecretStr

    @property
    def raw_code(self) -> str:
        return self.code.get_secret_value()


@command_handler(VerifyCheckCodeCommand)
class VerifyCheckCodeHandler:
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

    async def handle(self, command: VerifyCheckCodeCommand) -> Authenticated:
        session = await self.shared_logic.check_session(
            command.application_id,
            command.claimant_id,
        )
        check_code = session.check_code
        now = self.datetime_service.utcnow()

        if (
            check_code is None
            or not session.user.is_active
            or check_code.has_expired(now)
            or not self.hasher.verify(command.raw_code, check_code.raw_value)
        ):
            raise Unauthorized()

        session.check_code = None
        session.last_seen = now
        session.verify().bump_version()
        await self.session_repository.save(session)

        access_token = self.shared_logic.new_access_token(session=session)
        return Authenticated(
            access_token=SecretStr(access_token),
            session_status=session.status,
        )
