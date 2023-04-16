from bot.base import Event as BaseEvent

class Event(BaseEvent):
    name = "on_message"

    async def execute(self, message):
        pass
