import pygame.display

import stickutils
pygame.init()

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
    clock = pygame.time.Clock()
    dt = 0

    for i in range(5):
        block = stickutils.Block(WIDTH / 2 + i * 32, HEIGHT / 2 + 128)
        sprites.add(block)
        entities.append(block)
    block = stickutils.Block(WIDTH / 2 + 3 * 32, HEIGHT / 2 + 128 - 32)
    sprites.add(block)
    entities.append(block)

    block = stickutils.Block(WIDTH / 2 + 3 * 32, HEIGHT / 2 + 128 - 64)
    sprites.add(block)
    entities.append(block)


    block = stickutils.Block(WIDTH / 2 + 2 * 32, HEIGHT / 2 + 128 - 64 * 2)
    sprites.add(block)
    entities.append(block)


    block = stickutils.Block(WIDTH / 2 + 1 * 32, HEIGHT / 2 + 128 - 64 * 2)
    sprites.add(block)
    entities.append(block)

    # frame = stickutils.Frame(gui_sprites, 32, 32, 128, 128, stickutils.Color(0, 255, 0))
    nametag = stickutils.TextLabel(0, 0, player.name)

    while True:
        # player.handle_collisions(sprites, dt, 0)
        # player.handle_collisions(sprites, dt, 1)
        sprites.update(pygame.event.get(), dt)
        window.fill((0, 0, 0))
        sprites.draw(window)
        nametag.draw(window)
        nametag.update(player.rect.center[0] - nametag.rect.width / 2, player.rect.center[1] - player.rect.height - nametag.rect.height)
        gui_sprites.draw(window)
        pygame.display.update()
        dt = clock.tick(60)


if __name__ == "__main__":
    main()
