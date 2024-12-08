objects = []
collision_pairs = []

def add_object(obj, layer):
    while len(objects) <= layer:
        objects.append([])
    objects[layer].append(obj)

def add_objects(objs, layer):
    while len(objects) <= layer:
        objects.append([])
    objects[layer] += objs

def get_objects_in_layer(layer):
    """지정된 레이어의 객체 리스트 반환"""
    if layer < len(objects):
        return objects[layer]
    return []  # 해당 레이어가 없으면 빈 리스트 반환

def remove_object(obj):
    for layer in objects:
        if obj in layer:
            layer.remove(obj)
            del obj  # 객체 삭제
            return

def clear():
    global objects, collision_pairs
    for layer in objects:
        for obj in layer:
            del obj
    objects.clear()
    collision_pairs.clear()

def update():
    for layer in objects:
        for obj in layer:
            obj.update()

def render():
    for layer in objects:
        for obj in layer:
            obj.draw()

def add_collision_pair(group, a, b):
    collision_pairs.append((group, a, b))

def handle_collisions():
    for group, a, b in collision_pairs:
        if a is None or b is None:
            continue
        if collide(a, b):  # 충돌 여부 확인
            if group == 'character:platform':
                a.on_collision_with_platform(b)  # 충돌 처리 메서드 호출
            print(f'COLLISION: {group}')

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True
