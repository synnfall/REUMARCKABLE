from engine.Object import Object
from game.Utils import toPygameY

from pygame import Surface, transform, Color, SRCALPHA
from pygame.font import Font, get_default_font

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

    def __init__(self, text:str, fontFile: str|None, font_size: int, color: Color, backgroundColor: Color|None, x:int, y:int, width:int, height:int, drawSurface: Surface) -> None:
        self.x = x
        self.y = y

        font = Font(fontFile, font_size)
        optimizedTextSize = font.size(text)
        self.width = width if width != 0 else optimizedTextSize[0]
        self.height = height if height != 0 else optimizedTextSize[1]

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
    fontFile: str|None
    fontSize: int
    color: Color
    backgroundColor: Color|None
    drawSurface: Surface

    def __init__(self, text:str, fontFile: str|None, fontSize: int, color:Color, backgroundColor:Color|None, x:int, y:int, width:int, height:int, drawSurface:Surface) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.text = text
        self.fontFile = fontFile
        self.fontSize = fontSize
        self.color = color
        self.backgroundColor = backgroundColor

        self.drawSurface = drawSurface
    
    def show(self):
        width: int = self.width
        height: int = self.height
        font: Font = Font(self.fontFile, self.fontSize)
        optimizedTextSize = font.size(self.text)
        if width == 0: width = optimizedTextSize[0]
        if height == 0: height = optimizedTextSize[1]

        toDisplay: Surface = font.render(self.text if self.text != "" else " ", True, self.color)

        if self.backgroundColor != None:
            backgroundSurface: Surface = Surface((width, height), SRCALPHA)
            backgroundSurface.fill( self.backgroundColor )
            backgroundSurface.blit(toDisplay, (0,0))
            toDisplay = backgroundSurface
        
        self.drawSurface.blit(
            transform.scale(toDisplay, (width, height)),
            (
                self.x if self.x != -1 else self.drawSurface.get_width() // 2 - width // 2,
                toPygameY(
                    self.y if self.y != -1 else self.drawSurface.get_height() // 2 - height // 2,
                    height,
                    self.drawSurface.get_height()
                )
            )
        )
    
    def setText(self, text:str):
        self.text = text
    
    def setFontFile(self, fontFile:str|None):
        self.fontFile = fontFile
        
    def setFontSize(self, fontSize:int):
        self.fontSize = fontSize
    
    def setColor(self, color:Color):
        self.color = color
    
    def setBackgroundColor(self, backgroundColor:Color|None):
        self.backgroundColor = backgroundColor