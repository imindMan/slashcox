### BASE ####
# Necessary classes for the infrastruture of this bot
##
############

from abc import abstractmethod
from typing import TypeAlias

#### IMPORTING ####
import discord
from discord import app_commands

from .config import Config
from .logger import Logger
from .manager import EventManager

### IMPORTANT VARIABLE ###
config = Config()

# avoid circular imports
ClientType: TypeAlias = "Client"
###################


# Client
class Client(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_messages = 2000
        self.status = discord.Status.online
        self.activity = discord.Activity(
            type=discord.ActivityType.watching, name="Virbox videos"
        )

    def init_tree(self, tree: app_commands.CommandTree):
        self.tree = tree

    async def on_ready(self):
        await self.tree.sync(guild=discord.Object(id=config.server_id))
        Logger.log("Slashcox has started!")
        Logger.newline()
        Logger.log(f"Logged in as {self.user.name}#{self.user.discriminator}")
        Logger.log("Server id:", config.server_id)

        eventManager = EventManager()
        eventManager.load_all(["bot", "events"])
        await eventManager.register_all(self)


# The tree
class Tree(app_commands.CommandTree):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BaseEvent:
    """The class for creating events
    To create an event, create a file in bot/events and have a class called Event in it wich extends this class.
    It needs to have a name attribute and an execute method.

    [Attributes]:
        name (str): The name of the event. Available names can be found here:
            https://discordpy.readthedocs.io/en/stable/api.html#discord-api-events
        execute (function):
            The function which will get called. For what arguments to use, read the above docs.
    """

    name: str = ""

    def __init__(self, client: Client, manager: EventManager) -> None:
        self.bot = client
        self.manager = manager

        if not self.name:
            raise ValueError("Event name is required")

    @abstractmethod
    async def execute(self) -> None:
        raise NotImplementedError("Execute method is required")
