import discord

from bot.base import BaseCommand
from bot.config import Config, Embed


class cmd(BaseCommand):
    """A discord command instance."""

    name = "avatar"
    description = "Returns the avatar of the user. If a mention or id is given, returns the avatar of that user"

    async def execute(self, interaction, member: discord.member.Member = None) -> None:
        user = interaction.user if member is None else member
        url = user.display_avatar.url
        embed = Embed(title=f"{user.name}'s avatar")
        embed.set_image(url=url)
        await interaction.response.send_message(embed=embed)
