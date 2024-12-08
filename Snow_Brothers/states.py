from pico2d import *
import game_framework
import game_world

GRAVITY = -500  # 중력 값 (픽셀/초^2)
GROUND_Y = 96   # 바닥 y 좌표 (플랫폼이 없을 때 착지하는 기본 높이)

class State:
    @staticmethod
    def enter(nick):
        pass

    @staticmethod
    def exit(nick):
        pass

    @staticmethod
    def update(nick):
        pass

    @staticmethod
    def handle_event(nick, event):
        pass

    @staticmethod
    def draw(nick):
        pass

class AppearsState(State):
    @staticmethod
    def enter(nick):
        nick.frame = 0

    @staticmethod
    def update(nick):
        nick.frame = (nick.frame + 10 * game_framework.frame_time) % nick.animations['appears']['frames']
        if int(nick.frame) == nick.animations['appears']['frames'] - 1:
            nick.change_state(IdleState)

    @staticmethod
    def draw(nick):
        draw_width = nick.animations['appears']['width'] * 2
        draw_height = nick.animations['appears']['height'] * 2
        nick.image_appears.clip_draw(int(nick.frame) * nick.animations['appears']['width'], 0,
                                     nick.animations['appears']['width'], nick.animations['appears']['height'],
                                     nick.x, nick.y, draw_width, draw_height)

