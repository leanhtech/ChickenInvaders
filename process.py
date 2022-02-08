import pygame


def create_game():
    pygame.init()
    screen = pygame.display.set_mode((1366, 768))
    pygame.display.set_caption('ChickenInvader')
    ic_game = pygame.image.load('Data/image/conga.png')
    pygame.display.set_icon(ic_game)
    return screen


def load_obj(path, size_obj):
    x = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(x, size_obj)


def show_point_hp(screen, point, hp):
    temp = text(50, f"x{point}", 'Yellow')
    screen.blit(temp, (50, 0))
    temp = text(50, f"x{hp}", 'Brown')
    screen.blit(temp, (50, 60))


def text(size_text, string, color):
    x = pygame.font.Font('Data/font/VT323-Regular.ttf', size_text)
    return x.render(string, False, color).convert_alpha()


def load_music(path, vol):
    sound = pygame.mixer.Sound(path)
    sound.set_volume(vol)
    return sound


def to_rect(obj):
    return obj.get_rect()


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
