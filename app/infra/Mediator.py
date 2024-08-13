from typing import Any, Callable


class Mediator():
    callbacks: dict[str, list[Callable[[Any], None]]] = {}

    def subscribe(self, event: str, callback: Callable[[Any], None]):
        self.callbacks[event].append(callback)

    def notify(self, event: str, args: Any):
        for callback in self.callbacks[event]:
            callback(args)