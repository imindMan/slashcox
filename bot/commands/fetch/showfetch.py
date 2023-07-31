from io import BytesIO

import discord
from PIL import Image

from bot.base import BaseCommand
from bot.config import Config, Embed


class cmd(BaseCommand):
    name = "showfetch"
    description = "Show your fetch"

    def apply_list_of_arguments(self, tuple_of_fetch: tuple):
        arguments = dict()
        list_of_keys = [
            "image",
            "**Distro**",
            "**Kernel**",
            "**Terminal**",
            "**Editor**",
            "**Shell**",
            "**DE/WM**",
            "**Bar**",
            "**Resolution**",
            "**Display Protocol**",
            "**GTK**",
            "**GTK icon**",
            "**CPU**",
            "**GPU**",
            "**Description**",
            "**Dotfiles**",
            "**Git**",
            "**Memory**",
        ]
        has_image = False
        for i in range(len(list_of_keys)):
            if tuple_of_fetch[0][1:][i] is not None:
                arguments[list_of_keys[i]] = tuple_of_fetch[0][1:][i]
                if i == 0:
                    has_image = True

        self.arguments = arguments
        if has_image == False:
            self.arguments["image"] = None

    async def execute(self, interaction, member: discord.member.Member = None):
        if member is None:
            fetch_data = await self.db.raw_exec_select(
                "SELECT * FROM slashcox.fetch WHERE user=?", interaction.user
            )
            user = interaction.user

        else:
            fetch_data = await self.db.raw_exec_select(
                "SELECT * FROM slashcox.fetch WHERE user=?", member
            )
            user = member
        if fetch_data == ():
            await self.logger.send_error("No existed user", interaction)
            return

        self.apply_list_of_arguments(fetch_data)

        string_to_print = ""
        self.arguments_tempo = {
            key: value for key, value in self.arguments.items() if key != "image"
        }
        for key, value in self.arguments_tempo.items():
            if value is not None:
                string_to_print += "{:<17} {:<15}\n".format(key, value)

        if self.arguments["image"] is None:
            embed = Embed(title=f"Fetch info from {user}", description=string_to_print)
            await interaction.response.send_message(embed=embed)

        else:
            embed = Embed(title=f"Fetch info from {user}", description=string_to_print)
            embed.set_image(url=str(self.arguments["image"]))
            await interaction.response.send_message(embed=embed)
