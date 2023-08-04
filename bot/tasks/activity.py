import discord
from discord.ext.tasks import loop
from mcstatus import JavaServer

from bot.base import BaseTask
from bot.config import Config


class TaskLoop(BaseTask):
    current = 0

    @loop(minutes=10)
    async def execute(self) -> None:
        server = JavaServer.lookup(f"{Config.minecraft_url}:{Config.minecraft_port}")
        status = server.status()

        # Prevent discord api spam
        if status.players.online == self.current:
            return
        else:
            if status.players.online > 6:
                activity = discord.Activity(
                    type=discord.ActivityType.playing,
                    name=f"with {status.players.online} Virbcrafters",
                )
            else:
                activity = discord.Activity(
                    type=discord.ActivityType.watching, name=f"Virbox videos"
                )
            self.current = status.players.online
            await self.bot.change_presence(activity=activity)
