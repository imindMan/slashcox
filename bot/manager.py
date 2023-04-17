__all__ = ["BaseManager", "EventManager"]

from abc import abstractmethod
from typing import List, TYPE_CHECKING
import os

#avoid circular imports
if TYPE_CHECKING:
    from .base import ClientType

class BaseManager:
    def __init__(self) -> None:
        self.modules = {}

    def load_all(self, directory: List[str]) -> None:
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
        return self.modules[name]

    @abstractmethod
    def load_module(self, path: str):
        raise NotImplementedError("load_module method is not implemented")

    @abstractmethod
    async def register_all(self, client: "ClientType"):
        raise NotImplementedError("register_all method is not implemented")

class EventManager(BaseManager):
    def load_module(self, path: str):
        event = __import__(
            path, globals(), locals(), ["Event"], 0
        ).Event
        return event

    async def register_all(self, client: "ClientType"):
        for obj in self.modules.values():
            event = obj(client, self)
            setattr(client, event.name, event.execute)
