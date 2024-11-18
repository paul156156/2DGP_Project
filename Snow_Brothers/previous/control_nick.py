from pico2d import *

from nick import Nick
from stage import Stage


# Game object class here


def handle_events(nick):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            return False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            return False
        else:
            nick.handle_event(event)
    return True


def reset_world():
    world = []

    stage = Stage()
    world.append(stage)

    nick = Nick()
    world.append(nick)

    return world, nick


def update_world(world):
    for obj in world:
        obj.update()


def render_world(world):
    clear_canvas()
    for obj in world:
        obj.draw()
    update_canvas()


open_canvas(512,464)
world, nick = reset_world()
running = True

# game loop
while running:
    running = handle_events(nick)  # handle_events가 False를 반환하면 종료
    update_world(world)
    render_world(world)
    delay(0.03)

# finalization code
close_canvas()
