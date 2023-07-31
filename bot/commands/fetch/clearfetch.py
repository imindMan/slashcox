from bot.base import BaseCommand
from bot.config import Config, Embed
from typing import Literal

class cmd(BaseCommand):
    name = "clearfetch"
    description = "Clear your fetch"


    async def execute(self, interaction, field: Literal [
            "image",
            "distro",
            "kernel",
            "terminal",
            "editor",
            "shell",
            "de_wm",
            "bar",
            "resolution",
            "display_protocol",
            "gtk_theme",
            "gtk_icon_theme",
            "cpu",
            "gpu",
            "description",
            "dotfiles",
            "git",
            "memory",

            ]):

        await self.db.raw_exec_commit(
                        f"UPDATE slashcox.fetch SET {field} = ? WHERE user = ?;",
                        (None, interaction.user),
                    )

        embed = Embed(title="Successfully update the fetch")
        await interaction.response.send_message(embed=embed)

