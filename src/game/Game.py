from __future__ import annotations

import pygame
from pygame import Surface
from pygame.time import Clock
import pygame.display as display

from typing import Callable
from threading import Thread

from game.Utils import FRAME_NAME, FRAME_WIDTH, FRAME_HEIGHT, ICON
from game.Image import getImage

class Game:
    screen: Surface|None = None
    clock: Clock
    running: bool = True
    toRun: Callable[[Game], None]

    def __init__(self) -> None:
        self.clock = Clock()
        self.setToRun()

        gameThread: Thread = Thread(target=self.run)
        gameThread.start()

        while self.screen == None:
            pass
    
    def stop(self):
        """Arrête le programme"""
        self.running = False
    
    def run(self):
        """S'éxecute à chaque frame"""
        pygame.init()
        self.screen = display.set_mode( (FRAME_WIDTH, FRAME_HEIGHT) )
        display.set_caption(FRAME_NAME)
        display.set_icon( getImage(ICON) )
        while self.running:
            for _ in pygame.event.get( pygame.QUIT ):
                self.stop()
            
            if self.toRun != None:
                self.toRun(self)
            self.clock.tick(60)
            display.flip()
        pygame.quit()
    
    def setToRun(self, toRun: Callable[[Game], None]|None = None):
        """Défini la fonction à éxecuter à chaque frame (affichage, traitement, ect)."""
        if toRun == None:
            def defaultToRun(game: Game) -> None:
                pass
            toRun = defaultToRun
        self.toRun = toRun
    
    def getScreen(self) -> Surface:
        if self.screen == None:
            self.screen = Surface((0,0))
        return self.screen