"""All the managers for commands, events, etc.
To create a manager, create a class that extends BaseManager
In it override these two methods:
    load_module(self, path: str):
        This method takes the path to a file (seperated with dots) and imports something from it.
        For example the the CommandManager imports the Command class,
        EventManager imports the Event class, etc.
        You can do this by using the following code:
        name = __import__(
            path, globals(), locals(), ["Name"], 0
        ).name
        return name

    register_all(self, client: bot.base.Client):
        This method takes the client instance.
        NOTE If you are adding a type to the argument, use "ClientType" to avoid a circular import
        It then runs code that registers everything, for example all commands or events.
        You can get all the loaded objects with self.modules.values()
        This code will be different for every manager.
Now to use it, go to bot/base.py and put this code into Client.on_ready:
    xManager = XManager()
    xManager.load_all(["path", "to", "folder"])
    xManager.register_all(self)
You also have to import it of course.

TODO Add a command manager
TODO Add a task manager
"""

__all__ = ["BaseManager", "EventManager", "CommandManager"]

import os
from abc import abstractmethod
from typing import TYPE_CHECKING, List

import discord

from .config import Config

# avoid circular imports
if TYPE_CHECKING:
    from .base import ClientType


class BaseManager:
    """The base class all managers inherit from.
    [load_all(self, directory: List[str])]:
        This method imports all the files from a directory.
        The argument is a list of strings, each being one directory, that contains the files.

    [get(self, name: str)]:
        This method returns a loaded object by it's name.

    load_module and register_all are described above.
    """

    def __init__(self) -> None:
        """Initialize by creating an empty dictionary."""
        self.modules = {}

    def load_all(self, directory: List[str]) -> None:
        """Load all the files in a directory.
        NOTE: I just hate the idea of making a category file then use it to load everything. Why not load all of them from scratch?
        Also, speed is a problem anyway
        """

        def get_files_dict(path):
            files_dict = {}
            for root, dirs, files in os.walk(path):
                current_dict = files_dict
                for dir in os.path.relpath(root, path).split(os.path.sep):
                    current_dict = current_dict.setdefault(dir, {})
                for file in files:
                    current_dict[file] = "file"
            return files_dict

        files = get_files_dict(os.path.join(*directory))

        def load_module(files, extra_prefix=None):
            for filename, filevalue in files.items():
                string_to_import = ""
                for i in filevalue:
                    module_name = i[:-3]
                    if extra_prefix == None:
                        if filename == ".":
                            string_to_import = f"{'.'.join(directory)}.{module_name}"
                        elif filename == "__pycache__":
                            continue
                        elif files[filename] == "file":
                            string_to_import = (
                                f"{'.'.join(directory)}.{filename}.{module_name}"
                            )
                        else:
                            load_module(files[filename], filename)
                    else:
                        module_name = filename[:-3]
                        if filename == "__pycache__":
                            continue
                        elif files[filename] == "file":
                            string_to_import = (
                                f"{'.'.join(directory)}.{extra_prefix}.{module_name}"
                            )
                        else:
                            load_module(files[filename], extra_prefix + filename)
                    if string_to_import != "":
                        obj = self.load_module(string_to_import)

                        self.modules[obj.name] = obj

        load_module(files)

    def get(self, name: str):
        """Load an object from a given file.
        [Raises]:
            NotImplementedError, if function is called but has not been changed.
        """
        """Get an object by its name.
        [Raises]:
            KeyError, when name is not found.
        """
        return self.modules[name]

    @abstractmethod
    def load_module(self, path: str):
        """Load an object from a given file.
        [Raises]:
            NotImplementedError, if function is called but has not been changed.
        """
        raise NotImplementedError("load_module method is not implemented")

    @abstractmethod
    async def register_all(self, client: "ClientType"):
        """Register all the imported objects.
        [Raises]:
            NotImplementedError, if function is called but has not been changed.
        """
        raise NotImplementedError("register_all method is not implemented")


class EventManager(BaseManager):
    """Manager for discord events.
    The on_ready event is already registered by default and can't be changed with this.
    To create a event, create a file in bot/events and have a class in it called Event,
    that extends bot.base.BaseEvent
    It needs to have a name attribute and an execute method.
    """

    def __init__(self, db) -> None:
        self.modules = {}
        self.db = db

    def load_module(self, path: str):
        event = __import__(path, globals(), locals(), ["Event"], 0).Event
        return event

    async def register_all(self, client: "ClientType"):
        for obj in self.modules.values():
            event = obj(client, self, self.db)
            setattr(client, event.name, event.execute)


class CommandManager(BaseManager):
    """Manager for discord commands
    Always need to be allocate in the bot/commands directory
    The same steps as EventManager class but instead you must have a class cmd that extends bot.base.BaseCommand
    """

    def __init__(self, tree, db) -> None:
        """Initialize by creating an empty dictionary."""
        self.modules = {}
        self.tree = tree
        self.db = db

    def load_module(self, path: str):
        command = __import__(path, globals(), locals(), ["cmd"], 0).cmd
        return command

    async def register_all(self, client: "ClientType"):
        for obj in self.modules.values():
            command = obj(client, self, self.db)
            self.tree.register(command)
        await self.tree.sync(guild=discord.Object(id=Config.server_id))


class TasksManager(BaseManager):
    """Manager for discord events.
    The on_ready event is already registered by default and can't be changed with this.
    To create a event, create a file in bot/events and have a class in it called Event,
    that extends bot.base.BaseEvent
    It needs to have a name attribute and an execute method.
    """

    def __init__(self, db) -> None:
        self.modules = {}
        self.db = db

    def load_module(self, path: str):
        task = __import__(path, globals(), locals(), ["TaskLoop"], 0).TaskLoop
        return task

    async def register_all(self, client: "ClientType"):
        for obj in self.modules.values():
            task = obj(client, self, self.db)
            task.execute.start()
