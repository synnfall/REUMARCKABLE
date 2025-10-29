from typing import Any

class Activated:
    def onActuated(self, data:dict[str,Any]) -> None:
        pass

class Actuator:
    activated: Activated
    def actuate(self) -> None:
        self.activated.onActuated({"actuator": self})
        