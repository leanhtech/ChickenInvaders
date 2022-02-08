import pygame
import random
from var import link_music, player_chicken_laser_egg_score_inf, obj_playing
from process import screen_playing, create_game, load_music, add_event, change_pos, collision
from sys import exit


def set_ck(level, number_ck, ck_inf):
    distance = 60
    pos_x = 100
    pos_y = 0
    if level == 1:
        for i in range(number_ck):
            if i % 5 == 0 and i != 0:
                pos_x += 600
            if i % 10 == 0 and i != 0:
                pos_x = 100
                pos_y += distance
            ck_inf['pos'].append((pos_x, pos_y))
            pos_x += distance

        return


def screen_start(screen, obj_game, pos, pos_sl):
    screen.blit(obj_game['bg'], pos['bg'])
    screen.blit(obj_game['select_sign'], pos_sl)
    screen.blit(obj_game['main_menu'], (500, 100))
    screen.blit(obj_game['text_play'], (600, 350))
    screen.blit(obj_game['text_exit'], (640, 450))
    pygame.display.update()


def main():
    # Create game
    screen = create_game()
    refresh = pygame.time.Clock()
    Max = pygame.display.get_window_size()

    music = link_music()

    pl_inf, ck_inf, ls_inf, egg_inf, score_inf = player_chicken_laser_egg_score_inf()

    lv_inf = [[], [10, 40, 0], [20, 30, 20]]  # [[shoot_time, number_ck, point_req],...]
    shoot_time = 0
    number_ck = 1
    point_req = 2

    # Load music
    laser_sound = load_music(music['shoot'], 0.1)
    boom_sound = load_music(music['explode_ck'], 0.3)
    bg_sound = load_music(music['bg'], 0.3)
    collision_sound = load_music(music['collision'], 0.3)
    bg_sound.play(-1)

    # Set level
    level = 1
    '''
    load_lv(level, lv_inf, lv_ele)
    '''
    # Set chicken
    set_ck(level, lv_inf[level][number_ck], ck_inf)

    ls_speed = add_event(0, 500)
    egg_speed = add_event(1, 1500)

    pos_sl = (500, 350)
    '''
    while True:
        screen.blit(bg_show, pos['bg'])
        screen.blit(select_sign, pos_sl)
        screen.blit(menu, (500, 100))
        screen.blit(play_game, (600, 350))
        screen.blit(exit_game, (640, 450))
        pygame.display.update()
        # Handle event
        for event in pygame.event.get():
            # Close app
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Key
        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN] and pos_sl[1] < 450:
            pos_sl = change_pos(pos_sl, (0, 100))
        elif key[pygame.K_UP] and pos_sl[1] > 350:
            pos_sl = change_pos(pos_sl, (0, -100))
        elif key[pygame.K_RETURN]:
            pos_sl = (500, 350)
            while True:
                print('da vo')
                screen.blit(bg_show, pos['bg'])
                screen.blit(select_sign, pos_sl)
                screen.blit(cont_game, (600, 350))
                screen.blit(new_game, (640, 450))
                pygame.display.update()
                key = pygame.key.get_pressed()
                if key[pygame.K_DOWN] and pos_sl[1] < 450:
                    pos_sl = change_pos(pos_sl, (0, 100))
                elif key[pygame.K_UP] and pos_sl[1] > 350:
                    pos_sl = change_pos(pos_sl, (0, -100))
                refresh.tick(10)

        refresh.tick(10)
    '''
    basic = obj_playing()
    while True:
        refresh.tick(60)
        screen_playing(screen, basic, pl_inf, ck_inf, egg_inf, ls_inf, score_inf)
        # Handle event
        for event in pygame.event.get():
            # Close app
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Create laser
            if event.type == ls_speed:
                ls_inf['pos'].append(change_pos(pl_inf['pos'][0], (20, -50)))  # (20, -50)
                laser_sound.play()
            # Create egg
            if event.type == egg_speed:
                if len(ck_inf['pos']):
                    temp = random.randint(0, len(ck_inf['pos']) - 1)
                    egg_inf['pos'].append(change_pos(ck_inf['pos'][temp], (10, 50)))

        # Delete laser
        for i in ls_inf['pos']:
            if i[1] < 0:
                ls_inf['pos'].remove(i)
                break

        # Move laser
        for i in range(len(ls_inf['pos'])):
            ls_inf['pos'][i] = change_pos(ls_inf['pos'][i], (0, -10))

        # Move Score
        for i in range(len(score_inf['pos'])):
            score_inf['pos'][i] = change_pos(score_inf['pos'][i], (0, 5))

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
        for i in egg_inf['pos']:
            if i[1] > Max[1]:
                egg_inf['pos'].remove(i)
                break
        check = collision(egg_inf, pl_inf)
        if check is not None:
            collision_sound.play()
            screen.blit(pl_inf['img_explode'], pl_inf['pos'][0])
            pygame.display.update()

            egg_inf['pos'].pop(check[0])
            pl_inf['hp'] -= 1

        # Plus Score
        check = collision(score_inf, pl_inf)
        if check is not None:
            score_inf['pos'].pop(check[0])
            pl_inf['point'] += 1

        # Move Egg
        for i in range(len(egg_inf['pos'])):
            egg_inf['pos'][i] = change_pos(egg_inf['pos'][i], (0, 2))

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


if __name__ == "__main__":
    main()
