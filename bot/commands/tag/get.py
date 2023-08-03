from urllib.parse import quote, unquote

from bot.base import BaseCommand
from bot.config import Config, Embed


class cmd(BaseCommand):
    """A discord command instance."""

    name = "get"
    description = "Gets the content of a tag"

    async def execute(self, interaction, name:str) -> None:
        content = await self.db.raw_exec_select(
            """SELECT Content FROM tags WHERE Name = ?""", (quote(name),)
        )
        if not len(content):
            return await self.logger.send_error(f"Tag '{name}' doesn't exist", interaction)

        embed = Embed(title=f"Tag: `{name}`", description=f"{unquote(content[0][0])}")
        await interaction.response.send_message(embed=embed)
