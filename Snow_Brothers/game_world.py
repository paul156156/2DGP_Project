objects = []  # 게임 오브젝트를 관리할 리스트 (2D 리스트로 레이어별 관리)
collision_pairs = []  # 충돌 처리용 쌍 리스트

def add_object(obj, layer):
    """ 게임 오브젝트를 특정 레이어에 추가 """
    while len(objects) <= layer:
        objects.append([])
    objects[layer].append(obj)

def add_objects(objs, layer):
    """ 여러 오브젝트를 특정 레이어에 추가 """
    while len(objects) <= layer:
        objects.append([])
    objects[layer] += objs

def remove_object(obj):
    """ 특정 오브젝트를 제거 """
    for layer in objects:
        if obj in layer:
            layer.remove(obj)
            del obj  # 객체 삭제
            return

def clear():
    """ 모든 오브젝트를 제거 """
    global objects, collision_pairs
    for layer in objects:
        for obj in layer:
            del obj
    objects.clear()
    collision_pairs.clear()

def update():
    """ 모든 오브젝트 업데이트 """
    for layer in objects:
        for obj in layer:
            obj.update()

def render():
    """ 모든 오브젝트 렌더링 """
    for layer in objects:
        for obj in layer:
            obj.draw()

def add_collision_pair(group, a, b):
    """ 충돌 쌍을 추가합니다 """
    collision_pairs.append((group, a, b))

def handle_collisions():
    """ 모든 충돌 쌍을 처리합니다 """
    for group, a, b in collision_pairs:
        if a is None or b is None:
            continue
        if collide(a, b):
            print(f'COLLISION: {group}')

def collide(a, b):
    """ 간단한 충돌 검사 (사각형 충돌 예시) """
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True
