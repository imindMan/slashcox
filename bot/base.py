### BASE ####
# Necessary classes for the infrastruture of this bot
##
############

#### IMPORTING ####
import discord
from discord import app_commands

from .config import Config

### IMPORTANT VARIABLE ###
config = Config()
###################


# Client
class Client(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_messages = 2000
        self.status = discord.Status.online
        self.activity = discord.Activity(
            type=discord.ActivityType.watching, name=f"Virbox videos"
        )

    def init_tree(self, tree: app_commands.CommandTree):
        self.tree = tree

    async def on_ready(self):
        await self.tree.sync(guild=discord.Object(id=config.server_id))
        print("HELLO WORLD!")


# The tree
class Tree(app_commands.CommandTree):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
