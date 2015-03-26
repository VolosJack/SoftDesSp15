import os, pygame
from pygame.constants import RLEACCEL


class Stage:
    """The Base Class for Levels"""

    def __init__(self):
        self.name = "Base Stage"

    def getLayout(self):
        """Get the Layout of the Level"""
        """Returns a [][] list"""
        pass

    def getImages(self, name, colorkey=None):
        """Get a list of all the images used by the level"""
        """Returns a list of all the images used. The indices
        in the layout refer to sprites in the list returned by
        this function"""
        fullname = os.path.join('data', 'images')
        fullname = os.path.join(fullname, name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error, message:
            print('Cannot load image:', fullname)
            raise SystemExit, message
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image, image.get_rect()


class IntroStage(Stage):
    def __init__(self, ):
        Stage.__init__(self)
        self.name = 'Intro Stage'
        img = self.getImages('OregonTrailOld2.png')
