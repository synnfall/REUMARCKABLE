from engine.Object import Collideable
from game.Utils import toPygameY
from game.Player import Player

from pygame.surface import Surface
from pygame.color import Color
from pygame.rect import Rect
import pygame.draw as draw

class RectangleCollider(Collideable):
    color: Color
    drawSurface: Surface

    def __init__(self, x: int, y: int, w: int, h: int, priority: int, color: Color, surface: Surface) -> None:
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.priority = priority
        self.color = color
        self.drawSurface = surface
    
    def show(self):
        draw.rect(
            self.drawSurface,
            self.color,
            Rect(
                self.x,
                toPygameY(self.y, self.height, self.drawSurface.get_height()),
                self.width,
                self.height
            )
        )
        return

class PlayerDetectorCollider(RectangleCollider):
    player: Player
    
    def __init__(self, x: int, y: int, w: int, h: int, priority: int, color: Color, surface: Surface, player: Player) -> None:
        self.player = player
        super().__init__(x, y, w, h, priority, color, surface)
    
    def collidePlayer(self) -> bool:
        """Retourne si le joueur touche le detecteur"""
        return self.isColliding(self.player)