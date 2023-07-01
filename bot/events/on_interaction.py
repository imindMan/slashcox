from bot.base import BaseEvent
from bot.logger import Logger
# permissions checking

class Event(BaseEvent):
    name = "on_interaction"

    async def execute(self, interaction):
        logger = Logger()
        if interaction.command.check_permissions(interaction):
            pass 
        else:
            await logger.send_error("Insufficient permissions", interaction)
