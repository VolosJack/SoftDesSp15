import os, sys
import pygame
from pygame import *
import pygcurse as pygcurse
import eztext

WIN_WIDTH = 680
WIN_HEIGHT = 480

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)

levels = {0: {'Name': 'Main', 'Image': 'data/images/TeamChoice.png'}, 1: {'Name': 'Learn', 'Image': 'data/images/OregonTrailInfo.png'}}


class Scene(object):

    def __init__(self):
        pass

    def render(self, screen):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError


class GameScene(Scene):
    def __init__(self, level):
        super(GameScene, self).__init__()
        self.bg = Surface((0,0))
        self.bg.convert()
        self.bg.fill(Color("#000000"))

        self.levelno = level

        levelinfo = levels[level]

        self.txtbx = eztext.Input(maxlength=1, x=410, y=350, restricted="123456", color=(255, 255, 255),
                                  font=pygame.font.Font("data/fonts/Here-Lies-MECC.ttf", 17))

        self.img = pygame.image.load(str(levelinfo['Image'])).convert()
        self.input = None

    def render(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.img, (0, 0))
        self.txtbx.draw(screen)

    def update(self):
        pass

    def handle_events(self, events):
        pass


class CustomScene(object):

    def __init__(self, text):
        self.text = text
        super(CustomScene, self).__init__()
        self.font = pygame.font.Font("data/fonts/Here-Lies-MECC.ttf", 17)

    def render(self, screen):
        # ugly!
        screen.fill((0, 0, 0))
        text1 = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text1, (200, 50))

    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == KEYDOWN:
                self.manager.go_to(TitleScene())


class TitleScene(object):
    def __init__(self):
        super(TitleScene, self).__init__()
        self.txtbx = eztext.Input(maxlength=1, x=410, y=350, restricted="123456", color=(255, 255, 255),
                                  font=pygame.font.Font("data/fonts/Here-Lies-MECC.ttf", 17))
        self.img = pygame.image.load('data/images/OregonTrailOld2.png').convert()
        self.input = None

    def render(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.img, (0, 0))
        self.txtbx.draw(screen)

    def update(self):
        pass

    def handle_events(self, events):
        self.txtbx.update(events)
        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_1 or e.key == K_2 or e.key == K_3 or e.key == K_4 or e.key == K_5 or e.key == K_6:
                    self.input = e.key-49
                elif e.key == K_RETURN and not self.input == None:
                    self.manager.go_to(GameScene(self.input))


class SceneManager(object):
    def __init__(self):
        self.go_to(TitleScene())

    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self


def main():
    global HEALTH

    HEALTH = 5
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    screen.fill((0, 0, 0))
    timer = pygame.time.Clock()

    manager = SceneManager()

    while HEALTH > 0:
        # make sure the program is running at 30 fps
        timer.tick(60)

        # events for txtbx
        if pygame.event.get(QUIT):
            HEALTH = 0
            return
        # process other events
        manager.scene.handle_events(pygame.event.get())
        manager.scene.update()
        manager.scene.render(screen)
        pygame.display.flip()
        # clear the screen
        screen.fill((255, 255, 255))

if __name__ == '__main__':
    main()