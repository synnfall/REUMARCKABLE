import pygame

from engine.Object import Object,Clickable

from game.Game import Game
from game.Utils import toPygameY

class Menu(Object):
    content: list[Object] = []
    clickableIndexes: list[int] = []

    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.height = 0
        self.width = 0
    
    def showAt(self, x:int, y:int):
        return
    
    def add(self, *objects: Object):
        for obj in objects:
            if isinstance(obj, Clickable):
                self.clickableIndexes.append(len(self.content))
            self.content.append(obj)
    
    def show(self):
        for obj in self.content:
            obj.show()
        
    def onClick(self, x:int, y:int):
        i: int = 0
        found: bool = False
        while i < len(self.clickableIndexes) and not found:
            j: int = self.clickableIndexes[i]
            clickable: Object = self.content[j]
            if not isinstance(clickable, Clickable): return
            if clickable.isOn(x,y):
                clickable.onClick()
                found = True
            i += 1
    
    def run(self, game: Game):
        self.show()
        for event in pygame.event.get(pygame.MOUSEBUTTONDOWN):
            if event.dict["button"] == 1: # clic gauche
                mousePos = event.dict["pos"]
                self.onClick(
                    mousePos[0],
                    toPygameY(mousePos[1], 0, game.getScreen().get_height())
                )
