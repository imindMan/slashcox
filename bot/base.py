### BASE ####
# Necessary classes for the infrastruture of this bot
##
############

import asyncio
import inspect
from abc import abstractmethod
from typing import TypeAlias

#### IMPORTING ####
import discord
from discord import app_commands

from .config import Config
from .logger import Logger
from .manager import CommandManager, EventManager
from .sql import SQLParser

### IMPORTANT VARIABLE ###
config = Config()

# avoid circular imports
ClientType: TypeAlias = "Client"
###################
CREATE_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS slashcox.polls (
        channel_id BIGINT NOT NULL,
        message_id BIGINT NOT NULL PRIMARY KEY,
        type ENUM('single', 'multiple')
    );
    """,
    """
        CREATE TABLE IF NOT EXISTS slashcox.levels (
            user_id VARCHAR(100) PRIMARY KEY,
            level INTEGER,
            exp INTEGER,
            font_color VARCHAR(25),
            bg VARCHAR(2048) DEFAULT NULL
        );
    """,
    """
        CREATE TABLE IF NOT EXISTS slashcox.latest_video (
	       video_id VARCHAR(50) PRIMARY KEY
        );
    """,
    """
        CREATE TABLE IF NOT EXISTS slashcox.request (
            Number_id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
            Member_id VARCHAR(100) NOT NULL,
            Title VARCHAR(255) NOT NULL,
            Description VARCHAR(2048) NOT NULL,
            Upvote INTEGER NOT NULL,
            Downvote INTEGER NOT NULL,
            Pending_close INTEGER NOT NULL
        );
    """,
    """
        CREATE TABLE IF NOT EXISTS slashcox.reminders (
            id INTEGER AUTO_INCREMENT PRIMARY KEY,
            User VARCHAR(100),
            Timestamp INTEGER,
            Reminder VARCHAR(2048),
            Channel VARCHAR(100),
            Message VARCHAR(100)
        );
    """,
    """
        CREATE TABLE IF NOT EXISTS slashcox.membercount (
            membercount INT PRIMARY KEY
        );
    """,
    """
    	CREATE TABLE IF NOT EXISTS slashcox.starboard (
	       message_id VARCHAR(100) PRIMARY KEY,
	       board_message_id VARCHAR(100)
	   );
    """,
    """
        CREATE TABLE IF NOT EXISTS slashcox.tags (
            Name VARCHAR(100) UNIQUE PRIMARY KEY,
            Content VARCHAR(2048)
        );
    """,
]


# Client
class Client(discord.Client):
    """initialize the client class"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_messages = 2000
        self.status = discord.Status.online
        self.activity = discord.Activity(
            type=discord.ActivityType.watching, name="Virbox videos"
        )

    """Basically apply the tree to the main client"""

    def init_tree(self, tree: app_commands.CommandTree):
        self.tree = tree

    """MAIN PART: This is the code will run when launching slashcox"""

    async def on_ready(self):
        # sync the tree
        await self.tree.sync(guild=discord.Object(id=config.server_id))

        # basically logger being
        Logger.log("Slashcox has started!")
        Logger.newline()
        Logger.log(f"Logged in as {self.user.name}#{self.user.discriminator}")
        Logger.log("Server id:", config.server_id)

        # Initialize the database
        db = SQLParser("bot/assets/main.db", CREATE_STATEMENTS)

        await db.initialise()
        # Initialize some managers
        eventManager = EventManager(db)
        eventManager.load_all(["bot", "events"])
        await eventManager.register_all(self)

        commandManager = CommandManager(self.tree, db)
        commandManager.load_all(["bot", "commands"])
        await commandManager.register_all(self)


# The tree
class Tree(app_commands.CommandTree):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    """Instead of just making a decorator, let's make a register method. 
    This function is really inspired by the @command decorator. Basically I use the source code of @app_commands.command 
    and apply to this function"""

    def register(self, cmd):
        if not inspect.iscoroutinefunction(cmd.execute):
            raise TypeError("command function must be a coroutine function")

        self.add_command(
            app_commands.Command(
                name=cmd.name,
                description=cmd.description,
                callback=cmd.execute,
                parent=None,
            ),
            guild=discord.Object(id=config.server_id),
        )


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

    def __init__(self, client: Client, manager: EventManager, db) -> None:
        self.bot = client
        self.manager = manager
        self.db = db

        if not self.name:
            raise ValueError("Event name is required")

    @abstractmethod
    async def execute(self) -> None:
        raise NotImplementedError("Execute method is required")


class BaseCommand:
    """The class to create a command
    TO create a command, create a file in the bot/commands directory and have a class called cmd in it which extends this class
    Require: execute method, and also name, args, description
    """

    name: str = ""
    description: str = ""

    def __init__(self, client: Client, manager: CommandManager, db) -> None:
        self.bot = client
        self.manager = manager
        self.db = db

        if not self.name:
            raise ValueError("A name for a command is required")

        if not self.description:
            raise ValueError("Description for a command is required")

    @abstractmethod
    async def execute(self) -> None:
        raise NotImplementedError("Execute method is required")
