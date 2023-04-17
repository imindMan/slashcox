from bot.base import BaseEvent


class Event(BaseEvent):
    name = "on_message"

    async def execute(self, message):
        pass
