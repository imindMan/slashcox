from urllib.parse import unquote

from bot.base import BaseCommand
from bot.config import Config, Embed


class cmd(BaseCommand):
    """A discord command instance."""

    name = "list"
    description = """Lists all tags"""

    async def execute(self, interaction) -> None:
        tags = await self.db.raw_exec_select("SELECT * FROM tags")
        embed = Embed(title="Tags")
        for tag in tags:
            name, content = tag
            embed.add_field(
                name=f"{unquote(name)}",
                value=f"{unquote(content)}",
            )
        await interaction.response.send_message(embed=embed)
