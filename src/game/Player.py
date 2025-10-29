from math import floor, ceil

from engine.Object import Collideable
from engine.Entity import Entity
from game.Utils import toPygameY

from game.Image import Image

import pygame.draw as draw
from pygame import Surface, Rect, Color, SRCALPHA

class Player(Entity):
    collideableList: list[Collideable]
    jumpStep: list[int] = []
    isJumping: bool = False

    color: Color|None = None
    image: Image|None = None
    drawSurface: Surface

    spawnX: int
    spawnY: int

    lastGravity: int = 0

    isActive: bool = True

    def __init__(self, x: int, y: int, width: int, height: int, collideableList: list[Collideable], texture: Color|str, drawSurface: Surface) -> None:
        self.x = x
        self.y = y

        self.spawnX = x
        self.spawnY = y

        self.width = width
        self.height = height
        self.priority = 50
        self.hardColliding = True

        self.collideableList = collideableList

        if isinstance(texture, Color):
            self.color = texture
        else:
            self.image = Image(0,0,width,height,texture,drawSurface)
        self.drawSurface = drawSurface
    
    def spawn(self):
        """Place le joueur à son point d'apparition"""
        self.x = self.spawnX
        self.y = self.spawnY
        self.xMove = 0
        self.yMove = 0
        self.lastGravity = 0

    def jump(self):
        """Génère une liste de mouvement verticaux représentant la poussée d'un saut"""
        if not self.isJumping:
            self.jumpStep = [6 if i <= 10 else 1 for i in range(13)]
            self.isJumping = True
    
    def applyGravity(self):
        """Applique une formule compliquée pour générer la gravité sur le joueur"""
        self.lastGravity += 1
        self.yMove -= self.lastGravity

    def move(self):
        if self.isJumping:
            if len(self.jumpStep) != 0:
                self.yMove += self.jumpStep.pop(0)

        possibleMovement = self.evaluateMovement(self.xMove, self.yMove)
        if possibleMovement == (0, 0):
            futureXMove = self.evaluateMovement(self.xMove, 0)[0]
            futureYMove = self.evaluateMovement(0, self.yMove)[1]
            if self.yMove < 0 and futureYMove == 0: # s'il est au sol ou atteint le sol | self.yMove != 0: slimy head ?
                self.isJumping = False
                self.jumpStep = []
            
            if (self.xMove, self.yMove) != (futureXMove, futureYMove): # si le joueur ne fonce pas dans un coin, on accepte le mouvement
                self.xMove = futureXMove
                self.yMove = futureYMove
            else:
                self.xMove = 0
                self.yMove = futureYMove # priorité à la gravité
        else:
            self.xMove = possibleMovement[0]
            self.yMove = possibleMovement[1]
        
        if self.yMove < 0:
            self.isJumping = True
        else:
            self.lastGravity = 0
        super().move()
        if self.drawSurface.get_height() <= self.y or self.y + self.height <= 0:
            self.spawn()
    
    def switchActive(self):
        self.isActive = not self.isActive
    
    def show(self):
        if self.color:
            toDraw: Surface = Surface((self.width,self.height), SRCALPHA)
            toDraw.fill(self.color if self.isActive else (self.color - Color(50,50,50,0)))
            self.drawSurface.blit(
                toDraw,
                (
                    self.x,
                    toPygameY(self.y, self.height, self.drawSurface.get_height())
                )
            )
        elif self.image:
            self.image.setCoordinate(self.x,self.y)
            self.image.show()
        return
    
    def evaluateMovement(self, xMove: int, yMove: int) -> tuple[int,int]:
        """Renvoi le mouvement possible sans entrer en collision frontale"""
        collide: bool = False
        collideCoefficients: tuple[float, float] = (-1,-1) 
        i = 0
        while i < len(self.collideableList):
            collideable = self.collideableList[i]
            if collideable != self and collideable.hardColliding:
                cc: tuple[float, float] = self.willCollideWhen(collideable, xMove, yMove) # cc : collide coefficients
                if cc != (-1,-1):
                    if not collide and collideCoefficients == (-1,-1):
                        collide = True
                        collideCoefficients = cc
                    elif collide and (cc[0] <= collideCoefficients[0] and cc[1] != 0):
                            collideCoefficients = cc
            i += 1
        
        if collide:
            if not collideCoefficients[0] == collideCoefficients[1] == 0:
                t: float = collideCoefficients[0]
                xMove = floor(t * self.xMove) if 0 <= self.xMove else ceil(t * self.xMove)
                yMove = floor(t * self.yMove) if 0 <= self.yMove else ceil(t * self.yMove) 
        return (xMove, yMove)