import random
from sys import exit
from var import *
from os import remove


def create_game(name):
    pygame.init()
    screen = pygame.display.set_mode((1366, 768))
    pygame.display.set_caption(name)
    pygame.display.set_icon(pygame.image.load('../Data/image/chicken.png'))
    load_music(all_music()['bg'], 0.2).play(-1)
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


def show_score_hp(screen, score, hp):
    temp = text(f"x{score}", 50, 'Yellow')
    screen.blit(temp, (50, 0))
    temp = text(f"x{hp}", 50, 'Brown')
    screen.blit(temp, (50, 60))


def screen_playing(screen, obj, pl_inf, ck_inf, egg_inf, ls_inf, score_inf, score, hp, time):
    for i, j in obj:
        screen.blit(i, j)
    for i in ls_inf['pos']:
        screen.blit(ls_inf['img'], i)
    for i in ck_inf['pos']:
        screen.blit(ck_inf['img'], i)
    for i in egg_inf['pos']:
        screen.blit(egg_inf['img'], i)
    for i in score_inf['pos']:
        screen.blit(score_inf['img'], i)
    show_score_hp(screen, score, hp)
    screen.blit(text(f"Time remaining: {time}", 30, 'Red'), (1100, 700))
    screen.blit(pl_inf['img'], pl_inf['pos'][0])
    pygame.display.update()


def add_pos_menu(obj_menu):
    new_arr = [[obj_menu[0], (500, 100)]]
    pos_y = 350
    for i in range(1, len(obj_menu)):
        new_arr.append([obj_menu[i], (600, pos_y)])
        pos_y += 100
    return new_arr


def create_menu(screen, menu):
    obj = add_pos_menu(menu)
    bg = get_img('bg')
    signal = text('>>>', 50, 'White')
    pos_sgn = (obj[1][1][0] - 80, obj[1][1][1])
    fps = pygame.time.Clock()
    select = 1
    while True:
        fps.tick(15)
        screen.blit(bg, (0, 0))
        screen.blit(signal, pos_sgn)
        for i, j in obj:
            screen.blit(i, j)
        pygame.display.update()

        for event in pygame.event.get():
            # Close app
            if event.type == pygame.QUIT:
                close()
        # Key
        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN] and select < len(menu) - 1:
            select += 1
            pos_sgn = change_pos(pos_sgn, (0, 100))
        elif key[pygame.K_UP] and select > 1:
            select -= 1
            pos_sgn = change_pos(pos_sgn, (0, -100))
        elif key[pygame.K_RETURN]:
            return select


def create_chicken(level, number_ck, ck_inf):
    distance = 80
    x = 100
    y = 0
    direct = False
    if level < 4:
        ck_inf['pos'].append((x, y))
        for i in range(1, number_ck):
            if i % 15 == 0:
                x = 100
                y += 100
            else:
                x += distance
            ck_inf['pos'].append((x, y))
        return
    else:
        ck_row = 10
        if level == 5:
            ck_row = 15
        ck_inf['pos'].append((x, y))
        ck_inf['direct'].append(direct)
        for i in range(1, number_ck):
            if i % ck_row == 0:
                if direct:
                    x = 100
                    direct = False
                else:
                    x = 500
                    direct = True
                y += 100
            else:
                x += distance
            ck_inf['pos'].append((x, y))
            ck_inf['direct'].append(direct)


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
    if len(ck_inf['pos']) and level < 4:
        temp = random.randint(0, len(ck_inf['pos']) - 1)
        egg_inf['pos'].append(change_pos(ck_inf['pos'][temp], (10, 50)))
    elif len(ck_inf['pos']) and level >= 4:
        temp = random.randint(0, len(ck_inf['pos']) - 1)
        egg_inf['pos'].append(change_pos(ck_inf['pos'][temp], (10, 50)))
        egg_inf['direct'].append(ck_inf['direct'][temp])


