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

    def showAt(self, x:int, y:int):
        self.x, x = x, self.x
        self.y, y = y, self.y
        self.show()
        self.x = x
        self.y = y

    def update(self):
        """Mets à jour l'état d'un objet"""
        pass

class MoveableObject(Object):
    xMove: int = 0
    yMove: int = 0

    def move(self):
        self.x += self.xMove
        self.y += self.yMove
        
        self.xMove = 0
        self.yMove = 0

class Collideable(Object):
    priority: int
    hardColliding: bool

    def isColliding(self, c: Collideable) -> bool:
        """Retourne si le Collideable actuel est en collision avec le Collideable c"""
        return c.x <= self.x + self.width and self.x <= c.x+ c.width and c.y <= self.y + self.height and self.y <= c.y + c.height # <=> !(pas de collision)

class Clickable(Object):
    @abstractmethod
    def onClick(self):
        pass

    def isOn(self, x:int, y:int) -> bool:
        """Retourne si les coordonnées x,y sont comprise dans la zone clickable"""
        return x <= self.x + self.width and self.x <= x and y <= self.y + self.height and self.y <= y

class Button(Clickable):
    def __init__(self, x:int, y:int, width:int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def onClick(self):
        pass

    def show(self):
        pass