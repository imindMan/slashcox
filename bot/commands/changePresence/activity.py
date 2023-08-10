import discord

from typing import Literal
from bot.base import BaseCommand
from bot.config import Config, Embed


class cmd(BaseCommand):
    """A discord command instance."""

    name = "activity"
    description = "Changes the bot's activity."

    async def execute(self, interaction, _type:Literal["playing", "watching", "listening"], message:str) -> None:
        match _type:
            case "playing":
                activityType = discord.ActivityType.playing
            case "watching":
                activityType = discord.ActivityType.watching
            case "listening":
                activityType = discord.ActivityType.listening
            
        activity = discord.Activity(type=activityType, name=message)
        self.bot.current_activity = activity
        await self.bot.change_presence(
            activity=activity, status=self.bot.current_status
        )
        embed = Embed(
            title="Activity changed",
            description=f"Succesfully changed activity to {type}",
        )
        await interaction.response.send_message(embed=embed)

    def check_permissions(self, interaction: discord.Interaction) -> bool:
        # Check for a specific role in the member
        return any([i.id == Config().mod_role_id for i in interaction.user.roles])
