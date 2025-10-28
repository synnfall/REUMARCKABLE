from engine.Object import Collideable
from game.Utils import toPygameY
from game.Player import Player
from game.Image import Image

from pygame import Surface, Color, SRCALPHA

class RectangleCollider(Collideable):
    color: Color|None = None
    image: Image|None = None
    drawSurface: Surface

    def __init__(self, x: int, y: int, w: int, h: int, priority: int, texture: Color|str|None, surface: Surface) -> None:
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.priority = priority
        if texture == None or isinstance(texture, Color):
            self.color = texture
        elif texture != "":
            self.image = Image(x,y,w,h,texture,surface)
        self.drawSurface = surface
    
    def show(self):
        toDisplay: Surface = Surface((self.width, self.height), SRCALPHA)
        if self.color != None:
            if self.color.a == 0: return # rien a afficher vu que c'est totalement transparent
            toDisplay.fill(self.color)
            self.drawSurface.blit(
                toDisplay,
                (
                    self.x,
                    toPygameY(self.y, self.height, self.drawSurface.get_height())
                )
            )
        elif self.image != None:
            self.image.show()

class PlayerDetectorCollider(RectangleCollider):
    player: Player
    
    def __init__(self, x: int, y: int, w: int, h: int, priority: int, texture: Color|str, surface: Surface, player: Player) -> None:
        self.player = player
        super().__init__(x, y, w, h, priority, texture, surface)
    
    def collidePlayer(self) -> bool:
        """Retourne si le joueur touche le detecteur"""
        return self.isColliding(self.player)