from pico2d import *
import game_world
from bullet import Bullet
from states import AppearsState

GRAVITY = -500  # 중력 값 (픽셀/초^2)
GROUND_Y = 90   # 바닥 y 좌표 (플랫폼이 없을 때 착지하는 기본 높이)

class Nick:
    def __init__(self):
        self.x, self.y = 512 // 2, 90  # 캐릭터 초기 위치
        self.frame = 0  # 애니메이션 프레임 초기화
        self.dir = 0  # 움직임 방향 (0: 정지, 1: 오른쪽, -1: 왼쪽)
        self.face_dir = -1  # 캐릭터가 바라보는 방향 (1: 오른쪽, -1: 왼쪽)
        self.state = AppearsState()  # 초기 상태 설정

        # 이미지 로드 (각 상태에 맞는 이미지 파일 로드)
        self.image_appears = load_image('resources\\nick\\nick_appears.png')
        self.image_idle = load_image('resources\\nick\\nick_idle.png')
        self.image_walk = load_image('resources\\nick\\nick_walk.png')
        self.image_jump = load_image('resources\\nick\\nick_jump.png')
        self.image_shooting = load_image('resources\\nick\\nick_shooting.png')

        # 각 상태의 애니메이션 정보 (프레임 수와 간격)
        self.animations = {
            'appears': {'frames': 6, 'width': 16, 'height': 32, 'interval': 1},
            'idle': {'frames': 1, 'width': 16, 'height': 32},
            'jump': {'frames': 4, 'width': 16, 'height': 32, 'interval': 1},
            'shooting': {'frames': 2, 'width': 24, 'height': 24, 'interval': 1},
            'walk': {'frames': 3, 'width': 16, 'height': 32, 'interval': 1},
        }

    def update(self):
        self.state.update(self)

    def handle_event(self, event):
        self.state.handle_event(self, event)

    def change_state(self, new_state):
        self.state.exit(self)
        self.state = new_state
        self.state.enter(self)

    def shoot_bullet(self):
        offset = 20
        bullet_x = self.x + self.face_dir * offset
        bullet_strength = 0
        bullet = Bullet(bullet_x, self.y, bullet_strength, self.face_dir)
        game_world.add_object(bullet, 1)

    def get_bb(self):
        return self.x - 20, self.y - 40, self.x + 20, self.y + 20

    def collide_with(self, other):
        left_a, bottom_a, right_a, top_a = self.get_bb()
        left_b, bottom_b, right_b, top_b = other.get_bb()

        if left_a > right_b or right_a < left_b or top_a < bottom_b or bottom_a > top_b:
            return False
        return True

    def on_collision_with_platform(self, platform):
        left, bottom, right, top = platform.get_bb()
        self.y = top + 20  # 플랫폼 위로 위치 조정
        self.vy = 0  # 수직 속도 초기화
        self.on_ground = True  # 착지 상태로 전환

    def draw(self):
        self.state.draw(self)
        draw_rectangle(*self.get_bb())