from discord import Attachment

from bot.base import BaseCommand
from bot.config import Config, Embed


class cmd(BaseCommand):
    name = "updatefetch"
    description = "Update your fetch"

    async def execute(
        self,
        interaction,
        image: Attachment = None,
        distro: str = None,
        kernel: str = None,
        terminal: str = None,
        editor: str = None,
        shell: str = None,
        de_wm: str = None,
        bar: str = None,
        resolution: str = None,
        display_protocol: str = None,
        gtk_theme: str = None,
        gtk_icon_theme: str = None,
        cpu: str = None,
        gpu: str = None,
        description: str = None,
        dotfiles: str = None,
        git: str = None,
        memory: str = None,
    ) -> None:
        arguments = [
            image,
            distro,
            kernel,
            terminal,
            editor,
            shell,
            de_wm,
            bar,
            resolution,
            display_protocol,
            gtk_theme,
            gtk_icon_theme,
            cpu,
            gpu,
            description,
            dotfiles,
            git,
            memory,
        ]

        for i in range(len(arguments)):
            if arguments[i] is not None:
                col = await self.db.raw_exec_select(
                    "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE ORDINAL_POSITION = ? AND TABLE_NAME = 'fetch';",
                    (i + 2,),
                )

                await self.db.raw_exec_commit(
                    f"UPDATE slashcox.fetch SET {col[0][0]} = ? WHERE user = ?;",
                    (arguments[i], interaction.user),
                )
        embed = Embed(title="Successfully update the fetch")
        await interaction.response.send_message(embed=embed)
