import pygame.display

import stickutils

pygame.init()
pygame.mixer.init()


def main():
    world = stickutils.World("Sprites/bg_night_sky.png")
    world.game_loop()


if __name__ == "__main__":
    main()
