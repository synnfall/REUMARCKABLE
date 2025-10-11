from pygame import image, Surface, transform

from engine.Object import Object
from game.Utils import IMAGE_DIRECTORY, NO_TEXTURE, toPygameY

from os.path import isfile

class Image(Object):
    imageSurface: Surface
    drawSurface: Surface

    def __init__(self, x:int, y:int, width:int, height:int, imageName:str, drawSurface: Surface) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        if not isfile(IMAGE_DIRECTORY + imageName):
            imageName = NO_TEXTURE
        self.imageSurface = image.load(IMAGE_DIRECTORY + imageName).convert()
        self.drawSurface = drawSurface
    
    def show(self):
        self.drawSurface.blit(
            transform.scale(self.imageSurface, (self.width, self.height)),
            (
                self.x,
                toPygameY(self.y, self.height, self.drawSurface.get_height())
            )
        )
