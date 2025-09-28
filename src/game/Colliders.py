from engine.Object import Collideable

class RectangleCollider(Collideable):
    def __init__(self, x: int, y: int, w: int, h: int) -> None:
        self.x = x
        self.y = y
        self.width = w
        self.height = h
    
    def show(self):
        return