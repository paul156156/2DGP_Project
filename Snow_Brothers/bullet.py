from pico2d import *
import game_world
import game_framework

class Bullet:
    image = None

    def __init__(self, x, y, strength, face_dir):
        self.x, self.y, self.strength = x, y, strength
        self.nick_y = y
        self.face_dir = face_dir
        self.velocity_x = 150
        self.velocity_y = 75
        self.gravity = -500

        if Bullet.image == None:
            if self.strength == 0:
                Bullet.image = load_image('resources\\bullet\\bullet.png')
            else:
                Bullet.image = load_image('resources\\bullet\\reinforced_bullet.png')


    def draw(self):
        draw_width = self.image.w * 2  # 2배 크기로 설정
        draw_height = self.image.h * 2  # 2배 크기로 설정

        if self.face_dir == 1:  # 오른쪽을 바라보는 경우
            self.image.clip_composite_draw(
                0, 0, self.image.w, self.image.h,  # 원본 이미지의 너비와 높이 사용
                0, 'h',  # 0도 회전, 수평 반전
                self.x, self.y,  # 그릴 위치
                draw_width, draw_height  # 2배 크기로 그리기
            )
        else:  # 왼쪽을 바라보는 경우
            self.image.clip_composite_draw(
                0, 0, self.image.w, self.image.h,  # 원본 이미지의 너비와 높이 사용
                0, '',  # 0도 회전, 수평 반전 없음
                self.x, self.y,  # 그릴 위치
                draw_width, draw_height  # 2배 크기로 그리기
            )
        #draw_rectangle(*self.get_bb())

    def update(self):
        if self.face_dir == 1:
            self.x += self.velocity_x * game_framework.frame_time  # 오른쪽으로 이동
        else:
            self.x -= self.velocity_x * game_framework.frame_time  # 왼쪽으로 이동

        # 중력에 의한 속도와 위치 변화
        self.y += self.velocity_y * game_framework.frame_time  # 수직 속도에 따른 위치 변화
        self.velocity_y += self.gravity * game_framework.frame_time  # 중력 가속도에 따른 속도 감소

        # 특정 높이 이하로 떨어지면 제거
        if self.y <= self.nick_y - 32:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 5, self.y - 10, self.x + 5, self.y + 10

    def handle_collision(self, group, other):
        if group == 'enemy:bullet':
            print(f"Bullet collided with enemy at ({self.x}, {self.y})")
            game_world.remove_object(self)  # 충돌 후 Bullet 제거
