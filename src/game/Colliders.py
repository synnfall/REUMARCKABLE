from engine.Object import Collideable
from game.Utils import toPygameY
from game.Player import Player

from pygame.surface import Surface
from pygame.color import Color
from pygame.rect import Rect
from pygame import transform

class RectangleCollider(Collideable):
    color: Color|None
    drawSurface: Surface

    def __init__(self, x: int, y: int, w: int, h: int, priority: int, color: Color|None, surface: Surface) -> None:
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.priority = priority
        self.color = color
        self.drawSurface = surface
    
    def show(self):
        if self.color == None or self.color.a == 0:
            return
        toDisplay: Surface = Surface((self.width,self.height))
        toDisplay.fill(self.color)
        self.drawSurface.blit(
            transform.scale(toDisplay, (self.width, self.height)),
            (
                self.x,
                toPygameY(self.y, self.height, self.drawSurface.get_height())
            )
        )

class PlayerDetectorCollider(RectangleCollider):
    player: Player
    
    def __init__(self, x: int, y: int, w: int, h: int, priority: int, color: Color, surface: Surface, player: Player) -> None:
        self.player = player
        super().__init__(x, y, w, h, priority, color, surface)
    
    def collidePlayer(self) -> bool:
        """Retourne si le joueur touche le detecteur"""
        return self.isColliding(self.player)