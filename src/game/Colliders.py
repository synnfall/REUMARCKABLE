from engine.Object import Collideable

from pygame.surface import Surface
from pygame.color import Color
from pygame.rect import Rect
import pygame.draw as draw

class RectangleCollider(Collideable):
    color: Color
    surface: Surface

    def __init__(self, x: int, y: int, w: int, h: int, color: Color, surface: Surface) -> None:
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.color = color
        self.surface = surface
    
    def show(self):
        draw.rect(self.surface, self.color, Rect(self.x, self.surface.get_height() - self.y - self.height, self.width, self.height))
        return