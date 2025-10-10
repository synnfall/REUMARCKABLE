from game.Player import Player

class PhantomPlayer(Player):
    isActive: bool = False
    movementsList: list[int] = []

    def jump(self):
        if self.isActive and not self.isJumping:
            self.movementsList.append( 0 )
        super().jump()
    
    def move(self):
        previousXPos: int = self.x
        super().move()
        newXPos: int = self.x
        if self.isActive and newXPos - previousXPos != 0:
            self.movementsList.append( newXPos - previousXPos )

    def switchActive(self):
        self.isActive = not self.isActive
    
    def canSetActive(self):
        return not self.isActive and len(self.movementsList) == 0

    def goBack(self):
        if not self.isActive and len(self.movementsList) != 0:
            movement = self.movementsList.pop()
            if movement == 0:
                self.jump()
            else:
                self.xMove += -movement