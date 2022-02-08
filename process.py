import pygame
from sys import exit
from var import load_obj, text


def create_game():
    pygame.init()
    screen = pygame.display.set_mode((1366, 768))
    pygame.display.set_caption('ChickenInvader')
    ic_game = pygame.image.load('Data/image/conga.png')
    pygame.display.set_icon(ic_game)
    return screen


def show_point_hp(screen, point, hp):
    temp = text(50, f"x{point}", 'Yellow')
    screen.blit(temp, (50, 0))
    temp = text(50, f"x{hp}", 'Brown')
    screen.blit(temp, (50, 60))


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


def screen_playing(screen, basic, pl_inf, ck_inf, egg_inf, ls_inf, score_inf):
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
    show_point_hp(screen, pl_inf['point'], pl_inf['hp'])
    pygame.display.update()


def create_menu(screen, obj_sl, name):
    bg = load_obj('Data/image/hinhnen.png', (1366, 768))
    signal = text(50, '>>>', 'White')
    count = len(obj_sl) - 1
    pos = (obj_sl[0][1][0] - 70, obj_sl[0][1][1])
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
                pygame.quit()
                exit()
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
        [text(50, 'Continue Game', 'Yellow'), (600, 350)],
        [text(50, 'New Game', 'Yellow'), (640, 450)]
    ]
    name = text(100, 'Load or New', 'Red')
    return create_menu(screen, select, name)


def set_chicken(level, number_ck, ck_inf):
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
