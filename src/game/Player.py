from math import floor, ceil

from engine.Object import Collideable
from engine.Entity import Entity
class Player(Entity):
    collideableList: list[Collideable]
    jumpStep: list[int] = []
    isJumping: bool = False
    i: int = 0

    def __init__(self, x: int, y: int, width: int, height: int, collideableList: list[Collideable]) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.collideableList = collideableList
    
    def jump(self):
        if not self.isJumping:
            self.jumpStep = [10 if i <= 10 else 5 for i in range(13)]
            self.isJumping = True
    
    def applyGravity(self):
        self.yMove -= 5

    def move(self):
        if self.isJumping:
            if len(self.jumpStep) != 0:
                self.yMove += self.jumpStep.pop(0)

        possibleMovement = self.evaluateMovement(self.xMove, self.yMove)
        if possibleMovement == (0, 0):

            futureXMove = self.evaluateMovement(self.xMove, 0)[0]
            futureYMove = self.evaluateMovement(0, self.yMove)[1]
            self.xMove = futureXMove
            if self.yMove != 0 and futureYMove == 0:
                self.isJumping = False
            self.yMove = futureYMove
        else:
            self.xMove = possibleMovement[0]
            self.yMove = possibleMovement[1]
        
        if self.yMove < 0:
            self.isJumping = True
        super().move()
    
    def show(self):
        return
    
    def evaluateMovement(self, xMove: int, yMove: int) -> tuple[int,int]:
        """Renvoi le mouvement possible sans entrer en collision frontale"""
        collide: bool = False
        collideCoefficients: tuple[float, float] = (-1,-1) 
        i = 0
        while i < len(self.collideableList):
            collideable = self.collideableList[i]
            if collideable != self:
                cc: tuple[float, float] = self.willCollideWhen(collideable, xMove, yMove)
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