class IdleState(State):
    @staticmethod
    def enter(nick):
        nick.frame = 0
        nick.speed = 0  # Idle 상태에서는 이동하지 않음

    @staticmethod
    def update(nick):
        nick.frame = (nick.frame + 30 * game_framework.frame_time) % nick.animations['idle']['frames']

        # 중력 적용: 플랫폼 위에 있지 않은 경우 아래로 떨어짐
        if not nick.on_ground or nick.current_platform is None:
            nick.vy += 3 * GRAVITY * game_framework.frame_time
            nick.y += nick.vy * game_framework.frame_time

            # 하강 중 다른 플랫폼과의 충돌 확인
            for obj in game_world.get_objects_in_layer(0):  # 0번 레이어에서 플랫폼 가져오기
                if hasattr(obj, 'get_bb'):
                    left, bottom, right, top = obj.get_bb()
                    if nick.vy < 0 and bottom < nick.y <= top and left <= nick.x <= right:  # 아래 플랫폼만 감지
                        nick.on_collision_with_platform(obj)
                        return

            # 바닥 충돌 처리
            if nick.y < GROUND_Y:
                nick.y = GROUND_Y
                nick.vy = 0
                nick.on_ground = True
                nick.current_platform = None

    @staticmethod
    def handle_event(nick, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                nick.dir = 1
                nick.face_dir = 1
                nick.change_state(WalkState)
            elif event.key == SDLK_LEFT:
                nick.dir = -1
                nick.face_dir = -1
                nick.change_state(WalkState)
            elif event.key == SDLK_LALT:
                nick.change_state(JumpState)
            elif event.key == SDLK_LCTRL:
                nick.change_state(ShootingState)

    @staticmethod
    def draw(nick):
        draw_width = nick.animations['idle']['width'] * 2
        draw_height = nick.animations['idle']['height'] * 2
        flip = 'h' if nick.face_dir > 0 else ''
        nick.image_idle.clip_composite_draw(
            0, 0, nick.animations['idle']['width'], nick.animations['idle']['height'],
            0, flip,
            nick.x, nick.y,
            draw_width, draw_height
        )


class WalkState(State):
    @staticmethod
    def enter(nick):
        nick.frame = 0
        nick.speed = 150  # Walk 상태에서 이동 속도 설정

    @staticmethod
    def update(nick):
        nick.frame = (nick.frame + 30 * game_framework.frame_time) % nick.animations['walk']['frames']

        # 이동 방향에 따른 새로운 x 좌표 계산
        new_x = nick.x + nick.dir * nick.speed * game_framework.frame_time

        # 플랫폼 위에 있을 경우에만 이동 가능
        if nick.on_ground and nick.current_platform:
            left, bottom, right, top = nick.current_platform.get_bb()
            if left <= new_x <= right:  # 플랫폼 범위 내에서만 이동 허용
                nick.x = new_x
            else:
                # 플랫폼을 벗어나면 떨어지도록 설정
                nick.on_ground = False
                nick.current_platform = None
                #nick.vy = 0  # 중력 적용을 위한 초기 속도 설정
        else:
            # Nick이 플랫폼을 벗어난 경우 중력 적용
            nick.x = new_x
            nick.vy += 3 * GRAVITY * game_framework.frame_time
            nick.y += nick.vy * game_framework.frame_time

            # 하강 중 다른 플랫폼과의 충돌 확인
            for obj in game_world.get_objects_in_layer(0):  # 0번 레이어의 플랫폼 가져오기
                if hasattr(obj, 'get_bb'):
                    left, bottom, right, top = obj.get_bb()
                    if nick.vy < 0 and bottom < nick.y <= top and left <= nick.x <= right:  # 아래 플랫폼만 감지
                        nick.on_collision_with_platform(obj)
                        return

            # 바닥 충돌 처리
            if nick.y < GROUND_Y:
                nick.y = GROUND_Y
                nick.vy = 0
                nick.on_ground = True

    @staticmethod
    def handle_event(nick, event):
        if event.type == SDL_KEYUP and event.key in (SDLK_RIGHT, SDLK_LEFT):
            nick.dir = 0
            nick.change_state(IdleState)

    @staticmethod
    def draw(nick):
        draw_width = nick.animations['walk']['width'] * 2
        draw_height = nick.animations['walk']['height'] * 2
        flip = 'h' if nick.face_dir > 0 else ''
        nick.image_walk.clip_composite_draw(
            int(nick.frame) * nick.animations['walk']['width'], 0,
            nick.animations['walk']['width'], nick.animations['walk']['height'],
            0, flip,
            nick.x, nick.y,
            draw_width, draw_height
        )

class JumpState(State):
    @staticmethod
    def enter(nick):
        nick.frame = 0
        nick.vy = 250  # 점프 초기 속도 (양수: 위로 상승)
        nick.on_ground = False  # 점프 중에는 공중 상태

    @staticmethod
    def update(nick):
        nick.frame = (nick.frame + 15 * game_framework.frame_time) % nick.animations['jump']['frames']

        # 중력 적용
        nick.vy += GRAVITY * game_framework.frame_time
        nick.y += nick.vy * game_framework.frame_time

        # 착지할 때만 플랫폼 충돌 확인
        if nick.vy < 0:  # Nick이 하강 중일 때만 충돌 확인
            for obj in game_world.get_objects_in_layer(0):  # 0번 레이어에서 플랫폼 가져오기
                if hasattr(obj, 'get_bb') and nick.collide_with(obj):  # Nick과 플랫폼 충돌
                    nick.on_collision_with_platform(obj)
                    nick.change_state(IdleState)  # 충돌 시 Idle 상태로 전환
                    return

        # 바닥 충돌 확인
        if nick.y <= GROUND_Y:
            nick.y = GROUND_Y
            nick.vy = 0
            nick.on_ground = True
            nick.change_state(IdleState)  # 바닥에 닿으면 Idle 상태로 전환

    @staticmethod
    def handle_event(nick, event):
        pass

    @staticmethod
    def draw(nick):
        draw_width = nick.animations['jump']['width'] * 2
        draw_height = nick.animations['jump']['height'] * 2
        flip = 'h' if nick.face_dir > 0 else ''
        nick.image_jump.clip_composite_draw(
            int(nick.frame) * nick.animations['jump']['width'], 0,
            nick.animations['jump']['width'], nick.animations['jump']['height'],
            0, flip,
            nick.x, nick.y,
            draw_width, draw_height
        )


class ShootingState(State):
    @staticmethod
    def enter(nick):
        nick.frame = 0
        nick.shoot_bullet()

    @staticmethod
    def update(nick):
        nick.frame = (nick.frame + 15 * game_framework.frame_time) % nick.animations['shooting']['frames']

    @staticmethod
    def handle_event(nick, event):
        if event.type == SDL_KEYUP and event.key == SDLK_LCTRL:
            nick.change_state(IdleState)

    @staticmethod
    def draw(nick):
        #draw_height = nick.animations['shooting']['height'] * 2
        draw_height = 32 * 2  # 확대된 높이
        flip = 'h' if nick.face_dir > 0 else ''  # 오른쪽을 바라볼 때 수평 반전

        # 프레임별 크기와 간격 설정
        if int(nick.frame) == 0:
            frame_width = 24
            frame_x = 0  # 첫 번째 프레임은 시작 위치가 0
        else:
            frame_width = 16
            frame_x = 24 + 1  # 두 번째 프레임의 시작 위치는 첫 번째 프레임의 끝 + 간격 1

        nick.image_shooting.clip_composite_draw(
            frame_x, 0,
            frame_width, 32,  # 현재 프레임의 너비와 높이 (높이를 32로 설정)
            0, flip,
            nick.x, nick.y,
            frame_width * 2, draw_height  # 2배 확대하여 그리기
        )