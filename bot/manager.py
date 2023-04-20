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

__all__ = ["BaseManager", "EventManager"]

import os
from abc import abstractmethod
from typing import TYPE_CHECKING, List

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
        """Load all the files in a directory."""
        files = [
            i
            for i in os.listdir(os.path.join(*directory))
            if not i.startswith("__") and i.endswith(".py")
        ]

        for filename in files:
            module_name = filename[:-3]
            obj = self.load_module(f"{'.'.join(directory)}.{module_name}")
            self.modules[obj.name] = obj

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
    def load_module(self, path: str):
        event = __import__(path, globals(), locals(), ["Event"], 0).Event
        return event

    async def register_all(self, client: "ClientType"):
        for obj in self.modules.values():
            event = obj(client, self)
            setattr(client, event.name, event.execute)
