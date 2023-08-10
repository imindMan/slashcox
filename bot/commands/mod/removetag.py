from urllib.parse import quote

from bot.base import BaseCommand
from bot.config import Config, Embed


class cmd(BaseCommand):
    """A discord command instance."""

    name = "removetag"
    usage = "removetag <*name>"
    description = "Removes a tag"

    async def execute(self, interaction, name: str) -> None:
        if name == "":
            return await self.logger.send_error("Please provide a name", interaction)
        await self.db.raw_exec_commit(
            """DELETE FROM tags WHERE Name = ?""", (quote(name))
        )
        embed = Embed(title="Tag removed", description=f"The tag '{name}' was removed")
        await interaction.response.send_message(embed=embed)
    def check_permissions(self, interaction) -> bool:
        # Check for a specific role in the member
        return any([i.id == Config().mod_role_id for i in interaction.user.roles])
