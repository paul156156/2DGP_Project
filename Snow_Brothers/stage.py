from pico2d import *

class Stage:
    def __init__(self):
        # 배경 이미지를 로드합니다.
        self.image = load_image('resources\\stage\\floor_1.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(512/2, 464/2, 512, 464)  # 화면 중심 좌표 (가로 800, 세로 600 기준)
