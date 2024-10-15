from uuid import UUID

from cq import Command, command_handler
from pydantic import SecretStr

from hundred.ctx.auth.commands._shared_logic import AuthSharedLogic
from hundred.ctx.auth.dto import Authenticated
from hundred.ctx.auth.factories import SessionFactory
from hundred.ctx.auth.ports import SessionRepository, UserRepository
from hundred.exceptions import Unauthorized
from hundred.gettext import gettext as _
from hundred.services.hasher import Hasher
from hundred.services.token import TokenService


class LoginCommand(Command):
    application_id: UUID
    identifier: str
    password: SecretStr

    @property
    def raw_password(self) -> str:
        return self.password.get_secret_value()


@command_handler(LoginCommand)
class LoginHandler:
    __slots__ = (
        "hasher",
        "session_factory",
        "session_repository",
        "shared_logic",
        "token_service",
        "user_repository",
    )

    def __init__(
        self,
        hasher: Hasher,
        session_factory: SessionFactory,
        session_repository: SessionRepository,
        shared_logic: AuthSharedLogic,
        token_service: TokenService,
        user_repository: UserRepository,
    ) -> None:
        self.hasher = hasher
        self.session_factory = session_factory
        self.session_repository = session_repository
        self.shared_logic = shared_logic
        self.token_service = token_service
        self.user_repository = user_repository

    async def handle(self, command: LoginCommand) -> Authenticated:
        user = await self.user_repository.get_by_identifier(command.identifier)
        password = command.raw_password
        hashed_password = None

        if (
            user is None
            or not user.is_active
            or (hashed_password := user.raw_password) is None
            or not self.hasher.verify(password, hashed_password)
        ):
            raise Unauthorized(_("bad_credentials"))

        if self.hasher.needs_rehash(hashed_password):
            user.password = SecretStr(self.hasher.hash(password))
            user.bump_version()
            await self.user_repository.save(user)

        await self.shared_logic.logout(command.application_id)

        session_token = self.token_service.generate(256)
        session = self.session_factory.build(
            command.application_id,
            session_token,
            user,
        )
        await self.session_repository.save(session)

        access_token = self.shared_logic.new_access_token(session=session)
        return Authenticated(
            access_token=SecretStr(access_token),
            session_token=SecretStr(session_token),
            session_status=session.status,
        )
