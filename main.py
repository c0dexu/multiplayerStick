import pygame.display

import stickutils

pygame.init()
pygame.mixer.init()

def call_me(*argv):
    for arg in argv:
        print(arg)

def main():
    WIDTH = 1024
    HEIGHT = 512

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Stick")

    entities = []
    sprites = pygame.sprite.Group()
    player = stickutils.Player(WIDTH / 2, HEIGHT / 2, all_entities=entities)
    gui_sprites = pygame.sprite.Group()
    sprites.add(player)
    ball = stickutils.Ball(0, 0, all_entities=entities)
    entities.append(ball)
    sprites.add(ball)
    clock = pygame.time.Clock()
    dt = 0

    # frame = stickutils.Frame(gui_sprites, 32, 32, 128, 128, stickutils.Color(0, 255, 0))
    stickutils.generate_baseplate(0, 0, 1024, sprites, entities)

    frame_test = stickutils.Frame(window, 0, 0, 128, 128, (0, 255, 0))
    input_test = stickutils.TextInput(window, frame_test.width // 2, frame_test.height // 2, 128, 32, parent=frame_test)
    input_test.return_callback = call_me

    while True:
        events = pygame.event.get()
        for event in events:
            input_test.listen(event)

        sprites.update(pygame.event.get(), dt)
        window.fill((0, 0, 0))
        sprites.draw(window)
        frame_test.move_to_pixels(WIDTH / 4, 0)
        frame_test.draw()
        gui_sprites.draw(window)
        input_test.draw()
        pygame.display.update()
        dt = clock.tick(60)


if __name__ == "__main__":
    main()
