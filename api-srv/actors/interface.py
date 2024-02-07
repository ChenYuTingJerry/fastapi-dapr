from abc import abstractmethod

from dapr.actor import ActorInterface, actormethod


class IDemoActor(ActorInterface):
    @abstractmethod
    @actormethod(name="GetMyData")
    async def get_my_data(self) -> object:
        ...

    @abstractmethod
    @actormethod(name="SetMyData")
    async def set_my_data(self, data: object) -> None:
        ...

    @abstractmethod
    @actormethod(name="ClearMyData")
    async def clear_my_data(self) -> None:
        ...

    @abstractmethod
    @actormethod(name="SetReminder")
    async def set_reminder(self, enabled: bool) -> None:
        ...

    @abstractmethod
    @actormethod(name="SetTimer")
    async def set_timer(self, enabled: bool) -> None:
        ...

    @abstractmethod
    @actormethod(name="GetReentrancyStatus")
    async def get_reentrancy_status(self) -> bool:
        ...
