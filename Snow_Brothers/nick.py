from pico2d import *
import game_world
from bullet import Bullet

class Nick:
    def __init__(self):
        self.x, self.y = 512 // 2, 90  # 캐릭터 초기 위치
        self.frame = 0  # 애니메이션 프레임 초기화
        self.dir = 0  # 움직임 방향 (0: 정지, 1: 오른쪽, -1: 왼쪽)
        self.face_dir = -1  # 캐릭터가 바라보는 방향 (1: 오른쪽, -1: 왼쪽)
        self.state = 'appears'  # 초기 상태는 화면 등장 상태

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
        # 현재 상태에 따른 프레임 업데이트
        self.frame = (self.frame + 0.25) % self.animations[self.state]['frames']

        if self.state == 'walk':
            self.x += self.dir * 5  # 걷기 상태에서만 캐릭터 이동

        # appear 상태가 끝나면 자동으로 idle 상태로 전환
        if self.state == 'appears' and self.frame == 0:
            self.state = 'idle'

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.dir = 1
                self.face_dir = 1  # 오른쪽으로 이동하면 오른쪽을 바라보게 함
                self.state = 'walk'  # 오른쪽으로 이동하면 걷기 상태로 변경
            elif event.key == SDLK_LEFT:
                self.dir = -1
                self.face_dir = -1 # 왼쪽으로 이동하면 왼쪽을 바라보게 함
                self.state = 'walk'  # 왼쪽으로 이동하면 걷기 상태로 변경
            elif event.key == SDLK_LALT:
                self.state = 'jump'  # 점프 상태로 변경
                self.y += 32 * 2  # 점프 상태에서는 y좌표를 64만큼 증가
            elif event.key == SDLK_LCTRL:
                self.state = 'shooting'  # 공격(발사) 상태로 변경
                self.shoot_bullet()  # 총알 발사
        elif event.type == SDL_KEYUP:
            if event.key in (SDLK_RIGHT, SDLK_LEFT, SDLK_LALT, SDLK_LCTRL):
                self.dir = 0  # 이동 멈추면 정지
                self.state = 'idle'  # 모든 동작 후 idle 상태로 변경

    def shoot_bullet(self):
        # 총알이 Nick의 위치에서 발사되며 바라보는 방향으로 생성
        offset = 1  # Nick으로부터 총알의 초기 거리 오프셋
        bullet_x = self.x + self.face_dir * offset  # Nick의 앞에서 시작
        bullet_velocity = self.face_dir * 5  # 바라보는 방향으로 발사 속도 설정
        bullet = Bullet(bullet_x, self.y, bullet_velocity, self.y)
        game_world.add_object(bullet, 1)  # game_world에 총알 추가

    def get_bb(self):
        return self.x - 20, self.y - 40, self.x + 20, self.y + 20

    def draw(self):
        # 현재 상태에 맞는 애니메이션 정보 가져오기
        animation = self.animations[self.state]

        # 캐릭터 크기를 2배로 그리기 위해 width와 height를 2배로 설정
        draw_width = animation['width'] * 2
        draw_height = animation['height'] * 2
        flip = self.face_dir > 0  # 캐릭터가 오른쪽을 바라보면 flip을 False로 설정

        # 현재 상태에 맞는 이미지와 프레임을 그리기
        if self.state == 'appears':
            self.image_appears.clip_composite_draw(
                int(self.frame) * (animation['width'] + animation['interval']), 0,
                animation['width'], animation['height'],
                0, 'h' if flip else '',  # flip 값에 따라 좌우 반전 적용
                self.x, self.y, draw_width, draw_height)

        elif self.state == 'idle':
            self.image_idle.clip_composite_draw(
                0, 0, animation['width'], animation['height'],
                0, 'h' if flip else '',
                self.x, self.y, draw_width, draw_height)

        elif self.state == 'jump':
            self.image_jump.clip_composite_draw(
                int(self.frame) * (animation['width'] + animation['interval']), 0,
                animation['width'], animation['height'],
                0, 'h' if flip else '',
                self.x, self.y, draw_width, draw_height)

        elif self.state == 'shooting':
            self.image_shooting.clip_composite_draw(
                int(self.frame) * (animation['width'] + animation['interval']), 0,
                animation['width'], animation['height'],
                0, 'h' if flip else '',
                self.x, self.y - 12, draw_width, draw_height)

        elif self.state == 'walk':
            self.image_walk.clip_composite_draw(
                int(self.frame) * (animation['width'] + animation['interval']), 0,
                animation['width'], animation['height'],
                0, 'h' if flip else '',
                self.x, self.y, draw_width, draw_height)

        draw_rectangle(*self.get_bb())