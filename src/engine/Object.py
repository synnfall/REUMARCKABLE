from __future__ import annotations
from abc import ABC, abstractmethod

class Object(ABC):
    x: int = 0
    y: int = 0
    width: int
    height: int

    @abstractmethod
    def show(self):
        pass

class MoveableObject(Object):
    xMove: int = 0
    yMove: int = 0

    @abstractmethod
    def move(self):
        self.x += self.xMove
        self.y += self.yMove
        
        self.xMove = 0
        self.yMove = 0

class Collideable(Object):
    @abstractmethod
    def isColliding(self, c: Collideable) -> bool:
        """Retourne si le Collideable actuel est en collision avec le Collideable c"""
        return c.x <= self.x + self.width and self.x <= c.x+ c.width and c.y <= self.y + self.height and self.y <= c.y + c.height # <=> !(pas de collision)
