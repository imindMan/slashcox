from bot.base import BaseCommand
from bot.config import Config, Embed


class cmd(BaseCommand):
    """A discord command instance."""

    name = "ping"
    description = "Check the current latency of the bot."

    async def execute(self, interaction, _type:str="empty", test3:str="empty") -> None:
        if _type == "print":
            embed = Embed(
                title="Hello world!",
                description=f"This is a test embed\nYou typed {test3}",
            )
        else:
            embed = Embed(
                title="Hello world!",
                description=f"Current bot latency is `{round(self.bot.latency*1000,2)}ms`",
            )
        await interaction.response.send_message("Im alivetesererete!!", embed=embed)
