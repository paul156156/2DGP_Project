from pico2d import *
import game_world
import game_framework

class Bullet:
    image = None

    def __init__(self, x, y, strength, face_dir):
        self.x, self.y, self.strength = x, y, strength
        self.nick_y = y
        self.face_dir = face_dir

        if Bullet.image == None:
            if self.strength == 0:
                Bullet.image = load_image('resources\\bullet\\bullet.png')
            else:
                Bullet.image = load_image('resources\\bullet\\reinforced_bullet.png')


    def draw(self):
        if self.face_dir == 1:  # 오른쪽을 바라보는 경우
            self.image.clip_composite_draw(
                0, 0, self.image.w, self.image.h,  # 원본 이미지의 너비와 높이 사용
                0, 'h',  # 0도 회전, 수평 반전
                self.x, self.y,  # 그릴 위치
                self.image.w, self.image.h  # 원본 크기 그대로 그리기
            )
        else:  # 왼쪽을 바라보는 경우
            self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        if self.face_dir == 1:
            self.x += 5
        else:
            self.x -= 5
        self.y -= 2

        if self.y <= self.nick_y - 32:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def handle_collision(self, group, other):
        pass