from process import load_obj, text, to_rect


def link_img():
    dir_img = 'Data/image/'
    return {
        'bg': f'{dir_img}hinhnen.png',
        'score': f'{dir_img}duiga.png',
        'hp': f'{dir_img}tim.png',
        'menu': f'{dir_img}menu.png',
        'esc': f'{dir_img}thoat.png',
        'player': f'{dir_img}phithuyen.png',
        'chicken': f'{dir_img}conga.png',
        'laser_pl_lv1': f'{dir_img}laser_lv1.png',
        'egg': f'{dir_img}egg.png',
        'explode': f'{dir_img}explode.png'
    }


def link_music():
    dir_music = 'Data/Music/'
    return {
        'bg': f'{dir_music}level1.ogg',
        'shoot': f'{dir_music}shoot.wav',
        'explode_ck': f'{dir_music}Chicken.mp3',
        'collision': f'{dir_music}boom.wav'
    }


def size():
    return {
        'bg': (1366, 768),
        'player': (60, 60),
        'chicken': (50, 50),
        'items': (50, 50),
        'laser': (20, 40),
        'egg': (30, 40),
        'font': 50,
    }


def position():
    return {
        'bg': (0, 0),
        'point_ic': (0, 0),
        'point': (50, 0),
        'hp_ic': (0, 60),
        'hp': (50, 60),
        'menu': (1306, 5),
        'main_menu': (500, 100),
        1: (600, 350),
        2: (640, 450)
    }


def obj_basic():
    img = link_img()
    size_ = size()
    return {
        'bg': load_obj(img['bg'], size_['bg']),
        'point_ic': load_obj(img['score'], size_['items']),
        'hp_ic': load_obj(img['hp'], size_['items']),
        'menu_ic': load_obj(img['menu'], size_['items']),
        'close_ic_menu': load_obj(img['esc'], size_['items']),
        'menu': text(100, 'Main Menu', 'Red'),
        'text_play': text(size_['font'], 'Play Game', 'Yellow'),
        'text_exit': text(size_['font'], 'Exit', 'Yellow'),
        'select_sign': text(size_['font'], '>>>', 'White'),
        'text_cont': text(size_['font'], 'Continue Game', 'Yellow'),
        'text_new': text(size_['font'], 'New Game', 'Yellow')
    }


def player_chicken_laser_egg_score_inf():
    img = link_img()
    size_ = size()
    img_pl = load_obj(img['player'], size_['player'])
    img_ck = load_obj(img['chicken'], size_['chicken'])
    img_ls = load_obj(img['laser_pl_lv1'], size_['laser'])
    img_egg = load_obj(img['egg'], size_['egg'])
    explode = load_obj(img['explode'], size_['player'])
    img_score = load_obj(img['score'], size_['egg'])
    return {
               'img': img_pl,
               'img_explode': explode,
               'rect': to_rect(img_pl),
               'pos': [(600, 650)],
               'size': size_['player'],
               'move': 5,
               'point': 0,
               'hp': 5
           }, {
               'img': img_ck,
               'img_explode': explode,
               'rect': to_rect(img_ck),
               'pos': [],  # [(x,y),...]
               'size': size_['chicken']
           }, {
               'img': img_ls,
               'rect': to_rect(img_ls),
               'pos': [],  # [(x,y),...]
               'size': size_['laser']
           }, {
               'img': img_egg,
               'rect': to_rect(img_egg),
               'pos': [],
               'size': size_['egg']
           }, {
                'img': img_score,
                'rect': to_rect(img_score),
                'pos': [],
                'size': size_['egg']
            }


def obj_playing():
    img = link_img()
    size_ = size()
    return [
        [load_obj(img['bg'], size_['bg']), (0, 0)],
        [load_obj(img['score'], size_['items']), (0, 0)],
        [load_obj(img['hp'], size_['items']), (0, 60)],
        [load_obj(img['menu'], size_['items']), (1306, 5)]
    ]
