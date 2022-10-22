import pygame
import uuid


class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy, sprite_path):
        pygame.sprite.Sprite.__init__(self)
        self.id = uuid.uuid4()
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.sprite = pygame.image.load(sprite_path)
        self.rect = self.sprite.get_rect()
        self.jump_speed = 5
        self.in_air = False

