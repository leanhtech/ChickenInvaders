import pygame
import random
from sys import exit
from var import load_obj, text, obj_playing, link_music, player_chicken_laser_egg_score_inf


def create_game():
    pygame.init()
    screen = pygame.display.set_mode((1366, 768))
    pygame.display.set_caption('ChickenInvader')
    ic_game = pygame.image.load('../Data/image/conga.png')
    pygame.display.set_icon(ic_game)
    return screen


def w_file(lv_game, lv_gun, score, hp):
    s = [str(lv_game) + '\n', str(lv_gun) + '\n', str(score) + '\n', str(hp) + '\n']
    with open('../Data/save/save.txt', 'w') as file:
        file.writelines(s)


def r_file():
    x = []
    with open('../Data/save/save.txt') as file:
        for line in file:
            x.append(int(line.strip()))
    return x


def close():
    pygame.quit()
    exit()


def show_score_hp(screen, score, hp):
    temp = text(50, f"x{score}", 'Yellow')
    screen.blit(temp, (50, 0))
    temp = text(50, f"x{hp}", 'Brown')
    screen.blit(temp, (50, 60))
    pygame.display.update()


def load_music(path, vol):
    sound = pygame.mixer.Sound(path)
    sound.set_volume(vol)
    return sound


def collision(inf_1, inf_2):
    for i in range(len(inf_1['pos'])):
        inf_1['rect'].topleft = inf_1['pos'][i]
        for j in range(len(inf_2['pos'])):
            inf_2['rect'].topleft = inf_2['pos'][j]
            if (inf_1['rect']).colliderect(inf_2['rect']):
                return [i, j]
    return None


def change_pos(tuple_1, tuple_2):
    return tuple(a + b for a, b in zip(tuple_1, tuple_2))


def add_event(id_event, timer):
    x = pygame.USEREVENT + id_event
    pygame.time.set_timer(x, timer)
    return x


def screen_playing(screen, basic, pl_inf, ck_inf, egg_inf, ls_inf, score_inf, score, hp):
    for i, j in basic:
        screen.blit(i, j)
    for i in ls_inf['pos']:
        screen.blit(ls_inf['img'], i)
    for i in ck_inf['pos']:
        screen.blit(ck_inf['img'], i)
    for i in egg_inf['pos']:
        screen.blit(egg_inf['img'], i)
    for i in score_inf['pos']:
        screen.blit(score_inf['img'], i)
    screen.blit(pl_inf['img'], pl_inf['pos'][0])

    show_score_hp(screen, score, hp)
    pygame.display.update()


def create_menu(screen, obj_sl, name):
    bg = load_obj('../Data/image/hinhnen.png', (1366, 768))
    signal = text(50, '>>>', 'White', False)
    count = len(obj_sl) - 1
    pos = (obj_sl[0][1][0] - 80, obj_sl[0][1][1])
    fps = pygame.time.Clock()
    select = 0
    while True:
        fps.tick(15)
        screen.blit(bg, (0, 0))
        screen.blit(signal, pos)
        for i, j in obj_sl:
            screen.blit(i, j)
        screen.blit(name, (500, 100))
        pygame.display.update()

        for event in pygame.event.get():
            # Close app
            if event.type == pygame.QUIT:
                close()
        # Key
        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN] and select < count:
            select += 1
            pos = change_pos(pos, (0, 100))
        elif key[pygame.K_UP] and select > 0:
            select -= 1
            pos = change_pos(pos, (0, -100))
        elif key[pygame.K_RETURN]:
            return select


def menu_start(screen):
    select = [
        [text(50, 'Play Game', 'Yellow'), (600, 350)],
        [text(50, 'Exit', 'Yellow'), (640, 450)]
    ]
    name = text(100, 'Main Menu', 'Red')
    return create_menu(screen, select, name)


def menu_load(screen):
    select = [
        [text(50, 'Previous Level', 'Yellow'), (600, 350)],
        [text(50, 'New Game', 'Yellow'), (640, 450)]
    ]
    name = text(100, 'Load or New', 'Red')
    return create_menu(screen, select, name)


def menu_pause(screen):
    select = [
        [text(50, 'Resume', 'Yellow'), (600, 350)],
        [text(50, 'Reload', 'Yellow'), (600, 450)]
    ]
    name = text(100, 'Pause Game', 'Red')
    return create_menu(screen, select, name)


def create_chicken(level, number_ck, ck_inf):
    distance = 80
    x = 100
    y = 0
    ck_inf['pos'].append((x, y))
    if level == 1:
        for i in range(1, number_ck):
            if i % 15 == 0:
                x = 100
                y += 100
            else:
                x += distance
            ck_inf['pos'].append((x, y))
        return


def create_laser(num_ray, ls_inf, pl_inf, sound):
    if num_ray == 1:
        ls_inf['pos'].append(change_pos(pl_inf['pos'][0], (20, -20)))
        sound.play()
    elif num_ray == 2:
        ls_inf['pos'].append(change_pos(pl_inf['pos'][0], (0, -20)))
        ls_inf['pos'].append(change_pos(pl_inf['pos'][0], (40, -20)))
        sound.play()
    elif num_ray == 3:
        ls_inf['pos'].append(change_pos(pl_inf['pos'][0], (-20, -20)))
        ls_inf['pos'].append(change_pos(pl_inf['pos'][0], (60, -20)))
        ls_inf['pos'].append(change_pos(pl_inf['pos'][0], (20, -20)))
        sound.play()


