from pico2d import *

SCALE = 2   # 2배 확대

class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_bb(self):
        return (
            self.x * SCALE,
            self.y * SCALE,
            (self.x + self.width) * SCALE,
            (self.y + self.height) * SCALE
        )

    def draw(self):
        #draw_rectangle(self.x * SCALE,self.y * SCALE,(self.x + self.width) * SCALE,(self.y + self.height) * SCALE)
        pass

    def update(self):
        pass

platform_data = [
    {"x": 0, "y": 64 - 16, "width": 64, "height": 16},  # 1층 1번
    {"x": 96, "y": 64 - 16, "width": 64, "height": 16},  # 1층 2번
    {"x": 192, "y": 64 - 16, "width": 64, "height": 16},  # 1층 3번
    {"x": 48, "y": 96 - 16, "width": 160, "height": 16},  # 2층
    {"x": 0, "y": 128 - 16, "width": 112, "height": 16},  # 3층 1번
    {"x": 144, "y": 128 - 16, "width": 112, "height": 16},  # 3층 2번
    {"x": 32, "y": 160 - 16, "width": 32, "height": 16},  # 4층 1번
    {"x": 192, "y": 160 -16, "width": 32, "height": 16},  # 4층 2번
    {"x": 64, "y": 176 - 16, "width": 128, "height": 16},  # 5층
]

# 플랫폼 객체 생성
def create_platforms():
    return [Platform(data['x'], data['y'], data['width'], data['height']) for data in platform_data]