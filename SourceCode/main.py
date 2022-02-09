from process import r_file, loop_playing, create_game, menu_start, menu_load, close
import os


def main():
    # Create game
    screen = create_game()
    select_start = menu_start(screen)
    if select_start == 0:
        if os.path.exists('../Data/save/save.txt'):
            select_load = menu_load(screen)
            if select_load == 0:
                load_inf = r_file()
                loop_playing(screen, load_inf)
            elif select_load == 1:
                os.remove('../Data/save/save.txt')
                loop_playing(screen)
        else:
            loop_playing(screen)
    elif select_start == 1:
        close()


if __name__ == "__main__":
    main()
