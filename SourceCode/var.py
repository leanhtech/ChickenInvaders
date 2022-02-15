import pygame


def all_img():
    dir_img = '../Data/image/'
    return {
        'bg': f'{dir_img}background.png',
        'score': f'{dir_img}score.png',
        'hp': f'{dir_img}hp.png',
        'player': f'{dir_img}spaceship.png',
        'chicken': f'{dir_img}chicken.png',
        'laser': f'{dir_img}laser.png',
        'egg': f'{dir_img}egg.png',
        'explode': f'{dir_img}explode.png'
    }


def all_size():
    item_size = (50, 50)
    return {
        'bg': (1366, 768),
        'score_txt': 50,
        'hp_txt': 50,
        'hp': item_size,
        'score': item_size,
        'player': (60, 60),
        'chicken': (50, 50),
        'laser': (20, 40),
        'egg': (30, 40),
        'explode': (60, 60),
        'font': 50,
        'small_font': 25,
        'title': 100
    }


def all_music():
    dir_music = '../Data/music/'
    return {
        'bg': f'{dir_music}level1.ogg',
        'shoot': f'{dir_music}shoot.wav',
        'explode_ck': f'{dir_music}chicken.mp3',
        'collision': f'{dir_music}boom.wav'
    }


def all_position():
    return {
        'bg': (0, 0),
        'score': (0, 0),
        'hp': (0, 60),
        'pause': (1250, 5),
        'main_menu': (500, 100)
    }


def text(string='Unknown', size=50, color='Yellow', underline=False, bold=False, italic=False, smooth=True):
    x = pygame.font.Font('../Data/font/VT323-Regular.ttf', size)
    x.set_underline(underline)
    x.set_bold(bold)
    x.set_italic(italic)
    return x.render(string, smooth, color).convert_alpha()


def get_img(name_img='bg', name_size=None):
    if not name_size:
        name_size = name_img
    img = all_img()
    size = all_size()
    x = pygame.image.load(img[name_img]).convert_alpha()
    return pygame.transform.scale(x, size[name_size])


def menu_start():
    size = all_size()
    return [
        text('MAIN MENU', size['title'], 'Red'),
        text('Play Game', size['font'], 'Yellow', True),
        text('Exit', size['font'], 'Yellow', True)
    ]


def menu_load():
    size = all_size()
    return [
        text('LOAD LEVEL', size['title'], 'Red'),
        text('Previous Level', size['font'], 'Yellow', True),
        text('New Game', size['font'], 'Yellow', True)
    ]


def menu_pause():
    size = all_size()
    return [
        text('PAUSE GAME', size['title'], 'Red'),
        text('Resume', size['font'], 'Yellow', True),
        text('Reload', size['font'], 'Yellow', True)
    ]


def player_inf():
    pl = get_img('player')
    explode = get_img('explode')
    return {
        'img': pl,
        'img_explode': explode,
        'rect': pl.get_rect(),
        'pos': [(600, 650)],
        'move': 5,
    }


def chicken_inf():
    ck = get_img('chicken')
    explode = get_img('explode')
    return {
        'img': ck,
        'img_explode': explode,
        'rect': ck.get_rect(),
        'pos': [],
        'direct': []
    }


def laser_inf():
    ls = get_img('laser')
    return {
        'img': ls,
        'rect': ls.get_rect(),
        'pos': []
    }


def eg_inf():
    egg = get_img('egg')
    return {
        'img': egg,
        'rect': egg.get_rect(),
        'pos': [],
        'direct': []
    }


def sc_inf():
    sc = get_img('score', 'egg')
    return {
        'img': sc,
        'rect': sc.get_rect(),
        'pos': []
    }


def obj_default_playing():
    pos = all_position()
    size = all_size()
    return [
        [get_img('bg'), pos['bg']],
        [get_img('score'), pos['score']],
        [get_img('hp'), pos['hp']],
        [text('Pause(Esc)', size['small_font'], 'Gold'), pos['pause']]
    ]


def game_level():
    return [
        [],
        [1500, 30, 1, 80, 10, 25],
        [1000, 45, 1, 70, 15, 65],
        [800, 60, 1, 70, 15, 125],
        [500, 40, 3, 120, 20, 180],
        [500, 60, 4, 80, 20, 250]
    ]


def gun_level():
    return [
        [],
        [1000, 1, 8, 10],
        [500, 1, 8, 25],
        [1000, 2, 10, 50],
        [800, 2, 10, 80],
        [500, 2, 10, 100],
        [1000, 3, 10, 120],
        [800, 3, 10, 150],
        [500, 3, 10, 200]
    ]
