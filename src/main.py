import pygame
from pygame import Color, Surface, SRCALPHA

from engine.Object import Collideable, Object
from engine.Actuator import Actuator, Activated

from game.Game import Game
from game.Colliders import RectangleCollider, PlayerDetectorCollider, ActuatorCollider
from game.Player import Player
from game.PhantomPlayer import PhantomPlayer
from game.Image import Image
from game.Text import DynamicText, StaticText
from game.Utils import FRAME_WIDTH, FRAME_HEIGHT
from game.Menu import Menu
from game.Button import Button, TextButton
from game.Utils import toPygameY

class Rectangle(Object):
    toDraw: Surface
    drawSurface: Surface

    def __init__(self, x:int, y:int, width:int, height:int, color:Color, drawSurface: Surface) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.drawSurface = drawSurface

        self.toDraw = Surface((width, height), flags=SRCALPHA)
        pygame.draw.rect(self.toDraw, color, (0,0, width, height))

    def show(self):
        self.drawSurface.blit(
            self.toDraw,
            (
                self.x,
                toPygameY(self.y, self.height, self.drawSurface.get_height())
            )
        )


class Main:
    game: Game
    colliders: list[Collideable]
    toDisplay: list[Object]
    actuators: list[ActuatorCollider]
    end: PlayerDetectorCollider
    endText: DynamicText
    testText: DynamicText
    activePlayer: Player
    p: Player
    phantom: PhantomPlayer

    menu: Menu|None = None

    def __init__(self, game:Game|None = None) -> None:
        game = game if game != None else Game()
        colliders:list[Collideable] = []

        rectangleCollidersInfo: list[ tuple[int,int,int,int,int,bool,Color|None] ] = [
            (0,200,FRAME_WIDTH//2 - 100,50,51,True,Color(0,255,0)), # sol principal
            (FRAME_WIDTH // 2 - 100, 180, FRAME_WIDTH // 2 + 100, 50, 51, True, Color(0,255,0)), # plateforme basse
            (FRAME_WIDTH // 2, 280, FRAME_WIDTH // 4, 50, 51, True, Color(50, 230, 65)), # plateforme haut
            (0, 0, 0, FRAME_HEIGHT, 100, True, None), # mur écran gauche
            (FRAME_WIDTH, 0, 0, FRAME_HEIGHT, 100, True, None) # mur écran droit
        ]
        for rci in rectangleCollidersInfo:
            colliders.append( RectangleCollider(*rci, game.getScreen()) )

        p: Player = Player(0,400, 50, 50, colliders, "background.jpg", game.getScreen())
        phantom: PhantomPlayer = PhantomPlayer(0, 350, 50, 50, colliders, Color(0,0,255), game.getScreen())
        colliders.append(p)
        colliders.append(phantom)

        end: PlayerDetectorCollider = PlayerDetectorCollider(1000, 320, 50, 50, 51, True, Color(0,255,0), game.getScreen(), p)
        colliders.append(end)
        self.end = end

        toDisplay: list[Object] = []
        toDisplay += colliders

        testImage: Image = Image(0,0,50,50,"background.jpg",game.getScreen())
        toDisplay.append(testImage)

        defaultFont32 = pygame.font.Font(
            pygame.font.get_default_font(),
            32
        )

        text = "V"
        textSize = defaultFont32.size(text)

        testText: DynamicText = DynamicText(
            text,
            None,
            32,
            Color(0,0,0),
            None,
            0,
            500,
            textSize[0],
            textSize[1],
            game.getScreen()
        )

        toDisplay.append(testText)
        self.testText = testText

        endText: DynamicText = DynamicText(
            "",
            None,
            32,
            Color(0,0,0),
            None,
            FRAME_WIDTH // 2 - 200,
            FRAME_HEIGHT // 2 - 200,
            400,
            400,
            game.getScreen()
        )

        toDisplay.append(endText)

        self.endText = endText

        actuators: list[ActuatorCollider] = []
        actuators.append(
            ActuatorCollider(150,260, 20,10, end,"", game.getScreen())
        )

        toDisplay += actuators

        self.toDisplay = toDisplay
        self.colliders = colliders
        self.actuators = actuators

        self.activePlayer = p
        self.p = p
        self.phantom = phantom

        game.setToRun(self.mainLoop)
        self.game = game

    def closeMenu(self, button: TextButton|None = None):
        self.menu = None

    def mainLoop(self, game: Game):
        activePlayer: Player = self.activePlayer
        p: Player = self.p
        phantom: PhantomPlayer = self.phantom
        actuators: list[ActuatorCollider] = self.actuators
        end: PlayerDetectorCollider = self.end
        endText: DynamicText = self.endText
        testText: DynamicText = self.testText

        keyPressedMap = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if self.menu != None:
                    if event.dict["unicode"] == "\x1b":
                        self.closeMenu()
                else:
                    if event.dict["unicode"] in ["v", "V"]:
                        if activePlayer == p:
                            if phantom.canSetActive():
                                self.activePlayer = phantom
                                p.switchActive()
                                phantom.switchActive()
                        else:
                            self.activePlayer = p
                            p.switchActive()
                            phantom.switchActive()
                    elif event.dict["unicode"] in ["e", "E"]:
                        i = 0
                        stop = False
                        while i < len(actuators) and not stop:
                            if actuators[i].isColliding(activePlayer):
                                actuators[i].actuate()
                                stop = True
                            i += 1
                    elif event.dict["unicode"] == "\x1b": # echap
                        menu = Menu()
                        menu.add(
                            Rectangle(0,0, FRAME_WIDTH, FRAME_HEIGHT, Color(0,0,255, 25), game.getScreen()),
                            TextButton(-1,-1,200,100, "Continuer", None, 32,None, Color(0,255,0), self.game.getScreen(), self.closeMenu)
                        )
                        self.menu = menu
            if event.type == pygame.MOUSEBUTTONDOWN and self.menu != None:
                self.menu.handleClick(event, game)

        testText.setBackgroundColor(None if phantom.canSetActive() or phantom.isActive else Color(0,0,0,140))

        if keyPressedMap[pygame.K_d]:
            activePlayer.xMove += 5
        if keyPressedMap[pygame.K_q]:
            activePlayer.xMove -= 5
        if keyPressedMap[pygame.K_SPACE]:
            activePlayer.jump()

        if self.menu == None:
            p.update()
            phantom.update()

        game.getScreen().fill("white")

        if end.collidePlayer():
            endText.setText("Bravo !")
        else:
            endText.setText("")
        
        for o in self.toDisplay:
            o.show()
        activePlayer.showAt(0,0)
        
        if self.menu != None:
            self.menu.show()
            self.menu.run(game)

#m: Main = Main()

game: Game = Game()
mainMenu: Menu = Menu()

def startGame(btn: TextButton):
    Main(game)

objs: list[Object] = [
    StaticText("Reumarckable",None,32,Color(255,0,0),None,0,0,0,0,game.getScreen()),
    Button(0,0,100,50),
    TextButton(-1,-1,300,80, "Jouer", None, 100, Color(0,255,0), Color(255,0,0), game.getScreen(), startGame),
]
mainMenu.add(*objs)
game.setToRun(mainMenu.run)