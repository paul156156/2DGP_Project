from pico2d import *

class Stage:
    def __init__(self):
        # 배경 이미지를 로드합니다.
        self.image = load_image('resources\\stage\\floor_1.png')

    def update(self):
        # 만약 스크롤이 필요하다면 업데이트 로직을 추가할 수 있습니다.
        # 지금은 정적 배경이므로 특별한 업데이트는 필요하지 않습니다.
        pass

    def draw(self):
        # 배경 이미지를 화면에 그립니다.
        # 예를 들어, 전체 화면을 덮는 배경을 그릴 수 있습니다.
        self.image.draw(512/2, 464/2, 512, 464)  # 화면 중심 좌표 (가로 800, 세로 600 기준)
