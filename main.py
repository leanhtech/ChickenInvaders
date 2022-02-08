import pygame
import random
from var import link_music, player_chicken_laser_egg_score_inf, obj_playing
from process import set_chicken, screen_playing, create_game, load_music, add_event, change_pos, collision, menu_start, menu_load
from sys import exit


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
    set_chicken(1, 30, ck_inf)

    ls_speed = add_event(0, 800)
    egg_speed = add_event(1, 1500)

    basic = obj_playing()
    select = menu_start(screen)
    if select == 0:
        select = menu_load(screen)
        if select == 1:
            pass
    elif select == 1:
        pygame.quit()
        exit()
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
                ls_inf['pos'].append(change_pos(pl_inf['pos'][0], (20, -20)))  # (20, -50)
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
            score_inf['pos'][i] = change_pos(score_inf['pos'][i], (0, 1))

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
