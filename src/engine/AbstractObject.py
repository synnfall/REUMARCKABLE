from abc import ABC, abstractmethod

"""Classe représentant tous les objets du jeu"""
class AbstractObject(ABC):
    name: str
    texture: str
    x: int
    y: int
    width: int
    height: int

    def getName(self) -> str:
        return self.name

    def getTexture(self) -> str:
        return self.texture

    @abstractmethod    
    def getX(self) -> int:
        return self.x
    
    @abstractmethod
    def getY(self) -> int:
        return self.y
    
    def getWidth(self) -> int:
        return self.width
    
    def getHeight(self) -> int:
        return self.height
    
    @abstractmethod
    def draw(self):
        pass