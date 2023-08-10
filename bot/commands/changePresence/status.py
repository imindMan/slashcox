from typing import Literal

import discord

from bot.base import BaseCommand
from bot.config import Config, Embed


class cmd(BaseCommand):
    """A discord command instance."""

    name = "status"
    description = "Changes the bot's status."

    async def execute(
        self,
        interaction,
        _type: Literal["online", "idle", "do_not_disturb", "invisible"],
    ) -> None:
        match _type:
            case "online":
                status = discord.Status.online
            case "idle":
                status = discord.Status.idle
            case "do_not_disturb":
                status = discord.Status.do_not_disturb
            case "invisible":
                status = discord.Status.invisible

        await self.bot.change_presence(
            status=status, activity=self.bot.current_activity
        )
        self.bot.current_status = status
        embed = Embed(
            title="Status changed", description=f"Succesfully changed status to {type}"
        )
        await interaction.response.send_message(embed=embed)

    def check_permissions(self, interaction: discord.Interaction) -> bool:
        # Check for a specific role in the member
        return any([i.id == Config().mod_role_id for i in interaction.user.roles])
