class AbstractObject:
    name: str
    texture: str
    x: int
    y: int
    width: int
    height: int

    def getName(self) -> str:
        return self.name

    def getTexture(self) -> str:
        return self.texture
    
    def getX(self) -> int:
        return self.x
    
    def getY(self) -> int:
        return self.y
    
    def getWidth(self) -> int:
        return self.width
    
    def getHeight(self) -> int:
        return self.height