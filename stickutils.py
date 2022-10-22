import pygame
import uuid


class GameEntity(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy, sprite_path):
        pygame.sprite.Sprite.__init__(self)
        self.id = uuid.uuid4()
        self.vx = vx
        self.vy = vy
        self.sprite = pygame.image.load(sprite_path)
        self.rect = self.sprite.get_rect()
        self.collision_region = self.rect.copy()
        self.collision_region.width = self.rect.width * 2
        self.collision_region.height = self.rect.height * 2
        self.rect.x = x
        self.rect.y = y
        self.jump_speed = 5
        self.in_air = False
        self.h_collision = False
        self.v_collision = False
        self.gy = 0.3
        self.gx = 0
        self.angle = 0
        self.can_collide = True

    def handle_collisions(self, entities: [], collision_tolerance = 0.3):
        filtered_entities = filter(lambda e: self.collision_region.colliderect(e.rect), entities)
        for entity in filtered_entities:
            if entity.can_collide and self.rect.colliderect(entity.rect):

                # horizontal collision
                if self.rect.x + self.rect.width > entity.rect.x:
                    dx = self.rect.x + self.rect.width - entity.rect.x
                    force = -collision_tolerance * dx
                    self.vx += force

                if self.rect.x < entity.rect.x + entity.rect.width:
                    dx = entity.rect.x + entity.rect.width - self.rect.x
                    force = -collision_tolerance * dx
                    self.vx += force

                # vertical collision
                if self.rect.y + self.rect.height < entity.rect.y:
                    dy = entity.rect.y - (self.rect.y + self.rect.height)
                    force = -collision_tolerance * dy
                    self.vy += force

                if self.rect.y < entity.rect.y:
                    dy = self.rect.y - entity.rect.y
                    force = -collision_tolerance * dy
                    self.vy += force






    def update(self):
        if not self.v_collision:
            self.vy += self.gy
        else:
            self.vy = 0

        self.rect.x += self.vx
        self.rect.y += self.vy
        self.collision_region.x = self.rect.x
        self.collision_region.y = self.rect.y
