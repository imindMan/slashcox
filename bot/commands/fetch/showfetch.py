import discord

from bot.base import BaseCommand
from bot.config import Config, Embed


class cmd(BaseCommand):
    name = "showfetch"
    description = "Show your fetch"

    def apply_list_of_arguments(self, tuple_of_fetch: tuple):
        arguments = dict()
        list_of_keys = [
            "**image**",
            "**distro**",
            "**kernel**",
            "**terminal**",
            "**editor**",
            "**shell**",
            "**de_wm**",
            "**bar**",
            "**resolution**",
            "**display_protocol**",
            "**gtk_theme**",
            "**gtk_icon_theme**",
            "**cpu**",
            "**gpu**",
            "**description**",
            "**dotfiles**",
            "**git**",
            "**memory**",
        ]
        for i in range(len(list_of_keys)):
            if tuple_of_fetch[0][1:][i] is not None:
                arguments[list_of_keys[i]] = tuple_of_fetch[0][1:][i]
        self.arguments = arguments

    async def execute(self, interaction, member: discord.member.Member = None):
        if member is None:
            fetch_data = await self.db.raw_exec_select(
                "SELECT * FROM slashcox.fetch WHERE user=?", interaction.user
            )

        else:
            fetch_data = await self.db.raw_exec_select(
                "SELECT * FROM slashcox.fetch WHERE user=?", member
            )

        self.apply_list_of_arguments(fetch_data)

        string_to_print = ""

        for key, value in self.arguments[1:].items():
            if value is not None:
                string_to_print += "{:<17} {:<15}\n".format(key, value)

        await interaction.response.send_message(string_to_print)
