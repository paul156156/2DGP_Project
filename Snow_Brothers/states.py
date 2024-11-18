from pico2d import *
import game_framework

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
        nick.x += nick.dir * nick.speed * game_framework.frame_time

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
        nick.start_y = nick.y  # 점프 시작 시 초기 y 위치를 저장
        nick.jumping = True

    @staticmethod
    def update(nick):
        nick.frame = (nick.frame + 15 * game_framework.frame_time) % nick.animations['jump']['frames']
        if nick.jumping:
            if nick.y <= nick.start_y + 64:
                nick.y += 150 * game_framework.frame_time  # y 좌표를 증가시켜 점프
            else:
                nick.y = nick.start_y + 64  # 최대 높이를 제한
                nick.jumping = False  # 점프 완료
                nick.change_state(IdleState)  # Idle 상태로 전환

    @staticmethod
    def handle_event(nick, event):
        #if event.type == SDL_KEYUP and event.key == SDLK_LALT:
            #nick.change_state(IdleState)
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