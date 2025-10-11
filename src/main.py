import pygame
from pygame.color import Color

from engine.Object import Collideable, Object
from game.Colliders import RectangleCollider, PlayerDetectorCollider
from game.Player import Player
from game.PhantomPlayer import PhantomPlayer
from game.Image import Image

pygame.init()
defaultScreenWidth: int = 1280
defaultScreenHeight: int = 720
screen = pygame.display.set_mode((defaultScreenWidth, defaultScreenHeight))

clock = pygame.time.Clock()
running = True

colliders: list[Collideable] = []

sol1: RectangleCollider = RectangleCollider(0, 200, defaultScreenWidth, 50, 51, Color(0,255,0), screen)
colliders.append(sol1)

sol2: RectangleCollider = RectangleCollider(defaultScreenWidth // 2, 300, defaultScreenWidth // 4, 50, 51, Color(50, 230, 65), screen)
colliders.append(sol2)

p: Player = Player(0,400, 50, 50, colliders, Color(255,0,0), screen)
colliders.append(p)

end: PlayerDetectorCollider = PlayerDetectorCollider(1000, 350, 50, 50, 51, Color(0,255,0), screen, p)
colliders.append(end)

phantom: PhantomPlayer = PhantomPlayer(0, 350, 50, 50, colliders, Color(0,0,255), screen)
colliders.append(phantom)

leftLimit: RectangleCollider = RectangleCollider(0, 0, 0, defaultScreenHeight, 100, Color(0,0,0), screen)
colliders.append(leftLimit)

rightLimit: RectangleCollider = RectangleCollider(defaultScreenWidth, 0, 0, defaultScreenHeight, 100, Color(0,0,0), screen)
colliders.append(rightLimit)

toDisplay: list[Object] = []
toDisplay += colliders

testImage: Image = Image(0,0,50,50,"canope.png",screen)
toDisplay.append(testImage)

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
                        p.switchActive()
                        phantom.switchActive()
                else:
                    activePlayer = p
                    p.switchActive()
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

    for o in toDisplay:
        o.show()
        #pygame.draw.rect(screen, "red", Rect(c.x, toPygameY(c.y, c.height, screenHeight) ,c.width,c.height))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
