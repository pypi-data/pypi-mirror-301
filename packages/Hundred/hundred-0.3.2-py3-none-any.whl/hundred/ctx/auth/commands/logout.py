from uuid import UUID

from cq import Command, command_handler

from hundred.ctx.auth.commands._shared_logic import AuthSharedLogic


class LogoutCommand(Command):
    application_id: UUID
    claimant_id: UUID


@command_handler(LogoutCommand)
class LogoutHandler:
    __slots__ = ("shared_logic",)

    def __init__(self, shared_logic: AuthSharedLogic) -> None:
        self.shared_logic = shared_logic

    async def handle(self, command: LogoutCommand) -> None:
        await self.shared_logic.check_session(
            command.application_id,
            command.claimant_id,
        )
        await self.shared_logic.logout(command.application_id)
