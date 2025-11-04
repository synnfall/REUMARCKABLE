from engine.Object import Clickable

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