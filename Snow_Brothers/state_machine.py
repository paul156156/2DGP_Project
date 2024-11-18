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

class WalkState(State):
    @staticmethod
    def enter(nick):
        nick.frame = 0
        nick.speed = 150  # Walk 상태에서 이동 속도 설정

    @staticmethod
    def update(nick):
        nick.frame = (nick.frame + 30 * game_framework.frame_time) % nick.animations['walk']['frames']

    @staticmethod
    def handle_event(nick, event):
        if event.type == SDL_KEYUP and event.key in (SDLK_RIGHT, SDLK_LEFT):
            nick.dir = 0
            nick.change_state(IdleState)

class JumpState(State):
    @staticmethod
    def enter(nick):
        nick.frame = 0

    @staticmethod
    def update(nick):
        nick.frame = (nick.frame + 20 * game_framework.frame_time) % nick.animations['jump']['frames']
        nick.y += 100 * game_framework.frame_time  # 간단한 점프 로직

    @staticmethod
    def handle_event(nick, event):
        if event.type == SDL_KEYUP and event.key == SDLK_LALT:
            nick.change_state(IdleState)

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
