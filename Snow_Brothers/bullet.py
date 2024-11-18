from pico2d import *
import game_world
import game_framework

class Bullet:
    image = None

    def __init__(self, x, y, velocity, nick_y):
        if Bullet.image == None:
            Bullet.image = load_image('resources\\bullet\\bullet.png')
        self.x, self.y, self.velocity = x, y, velocity
        self.nick_y = nick_y

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.x += self.velocity * 1
        self.y -= 2

        if self.y <= self.nick_y - 32:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def handle_collision(self, group, other):
        pass