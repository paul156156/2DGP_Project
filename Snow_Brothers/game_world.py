objects = []  # 게임 오브젝트를 관리할 리스트 (2D 리스트로 레이어별 관리)
collision_pairs = []  # 충돌 처리용 쌍 리스트

def add_object(obj, layer):
    while len(objects) <= layer:
        objects.append([])
    objects[layer].append(obj)

def add_objects(objs, layer):
    while len(objects) <= layer:
        objects.append([])
    objects[layer] += objs

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
        if collide(a, b):
            print(f'COLLISION: {group}')

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True
