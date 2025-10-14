from engine.Object import Object
from game.Utils import toPygameY

from pygame import Surface, transform, font, Color, SRCALPHA

class Text(Object):
    def setPosition(self, x:int, y:int):
        self.x = x
        self.y = y
    
    def setSize(self, width:int, height:int):
        self.width = width
        self.height = height

class StaticText(Text):
    toDisplay: Surface
    drawSurface: Surface

    def __init__(self, text:str, font: font.Font, color: Color, backgroundColor: Color|None, x:int, y:int, width:int, height:int, drawSurface: Surface) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        toDisplay = font.render(text if text != "" else " ", True, color)

        if backgroundColor != None:
            backgroundSurface: Surface = Surface((self.width, self.height), SRCALPHA)
            backgroundSurface.fill(backgroundColor)
            backgroundSurface.blit(toDisplay, (0,0))
            toDisplay = backgroundSurface
        
        self.toDisplay = toDisplay
        self.drawSurface = drawSurface
    
    def show(self):
        self.drawSurface.blit(
            transform.scale(self.toDisplay, (self.width, self.height)),
            (
                self.x,
                toPygameY(self.y, self.height, self.drawSurface.get_height())
            )
        )

class DynamicText(Text):
    text: str
    textFont: font.Font
    color: Color
    backgroundColor: Color|None
    drawSurface: Surface

    def __init__(self, text:str, font:font.Font, color:Color, backgroundColor:Color|None, x:int, y:int, width:int, height:int, drawSurface:Surface) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.text = text
        self.textFont = font
        self.color = color
        self.backgroundColor = backgroundColor

        self.drawSurface = drawSurface
    
    def show(self):
        toDisplay = self.textFont.render(self.text if self.text != "" else " ", True, self.color)

        if self.backgroundColor != None:
            backgroundSurface: Surface = Surface((self.width, self.height), SRCALPHA)
            backgroundSurface.fill( self.backgroundColor )
            backgroundSurface.blit(toDisplay, (0,0))
            toDisplay = backgroundSurface
        
        self.drawSurface.blit(
            transform.scale(toDisplay, (self.width, self.height)),
            (
                self.x,
                toPygameY(self.y, self.height, self.drawSurface.get_height())
            )
        )
    
    def setText(self, text:str):
        self.text = text
    
    def setFont(self, font:font.Font):
        self.textFont = font
    
    def setColor(self, color:Color):
        self.color = color
    
    def setBackgroundColor(self, backgroundColor:Color|None):
        self.backgroundColor = backgroundColor