def create_egg(level, egg_inf, ck_inf):
    if len(ck_inf['pos']) and level == 1:
        temp = random.randint(0, len(ck_inf['pos']) - 1)
        egg_inf['pos'].append(change_pos(ck_inf['pos'][temp], (10, 50)))


def move(speed, inf):
    for i in range(len(inf['pos'])):
        inf['pos'][i] = change_pos(inf['pos'][i], (0, speed))


def out_screen(inf, size_screen):
    for i in inf['pos']:
        if i[0] > size_screen[0] or i[0] < 0 or i[1] > size_screen[1] or i[1] < 0:
            inf['pos'].remove(i)


def loop_playing(screen, load=None):
    if load is None:
        load = [1, 1, 0, 5]
    lv_game, lv_gun, score, hp = load[0], load[1], load[2], load[3]
    if lv_game != 1:
        w_file(lv_game, lv_gun, score, hp)
    shoot_time = 0
    num_ck = 1
    req_plus_hp = 2
    max_time = 3
    min_req_score = 4
    game = [
        [],
        [1500, 30, 10, 60000, 25]
    ]

    ray_gun = 1
    speed_gun = 2
    gun = [
        [],
        [1000, 1, 10]
    ]
    fps = pygame.time.Clock()
    Max = pygame.display.get_window_size()
    music = link_music()

    pl_inf, ck_inf, ls_inf, egg_inf, score_inf = player_chicken_laser_egg_score_inf()

    laser_sound = load_music(music['shoot'], 0.2)
    boom_sound = load_music(music['explode_ck'], 0.3)
    collision_sound = load_music(music['collision'], 0.3)
    bg_sound = load_music(music['bg'], 0.3)
    bg_sound.play(-1)

    create_chicken(lv_game, game[lv_game][num_ck], ck_inf)

    ls_speed = add_event(0, gun[lv_gun][shoot_time])
    egg_speed = add_event(1, game[lv_game][shoot_time])
    countdown = add_event(2, game[lv_game][max_time])

    count = game[lv_game][max_time] / 1000
    basic = obj_playing()
    while True:
        fps.tick(60)
        screen_playing(screen, basic, pl_inf, ck_inf, egg_inf, ls_inf, score_inf, score, hp)
        # Handle event
        for event in pygame.event.get():
            # Close app
            if event.type == pygame.QUIT:
                close()
            # Create laser
            if event.type == ls_speed:
                create_laser(gun[lv_gun][ray_gun], ls_inf, pl_inf, laser_sound)
            # Create egg
            if event.type == egg_speed:
                create_egg(lv_game, egg_inf, ck_inf)

        # Delete out screen
        out_screen(ls_inf, Max)
        out_screen(egg_inf, Max)
        out_screen(score_inf, Max)

        # Move
        move(- gun[lv_gun][speed_gun], ls_inf)
        move(1, score_inf)
        move(2, egg_inf)

        # Delete chicken
        check = collision(ls_inf, ck_inf)
        if check is not None:
            boom_sound.play()
            screen.blit(ck_inf['img_explode'], ck_inf['pos'][check[1]])
            pygame.display.update()
            score_inf['pos'].append(ck_inf['pos'][check[1]])
            ls_inf['pos'].pop(check[0])
            ck_inf['pos'].pop(check[1])

        # Delete Egg
        check = collision(egg_inf, pl_inf)
        if check is not None:
            collision_sound.play()
            screen.blit(pl_inf['img_explode'], pl_inf['pos'][check[1]])
            pygame.display.update()
            pygame.time.delay(20)
            egg_inf['pos'].pop(check[0])
            hp -= 1

        # Plus Score
        check = collision(score_inf, pl_inf)
        if check is not None:
            score_inf['pos'].pop(check[0])
            score += 1

        # Move Player
        key = pygame.key.get_pressed()
        pos_x, pos_y = pl_inf['pos'][0]
        more_max_w = pos_x - pl_inf['move'] > 0
        less_max_w = pos_x + pl_inf['move'] + pl_inf['size'][0] <= Max[0]
        more_half_h = pos_y - pl_inf['move'] > Max[1] // 2
        less_max_h = pos_y + pl_inf['move'] + pl_inf['size'][1] <= Max[1]
        if (key[pygame.K_LEFT] or key[pygame.K_a]) and more_max_w:
            pl_inf['pos'][0] = change_pos(pl_inf['pos'][0], (-pl_inf['move'], 0))
        elif (key[pygame.K_RIGHT] or key[pygame.K_d]) and less_max_w:
            pl_inf['pos'][0] = change_pos(pl_inf['pos'][0], (pl_inf['move'], 0))
        elif (key[pygame.K_UP] or key[pygame.K_w]) and more_half_h:
            pl_inf['pos'][0] = change_pos(pl_inf['pos'][0], (0, -pl_inf['move']))
        elif (key[pygame.K_DOWN] or key[pygame.K_s]) and less_max_h:
            pl_inf['pos'][0] = change_pos(pl_inf['pos'][0], (0, pl_inf['move']))
        elif key[pygame.K_ESCAPE]:
            choose = menu_pause(screen)
            if choose == 1:
                break
    loop_playing(screen, load)
