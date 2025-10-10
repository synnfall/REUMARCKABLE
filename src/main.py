# Example file showing a basic pygame "game loop"
import pygame
from pygame.surface import Surface
from pygame.rect import Rect
from pygame.color import Color

from engine.Object import Collideable
from game.Colliders import RectangleCollider
from game.Player import Player
from game.PhantomPlayer import PhantomPlayer

pygame.init()
screenWidth: int = 1280
screenHeight: int = 720
screen = pygame.display.set_mode((screenWidth, screenHeight))

def toPygameY(y:int, objectHeight: int, screenHeight: int) -> int:
    return screenHeight - y - objectHeight

clock = pygame.time.Clock()
running = True

colliders: list[Collideable] = []

sol1: RectangleCollider = RectangleCollider(0, 200, screenWidth, 50, Color(0,255,0), screen)
colliders.append(sol1)

mur1: RectangleCollider = RectangleCollider(1000, 280, 50, 50, Color(0,255,0), screen)
colliders.append(mur1)

p: Player = Player(0,400, 50, 50, colliders, Color(255,0,0), screen)
colliders.append(p)

phantom: PhantomPlayer = PhantomPlayer(0, 350, 50, 50, colliders, Color(0,0,255), screen)
colliders.append(phantom)

activePlayer: Player = p
while running:
    keyPressedMap = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False    
        if event.type == pygame.KEYDOWN:
            if event.dict["unicode"] == "v":
                if activePlayer == p:
                    if phantom.canSetActive():
                        activePlayer = phantom
                        phantom.switchActive()
                else:
                    activePlayer = p
                    phantom.switchActive()

    #if keyPressedMap[pygame.K_z]:
    #    activePlayer.yMove += 5
    #if keyPressedMap[pygame.K_s]:
    #    activePlayer.yMove -= 5
    if keyPressedMap[pygame.K_d]:
        activePlayer.xMove += 5
    if keyPressedMap[pygame.K_q]:
        activePlayer.xMove -= 5
    if keyPressedMap[pygame.K_SPACE]:
        activePlayer.jump()

    p.applyGravity()
    phantom.applyGravity()
    p.move()
    phantom.goBack()
    phantom.move()

    screen.fill("white")

    for c in colliders:
        c.show()
        #pygame.draw.rect(screen, "red", Rect(c.x, toPygameY(c.y, c.height, screenHeight) ,c.width,c.height))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
