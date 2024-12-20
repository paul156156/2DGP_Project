from pico2d import (load_image, get_events, clear_canvas, update_canvas
, SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE)
import game_framework
import play_mode
from pico2d import load_music

bgm = None

def init():
    global image, frame, elapsed_time, animation_done, bgm
    image = load_image('resources\\title\\title.png')  # 스프라이트 이미지 로드
    bgm = load_music('resources\\music\\01 Start.mp3')  # 음악 파일 로드
    bgm.set_volume(64)  # 음악 볼륨 설정 (0~128)
    bgm.repeat_play()  # 반복 재생

    frame = 0  # 현재 프레임 초기화
    elapsed_time = 0  # 경과 시간 초기화
    animation_done = False  # 애니메이션 완료 여부

def finish():
    global image, bgm
    del image
    bgm.stop()  # 음악 중지
    del bgm

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            game_framework.change_mode(play_mode)

def draw():
    global frame
    clear_canvas()

    frame_width = 1024 // 4
    frame_height = 232
    interval = 1

    frame_x = frame * (frame_width + interval)

    image.clip_draw(frame_x, 0, frame_width, frame_height, 512 // 2, 464 // 2, 512, 464)

    update_canvas()

def update():
    global frame, elapsed_time, animation_done
    if not animation_done:
        elapsed_time += game_framework.frame_time

        if elapsed_time > 1:
            frame += 1
            elapsed_time = 0
            if frame >= 3:
                frame = 3
                animation_done = True

def pause(): pass
def resume(): pass
