import game_framework
import game_world
from pico2d import *

from nick import Nick
from stage import Stage

#nick = None

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            nick.handle_event(event)

def init():
    global nick

    stage = Stage()
    game_world.add_object(stage, 0)  # 레이어 0에 추가

    nick = Nick()
    game_world.add_object(nick, 1)  # 레이어 1에 추가

def update():
    game_world.update()  # 모든 오브젝트 업데이트

def draw():
    clear_canvas()
    game_world.render()  # 모든 오브젝트 렌더링
    update_canvas()

def pause():
    pass

def resume():
    pass

def finish():
    game_world.clear()  # 모든 오브젝트 제거
