from uuid import UUID

from cq import Command, command_handler

from hundred.ctx.auth.commands._shared_logic import AuthSharedLogic
from hundred.ctx.auth.factories import CheckCodeFactory
from hundred.ctx.auth.ports import SessionRepository, TwoFactorAuthenticator
from hundred.exceptions import NotModified, Unauthorized


class SendCheckCodeCommand(Command):
    application_id: UUID
    claimant_id: UUID


@command_handler(SendCheckCodeCommand)
class SendCheckCodeHandler:
    __slots__ = (
        "check_code_factory",
        "provider",
        "session_repository",
        "shared_logic",
    )

    def __init__(
        self,
        check_code_factory: CheckCodeFactory,
        provider: TwoFactorAuthenticator,
        session_repository: SessionRepository,
        shared_logic: AuthSharedLogic,
    ) -> None:
        self.check_code_factory = check_code_factory
        self.provider = provider
        self.session_repository = session_repository
        self.shared_logic = shared_logic

    async def handle(self, command: SendCheckCodeCommand) -> None:
        session = await self.shared_logic.check_session(
            command.application_id,
            command.claimant_id,
        )

        if not session.user.is_active:
            raise Unauthorized()

        if session.is_verified:
            raise NotModified(session.readable)

        code = await self.provider.send_code(session.user.id)

        if not code:
            return

        session.check_code = self.check_code_factory.build(code)
        session.bump_version()
        await self.session_repository.save(session)
