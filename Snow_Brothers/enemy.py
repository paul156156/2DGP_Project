from pico2d import *
import game_framework
import game_world
from bullet import Bullet
from nick import Nick

class Enemy:
    def __init__(self, x, y, platform):
        self.x, self.y = x, y  # 적의 초기 위치
        self.vx = 25  # 적의 속도 (픽셀/초)
        self.direction = 1  # 이동 방향 (1: 오른쪽, -1: 왼쪽)
        self.width, self.height = 32, 32  # 적의 크기
        self.platform = platform  # 적이 속한 플랫폼 객체

        # 이미지 로드
        self.image_idle = load_image('resources\\enemy\\enemy_1_idle.png')
        self.image_walk = load_image('resources\\enemy\\enemy_1_walk.png')

        # 애니메이션 정보
        self.animations = {
            'idle': {'frames': 1, 'width': 24, 'height': 32},
            'walk': {'frames': 2, 'width': 24, 'height': 32, 'frame_gap': 1},  # 1픽셀 간격
        }

        self.current_state = 'idle'  # 현재 상태
        self.frame = 0

    def update(self):
        # 이동 상태로 변경
        self.current_state = 'walk'

        # 좌우 이동
        self.x += self.direction * self.vx * game_framework.frame_time

        # 플랫폼 경계 내로 제한
        platform_left = self.platform.x * 2
        platform_right = (self.platform.x + self.platform.width) * 2

        if self.x <= platform_left or self.x >= platform_right:
            self.direction *= -1  # 방향 반전
            self.x = max(min(self.x, platform_right), platform_left)  # x좌표 경계 내로 보정

        # 애니메이션 프레임 업데이트
        anim = self.animations[self.current_state]
        self.frame = (self.frame + 5 * game_framework.frame_time) % anim['frames']

    def draw(self):
        # 현재 상태의 애니메이션 정보
        anim = self.animations[self.current_state]
        image = self.image_idle if self.current_state == 'idle' else self.image_walk
        frame_width = anim['width']
        frame_height = anim['height']
        frame_gap = anim.get('frame_gap', 0)  # 프레임 간 간격
        frame_x = int(self.frame) * (frame_width + frame_gap)  # 정확한 프레임 위치 계산

        # 이동 방향에 따라 좌우 반전 설정
        flip = 'h' if self.direction > 0 else ''  # 오른쪽: 반전(h), 왼쪽: 그대로

        # 적 스프라이트 그리기
        image.clip_composite_draw(
            frame_x, 0, frame_width, frame_height,  # 현재 프레임의 클립 영역
            0, flip,  # 회전 각도와 수평/수직 반전 설정
            self.x, self.y, frame_width * 2, frame_height * 2  # 화면에 2배 크기로 출력
        )

        #draw_rectangle(*self.get_bb())

    def get_bb(self):
        # 적의 Bounding Box 계산
        return self.x - 25, self.y - 30, self.x + 25, self.y + 20

    def handle_collision(self, other):
        if isinstance(other, Bullet):  # Bullet과 충돌 시
            print(f"Enemy hit by bullet at ({self.x}, {self.y})")
            game_world.remove_object(self)  # 적 제거

        elif isinstance(other, Nick):
            print(f"Enemy collided with Nick at ({self.x}, {self.y})")

def create_enemies(platforms):
    enemies = []
    for platform in platforms:
        # 적의 위치는 플랫폼의 중앙 x좌표와 위쪽 y좌표 기준
        enemy_x = (platform.x + platform.width) * 2
        enemy_y = (platform.y + platform.height + 16) * 2  # 적이 플랫폼 위에 위치하도록 y좌표 보정

        # 적 객체 생성
        enemy = Enemy(enemy_x, enemy_y, platform)

        # 적을 게임 월드에 추가
        import game_world
        game_world.add_object(enemy, 1)  # 레이어 1에 적 추가

        enemies.append(enemy)

    return enemies
