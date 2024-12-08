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
    if isinstance(a, list) and isinstance(b, list):
        for obj_a in a:
            for obj_b in b:
                collision_pairs.append((group, obj_a, obj_b))
    elif isinstance(a, list):
        for obj_a in a:
            collision_pairs.append((group, obj_a, b))
    elif isinstance(b, list):
        for obj_b in b:
            collision_pairs.append((group, a, obj_b))
    else:
        collision_pairs.append((group, a, b))

def handle_collisions():
    for group, a, b in collision_pairs:
        # 객체 검증
        if a is None or b is None:
            print(f"Invalid collision pair: {a}, {b}")
            continue

        # Bounding Box 확인
        if not hasattr(a, 'get_bb') or not hasattr(b, 'get_bb'):
            print(f"Non-collidable objects in pair: {a}, {b}")
            continue

        # 충돌 감지
        if collide(a, b):
            print(f"COLLISION: {group} between {a} and {b}")

            # 그룹별 충돌 처리
            if group == 'character:platform':
                a.on_collision_with_platform(b)
            elif group == 'enemy:bullet':
                a.handle_collision(b)
                b.handle_collision(a)
            elif group == 'character:enemy':
                a.on_collision_with_enemy(b)
                b.handle_collision(a)
            else:
                print(f"Unhandled collision group: {group}")



def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    print(f"Checking collision:")
    print(f" - Object A BB: {left_a, bottom_a, right_a, top_a}")
    print(f" - Object B BB: {left_b, bottom_b, right_b, top_b}")

    if left_a > right_b or right_a < left_b or top_a < bottom_b or bottom_a > top_b:
        print("No collision detected.")
        return False

    print("Collision detected!")
    return True