def move(speed, inf):
    for i in range(len(inf['pos'])):
        inf['pos'][i] = change_pos(inf['pos'][i], (0, speed))


def move_ck(inf):
    get_dir = {
        True: -1,
        False: 1,
    }
    for i in range(len(inf['pos'])):
        inf['pos'][i] = change_pos(inf['pos'][i], (get_dir[inf['direct'][i]], 0))
        if inf['pos'][i][0] > 1360:
            inf['pos'][i] = (0, inf['pos'][i][1])
        elif inf['pos'][i][0] < 0:
            inf['pos'][i] = (1300, inf['pos'][i][1])


def move_eggs(inf):
    get_dir = {
        True: -1,
        False: 1,
    }
    for i in range(len(inf['pos'])):
        inf['pos'][i] = change_pos(inf['pos'][i], (get_dir[inf['direct'][i]], 2))


def out_screen(inf, size_screen):
    for i in inf['pos']:
        if i[0] > size_screen[0] or i[0] < 0 or i[1] > size_screen[1] or i[1] < 0:
            inf['pos'].remove(i)


def out_screen_egg(level, inf, size_screen):
    for i in inf['pos']:
        if i[0] > size_screen[0] or i[0] < 0 or i[1] > size_screen[1] or i[1] < 0:
            if level > 3:
                del inf['direct'][inf['pos'].index(i)]
            inf['pos'].remove(i)


def screen_show_mess(screen, string):
    screen.blit(get_img('bg'), (0, 0))
    screen.blit(text(string, 100, 'Red'), (500, 200))
    pygame.display.update()


