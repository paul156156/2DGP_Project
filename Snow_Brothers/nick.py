from pico2d import *

class Nick:
    def __init__(self):
        self.x, self.y = 512 // 2, 464 // 2  # 캐릭터 초기 위치
        self.frame = 0  # 애니메이션 프레임 초기화
        self.dir = 0  # 움직임 방향 (0: 정지, 1: 오른쪽, -1: 왼쪽)
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
            'shooting': {'frames': 2, 'width': 16, 'height': 32, 'interval': 1},
            'walk': {'frames': 3, 'width': 16, 'height': 32, 'interval': 1},
        }

    def update(self):
        # 현재 상태에 따른 프레임 업데이트
        self.frame = (self.frame + 1) % self.animations[self.state]['frames']

        if self.state == 'walk':
            self.x += self.dir * 5  # 걷기 상태에서만 캐릭터 이동

        # appear 상태가 끝나면 자동으로 idle 상태로 전환
        if self.state == 'appears' and self.frame == 0:
            self.state = 'idle'

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.dir = 1
                self.state = 'walk'  # 오른쪽으로 이동하면 걷기 상태로 변경
            elif event.key == SDLK_LEFT:
                self.dir = -1
                self.state = 'walk'  # 왼쪽으로 이동하면 걷기 상태로 변경
            elif event.key == SDLK_LALT:
                self.state = 'jump'  # 점프 상태로 변경
            elif event.key == SDLK_LCTRL:
                self.state = 'shooting'  # 공격(발사) 상태로 변경
        elif event.type == SDL_KEYUP:
            if event.key in (SDLK_RIGHT, SDLK_LEFT, SDLK_LALT, SDLK_LCTRL):
                self.dir = 0  # 이동 멈추면 정지
                self.state = 'idle'  # 모든 동작 후 idle 상태로 변경

    def draw(self):
        # 현재 상태에 맞는 애니메이션 정보 가져오기
        animation = self.animations[self.state]

        # 캐릭터 크기를 2배로 그리기 위해 width와 height를 2배로 설정
        draw_width = animation['width'] * 2
        draw_height = animation['height'] * 2

        # 현재 상태에 맞는 이미지와 프레임을 그리기
        if self.state == 'appears':
            self.image_appears.clip_draw(
                self.frame * (animation['width'] + animation['interval']),  # 프레임 간 간격 적용
                0, animation['width'], animation['height'], self.x, self.y, draw_width, draw_height)

        elif self.state == 'idle':
            self.image_idle.clip_draw(
                0, 0, animation['width'], animation['height'], self.x, self.y, draw_width, draw_height)  # Idle은 한 프레임만 사용

        elif self.state == 'jump':
            self.image_jump.clip_draw(
                self.frame * (animation['width'] + animation['interval']),  # 프레임 간 간격 적용
                0, animation['width'], animation['height'], self.x, self.y, draw_width, draw_height)

        elif self.state == 'shooting':
            self.image_shooting.clip_draw(
                self.frame * (animation['width'] + animation['interval']),  # 프레임 간 간격 적용
                0, animation['width'], animation['height'], self.x, self.y, draw_width, draw_height)

        elif self.state == 'walk':
            self.image_walk.clip_draw(
                self.frame * (animation['width'] + animation['interval']),  # 프레임 간 간격 적용
                0, animation['width'], animation['height'], self.x, self.y, draw_width, draw_height)
