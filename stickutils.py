import pygame
import uuid


def place_meeting(x, y, w, h, rect: pygame.Rect):
    test_rect = pygame.Rect(x, y, w, h)
    return test_rect.colliderect(rect)


## GUI elements ##
class Color:
    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b


class TextLabel:
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.font = pygame.font.Font("freesansbold.ttf", 14)
        self.text = self.font.render(text, True, (255, 255, 255), (0, 0, 0))
        self.rect = self.text.get_rect()

    def draw(self, surface):
        surface.blit(self.text, self.rect)

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y


## Game entities ##
class GameEntity(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy, sprite_path, all_entities):
        pygame.sprite.Sprite.__init__(self)
        self.id = uuid.uuid4()
        self.all_entities = all_entities
        self.vx = vx
        self.vy = vy
        self.image = pygame.image.load(sprite_path)
        self.rect = self.image.get_rect()
        self.collision_region = self.rect.copy()
        self.collision_region.width = self.rect.width * 2
        self.collision_region.height = self.rect.height * 2
        self.rect.x = x
        self.rect.y = y
        self.jump_speed = 5
        self.in_air = False
        self.gy = 0.3
        self.angle = 0
        self.has_gravity = True
        self.can_collide = True
        self.dx = 0
        self.dy = 0

    def handle_collisions(self, entities: [], dt, axis, collision_tolerance=0.3):

        filtered_entities = list(filter(lambda e: e != self and self.collision_region.colliderect(e.rect), entities))
        colliding_entities = []
        for entity in filtered_entities:
            if entity.can_collide and self.rect.colliderect(entity.rect):
                colliding_entities.append(entity)
        for e in entities:
            if e.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height):
                self.dx = 0
                # self.vx = 0

            if e.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height):
                if self.vy < 0:
                    self.dy = e.rect.bottom - self.rect.top
                    self.vy += self.dy
                elif self.vy >= 0:
                    self.dy = e.rect.top - self.rect.bottom
                    self.vy = 0



    def update(self):
        if self.has_gravity:
            self.vy += self.gy

        self.dy += self.vy
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.collision_region.x = self.rect.x
        self.collision_region.y = self.rect.y


class Player(GameEntity):
    def __init__(self, x, y, all_entities,sprite_path="Sprites/stickman.png"):
        GameEntity.__init__(self, x, y, 0, 0, sprite_path, all_entities)
        self.walkspeed = 3
        self.gy = 0.0125
        self.horizontal = 0
        self.vertical = 0
        self.xspawn = self.rect.x
        self.yspawn = self.rect.y
        self.name = "Player_" + str(uuid.uuid4()).split('-')[0]

    def respawn(self):
        self.rect.x = self.xspawn
        self.rect.y = self.yspawn
        self.vx = 0
        self.vy = 0

    def update(self, a, dt):
        self.dx = 0
        self.dy = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.dx = -self.walkspeed

        if key[pygame.K_r]:
            self.respawn()

        if key[pygame.K_d]:
            self.dx = self.walkspeed

        if key[pygame.K_SPACE] and not self.in_air:
            self.vy -= self.jump_speed * 1

        if self.has_gravity:
            self.vy += self.gy * dt

        self.dy += self.vy
        self.handle_collisions(self.all_entities, dt, 1)

        if abs(self.vy) > 1:
            self.in_air = True
        else:
            self.in_air = False
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.collision_region.x = self.rect.x
        self.collision_region.y = self.rect.y


class Block(GameEntity):
    def __init__(self, x, y):
        GameEntity.__init__(self, x, y, 0, 0, "Sprites/block.png", all_entities=None)

    def update(self, a, b):
        pass