def loop_playing(screen, load=None):
    if load is None:
        load = [1, 1, 0, 5]
    lv_game, lv_gun, score, hp = load[0], load[1], load[2], load[3]
    if lv_game > 1:
        w_file(lv_game, lv_gun, score, hp)

    shoot_time = 0
    num_ck = 1
    num_create_ck = 2
    max_time = 3
    req_plus_hp = 4
    min_req_score = 5
    game = game_level()

    ray_gun = 1
    speed_gun = 2
    req_score_gun = 3
    gun = gun_level()

    screen_show_mess(screen, f"LEVEL {lv_game}")
    pygame.time.delay(3000)

    fps = pygame.time.Clock()
    Max = pygame.display.get_window_size()
    music = all_music()

    pl_inf = player_inf()
    ck_inf = chicken_inf()
    ls_inf = laser_inf()
    egg_inf = eg_inf()
    score_inf = sc_inf()

    size_player = pl_inf['img'].get_size()
    laser_sound = load_music(music['shoot'], 0.05)
    boom_sound = load_music(music['explode_ck'], 0.05)
    collision_sound = load_music(music['collision'], 0.05)

    create_chicken(lv_game, game[lv_game][num_ck], ck_inf)
    game[lv_game][num_create_ck] -= 1

    ls_speed = add_event(0, gun[lv_gun][shoot_time])
    egg_speed = add_event(1, game[lv_game][shoot_time])
    countdown = add_event(2, 1000)

    count = game[lv_game][max_time]
    obj = obj_default_playing()
    plus_hp = False

    while True:
        fps.tick(60)
        screen_playing(screen, obj, pl_inf, ck_inf, egg_inf, ls_inf, score_inf, score, hp, count)
        # Handle event
        for event in pygame.event.get():
            # Close app
            if event.type == pygame.QUIT:
                close()
            # Create laser
            elif event.type == ls_speed:
                create_laser(gun[lv_gun][ray_gun], ls_inf, pl_inf, laser_sound)
            # Create egg
            elif event.type == egg_speed:
                create_egg(lv_game, egg_inf, ck_inf)
            elif event.type == countdown:
                count -= 1

        if game[lv_game][num_create_ck] > 0 and (len(ck_inf['pos']) == 0 and len(score_inf['pos']) == 0):
            create_chicken(lv_game, game[lv_game][num_ck], ck_inf)
            game[lv_game][num_create_ck] -= 1

        if score % game[lv_game][req_plus_hp] == 0 and score != 0 and plus_hp is False:
            hp += 1
            plus_hp = True

        if (len(ck_inf['pos']) == 0 and len(score_inf['pos']) == 0) or (
                count == 0 and score >= game[lv_game][min_req_score]):
            lv_game += 1
            w_file(lv_game, lv_gun, score, hp)
            load = [lv_game, lv_gun, score, hp]
            break
        elif count == 0 or hp == 0:
            screen_show_mess(screen, 'YOU LOSE')
            pygame.time.delay(3000)
            if lv_game != 1:
                remove('../Data/save/save.txt')
            return

        # Upgrade Gun
        if score >= gun[lv_gun][req_score_gun] and lv_gun < len(gun):
            lv_gun += 1
            pygame.time.set_timer(ls_speed, gun[lv_gun][shoot_time])

        # Delete out screen
        out_screen(ls_inf, Max)
        out_screen(score_inf, Max)
        out_screen_egg(lv_game, egg_inf, Max)

        # Move
        if lv_game > 3:
            move_ck(ck_inf)
            move_eggs(egg_inf)
        else:
            move(2, egg_inf)
        move(- gun[lv_gun][speed_gun], ls_inf)
        move(1, score_inf)

        # Delete chicken
        check = collision(ls_inf, ck_inf)
        if check is not None:
            boom_sound.play()
            screen.blit(ck_inf['img_explode'], ck_inf['pos'][check[1]])
            pygame.display.update()
            score_inf['pos'].append(ck_inf['pos'][check[1]])
            ls_inf['pos'].pop(check[0])
            ck_inf['pos'].pop(check[1])
            if lv_game > 3:
                ck_inf['direct'].pop(check[1])

        # Delete Egg
        check = collision(egg_inf, pl_inf)
        if check is not None:
            collision_sound.play()
            screen.blit(pl_inf['img_explode'], pl_inf['pos'][check[1]])
            pygame.display.update()
            pygame.time.delay(20)
            egg_inf['pos'].pop(check[0])
            if lv_game > 3:
                egg_inf['direct'].pop(check[0])
            hp -= 1

        # Plus Score
        check = collision(score_inf, pl_inf)
        if check is not None:
            score_inf['pos'].pop(check[0])
            score += 1
            plus_hp = False

        # Move Player
        key = pygame.key.get_pressed()
        pos_x, pos_y = pl_inf['pos'][0]
        more_max_w = pos_x - pl_inf['move'] > 0
        less_max_w = pos_x + pl_inf['move'] + size_player[0] <= Max[0]
        more_half_h = pos_y - pl_inf['move'] > Max[1] // 2
        less_max_h = pos_y + pl_inf['move'] + size_player[1] <= Max[1]
        if (key[pygame.K_LEFT] or key[pygame.K_a]) and more_max_w:
            pl_inf['pos'][0] = change_pos(pl_inf['pos'][0], (-pl_inf['move'], 0))
        elif (key[pygame.K_RIGHT] or key[pygame.K_d]) and less_max_w:
            pl_inf['pos'][0] = change_pos(pl_inf['pos'][0], (pl_inf['move'], 0))
        elif (key[pygame.K_UP] or key[pygame.K_w]) and more_half_h:
            pl_inf['pos'][0] = change_pos(pl_inf['pos'][0], (0, -pl_inf['move']))
        elif (key[pygame.K_DOWN] or key[pygame.K_s]) and less_max_h:
            pl_inf['pos'][0] = change_pos(pl_inf['pos'][0], (0, pl_inf['move']))
        elif key[pygame.K_ESCAPE]:
            choose = create_menu(screen, menu_pause())
            if choose == 2:
                break
    if load[0] < len(game):
        loop_playing(screen, load)
    else:
        screen_show_mess(screen, 'YOU WIN')
    return
