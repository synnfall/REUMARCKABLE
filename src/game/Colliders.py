from engine.Object import Object, Collideable
from engine.Actuator import Actuator, Activated
from game.Utils import toPygameY
from game.Player import Player
from game.Image import Image

from pygame import Surface, Color, SRCALPHA

class RectangleCollider(Collideable, Activated):
    color: Color|None = None
    image: Image|None = None
    drawSurface: Surface

    def __init__(self, x: int, y: int, w: int, h: int, priority: int, hardColliding:bool, texture: Color|str|None, surface: Surface) -> None:
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.priority = priority
        self.hardColliding = hardColliding
        if texture == None or isinstance(texture, Color):
            self.color = texture
        else:
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
    
    def __init__(self, x: int, y: int, w: int, h: int, priority: int, hardColliding: bool, texture: Color|str, surface: Surface, player: Player) -> None:
        self.player = player
        super().__init__(x, y, w, h, priority, hardColliding, texture, surface)
    
    def collidePlayer(self) -> bool:
        """Retourne si le joueur touche le detecteur"""
        return self.isColliding(self.player)

class ActuatorCollider(RectangleCollider, Actuator):
    def __init__(self, x:int, y:int, w:int, h:int, activated: Activated, texture:Color|str|None, surface:Surface) -> None:
        self.activated = activated
        super().__init__(x, y, w, h, 0, False, texture, surface)