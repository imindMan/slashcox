from mcstatus import JavaServer

from bot.base import BaseCommand
from bot.config import Config, Embed


class cmd(BaseCommand):
    name = "players"
    description = "Get the players of the minecraft server"

    async def execute(self, interaction) -> None:
        server = JavaServer.lookup(f"{Config.minecraft_url}:{Config.minecraft_port}")
        # 'query' has to be enabled in a server's server.properties file!
        # It may give more information than a ping, such as a full player list or mod information.
        query = server.query()

        players = " \n".join(query.players.names)
        if len(query.players.names) == 0:
            players = "Nobody Online :("
        embed = Embed(
            title="Minecraft",
            description=f"""
**CURRENTLY ONLINE ({query.players.online}/{query.players.max}):** ```{players}```
""",
        )
        embed.set_color("green")
        await interaction.response.send_message(embed=embed)
