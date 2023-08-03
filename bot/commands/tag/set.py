import asyncio
from urllib.parse import quote

from bot.base import BaseCommand
from bot.config import Config, Embed

from discord.ui import Modal, TextInput
import discord


class TagModel(Modal, title="New Tag"):
    name = TextInput(
            style=discord.TextStyle.short,
            label="What should the name of the tag be?",
            required=True,
            max_length=100,
            placeholder="Sample"
            )
    description = TextInput(
            style=discord.TextStyle.long,
            label="What should the content of the tag be?",
            required=True,
            max_length=1000,
            placeholder="This is a sample description"

            )
    def init_db(self, db):
        self.db = db
    
    async def on_submit(self, interaction) -> None:
        await self.db.raw_exec_commit(
            """INSERT INTO tags VALUES(?, ?)""",
            (
                quote(self.name.value),
                quote(self.description.value),
            ),
        )
        embed = Embed(title="Tag set", description=f"Tag `{self.name.value}` set")
        await interaction.response.send_message(embed=embed)

class cmd(BaseCommand):
    """A discord command instance."""

    name = "set"
    description = "Add or update a tag"

    async def execute(self, interaction) -> None:
        modal = TagModel()
        modal.init_db(self.db)
        await interaction.response.send_modal(modal)
            
        

        
