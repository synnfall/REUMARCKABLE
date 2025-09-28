from game.Player import Player

class PhantomPlayer(Player):
    isActive: bool = False
    movementsList: list[str] = []

    def move(self):
        
        super().move()