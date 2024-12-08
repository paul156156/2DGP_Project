from pico2d import *
import game_world
from bullet import Bullet
from states import AppearsState

class Nick:
    def __init__(self):
        self.x, self.y = 512 // 2, 96  # 캐릭터 초기 위치
        self.frame = 0  # 애니메이션 프레임 초기화
        self.dir = 0  # 움직임 방향 (0: 정지, 1: 오른쪽, -1: 왼쪽)
        self.face_dir = -1  # 캐릭터가 바라보는 방향 (1: 오른쪽, -1: 왼쪽)
        self.state = AppearsState()  # 초기 상태 설정
        self.vy = 0  # 수직 속도
        self.on_ground = False  # 착지 상태
        self.current_platform = None  # 현재 서 있는 플랫폼
        self.bullets = []  # Nick이 발사한 총알 리스트 추가
        self.hp = 3  # 초기 HP 설정


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
        # bullets 리스트에서 제거된 총알을 필터링
        self.bullets = [bullet for bullet in self.bullets if bullet in game_world.objects]

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

        # 게임 월드에 추가 및 리스트에 저장
        game_world.add_object(bullet, 2)
        self.bullets.append(bullet)

        # 충돌 페어에 새로운 총알 추가
        for enemy in game_world.get_objects_in_layer(1):  # 레이어 1의 적 가져오기
            game_world.add_collision_pair('enemy:bullet', enemy, bullet)

    def get_bb(self):
        return self.x - 15, self.y - 35, self.x + 15, self.y + 15

    def collide_with(self, other):
        left_a, bottom_a, right_a, top_a = self.get_bb()
        left_b, bottom_b, right_b, top_b = other.get_bb()

        if left_a > right_b or right_a < left_b or top_a < bottom_b or bottom_a > top_b:
            return False
        return True

    def on_collision_with_platform(self, platform):
        left, bottom, right, top = platform.get_bb()
        self.y = top + 32  # 플랫폼 위로 위치 조정
        self.vy = 0  # 수직 속도 초기화
        self.on_ground = True  # 착지 상태로 전환
        self.current_platform = platform  # 현재 서 있는 플랫폼 기록

    def on_collision_with_enemy(self, enemy):
        print(f"Nick collided with enemy at ({enemy.x}, {enemy.y})")
        # HP 감소 로직 추가
        self.hp -= 1
        if self.hp <= 0:
            print("Game Over!")
            game_world.remove_object(self)  # Nick 제거 (게임 오버)

    def draw(self):
        self.state.draw(self)
        #draw_rectangle(*self.get_bb())