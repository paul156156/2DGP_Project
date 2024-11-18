from pico2d import *

class Stage:
    def __init__(self):
        self.image = load_image('resources\\stage\\floor_1.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(512/2, 464/2, 512, 464)
