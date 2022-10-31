import pygame
import uuid


def place_meeting(x, y, w, h, rect: pygame.Rect):
    test_rect = pygame.Rect(x, y, w, h)
    return test_rect.colliderect(rect)


def lerp(a, b, t):
    return a + (b - a) * t


## GUI elements ##
class Color:
    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b


class GuiElement:
    def __init__(self, surface, x, y, width, height, color, parent=None):
        self.parent = parent
        self.surface = surface
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.children = []
        if parent:
            self.parent.children.append(self)
            self.x = parent.x + x
            self.y = parent.y + y

            w, h = pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height()
            px = self.width / w
            py = self.height / h
            self.width = parent.width * px
            self.height = parent.height * py
        self.rect = pygame.rect.Rect(self.x, self.y, width, height)

    def move_to_pixels(self, x, y):

        if self.parent:
            self.x = self.parent.x + x
            self.y = self.parent.y + y
        else:
            self.x = x
            self.y = y

        self.rect.x = self.x
        self.rect.y = self.y

    def move_to_percentage(self, px=0, py=0):
        pass


class Frame(GuiElement):
    def __init__(self, surface, x, y, width, height, color, parent=None):
        super().__init__(surface, x, y, width, height, color, parent)

    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect)
        for child in self.children:
            child.draw()


class Button(GuiElement):
    def __init__(self, surface, x, y, width, height, default_color, hover_color, text="Button", parent=None):
        super().__init__(surface, x, y, width, height, default_color, parent)
        self.text = text
        self.hover_color = hover_color


class TextInput(GuiElement):
    def __init__(self, surface, x, y, width, height, return_callback=None, text="", parent=None):
        super().__init__(surface, x, y, width, height, (255, 255, 255), parent)
        self.text = text
        self.active: bool = False
        self.font = pygame.font.Font(None, 24)
        self.inital_timer = 50
        self.timer = 0
        self.flag = False
        self.return_callback = return_callback

    def listen(self, event):
        mx, my = pygame.mouse.get_pos()

        if self.rect.collidepoint(mx, my) and event.type == pygame.MOUSEBUTTONDOWN:
            self.active = True
        elif not self.rect.collidepoint(mx, my) and event.type == pygame.MOUSEBUTTONDOWN:
            self.active = False

        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and len(self.text) > 0:
                    self.text = self.text.replace(self.text[-1], '')
                else:
                    self.text += event.unicode

                if event.key == pygame.K_RETURN:
                    self.return_callback(self.text)

    def draw(self):
        if self.active:
            self.timer += 1
            if self.timer % self.inital_timer == 0:
                self.flag = not self.flag
            if self.flag:
                col = (255, 255, 255)
            else:
                col = (0, 0, 0)
        else:
            col = (255, 255, 255)
        pygame.draw.rect(self.surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        self.surface.blit(text_surface, (self.x + 5, self.y + self.height // 2))
        pygame.draw.rect(self.surface, col, pygame.rect.Rect(self.x + 3, self.y + 2, 2, self.rect.height - 2))


class ImageBox(GuiElement):
    def __init__(self, surface, x, y, width, height, color, image_path, parent=None):
        super().__init__(surface, x, y, width, height, color, parent)
        self.image_path = image_path
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

    def draw(self):
        self.surface.blit(self.image, (self.x, self.y))


class ProgressBar(GuiElement):
    def __init__(self, surface, x, y, width, height, inner_min_color, inner_max_color, outer_color, parent=None):
        super().__init__(surface, x, y, width, height, outer_color, parent)
        self.inner_min_color = inner_min_color
        self.inner_max_color = inner_max_color
        self.rect_inner = self.rect.copy()
        self.percentage = 1
        self.set_bar_percentage(1)

    def draw(self):
        final_color = (
            lerp(self.inner_min_color[0], self.inner_max_color[0], self.percentage),
            lerp(self.inner_min_color[1], self.inner_max_color[1], self.percentage),
            lerp(self.inner_min_color[2], self.inner_max_color[2], self.percentage)
        )
        pygame.draw.rect(self.surface, self.color, self.rect)
        pygame.draw.rect(self.surface, final_color, self.rect_inner)

    def set_bar_percentage(self, percentage):
        if percentage > 0:
            self.rect_inner.width = self.rect.width * percentage
            self.percentage = percentage


class GameEntity(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy, sprite_path, all_entities):
        pygame.sprite.Sprite.__init__(self)
        self.damage_timer = 50
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
        self.jump_speed = 4
        self.in_air = False
        self.gy = 0.3
        self.angle = 0
        self.has_gravity = True
        self.can_collide = True
        self.dx = 0
        self.dy = 0

    def fill(self, surface, color):
        """Fill all pixels of the surface with color, preserve transparency."""
        w, h = surface.get_size()
        r, g, b, _ = color
        for x in range(w):
            for y in range(h):
                a = surface.get_at((x, y))[3]
                surface.set_at((x, y), pygame.Color(r, g, b, a))

    def take_damage(self):
        pass

    def handle_collisions(self, entities: [], dt, axis, collision_tolerance=0.3):
        filtered_entities = list(filter(lambda e: e != self and self.collision_region.colliderect(e.rect), entities))
        colliding_entities = []
        for entity in filtered_entities:
            if entity.can_collide and self.rect.colliderect(entity.rect):
                colliding_entities.append(entity)
        for e in entities:
            if e != self:
                if e.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height):
                    self.dx = 0
                    # self.vx = 0

                if e.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height):
                    if abs(self.vy) > 5:
                        fallen = pygame.mixer.Sound("Sounds/fall_solid.mp3")
                        pygame.mixer.Sound.play(fallen)
                    if abs(self.vy) > 10:
                        fallen = pygame.mixer.Sound("Sounds/fall_damage2.mp3")
                        pygame.mixer.Sound.play(fallen)
                        self.take_damage()
                    if self.vy < 0:
                        self.dy = e.rect.bottom - self.rect.top
                        self.vy += self.dy
                    elif self.vy >= 0:
                        self.dy = e.rect.top - self.rect.bottom
                        self.vy = 0

    def update(self, a, b):
        if self.has_gravity:
            self.vy += self.gy

        self.dy += self.vy
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.collision_region.x = self.rect.x
        self.collision_region.y = self.rect.y


class Player(GameEntity):
    def __init__(self, x, y, all_entities, sprite_path="Sprites/stickman.png"):
        GameEntity.__init__(self, x, y, 0, 0, sprite_path, all_entities)
        self.walkspeed = 3
        self.default_walkspeed = 3
        self.gy = 0.0125
        self.horizontal = 0
        self.vertical = 0
        self.xspawn = self.rect.x
        self.yspawn = self.rect.y
        self.name = "Player_" + str(uuid.uuid4()).split('-')[0]
        self.event_flag = False
        self.damage_timer = 50

    def respawn(self):
        self.rect.x = self.xspawn
        self.rect.y = self.yspawn
        self.vx = 0
        self.vy = 0

    def update(self, a, dt):
        self.dx = 0
        self.dy = 0
        key = pygame.key.get_pressed()
        if not self.event_flag:
            if key[pygame.K_a]:
                self.dx = -self.walkspeed

            if key[pygame.K_r]:
                self.respawn()

            if key[pygame.K_d]:
                self.dx = self.walkspeed

            if key[pygame.K_SPACE] and not self.in_air:
                self.vy -= self.jump_speed * 1
            pygame.event.pump()

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


class Ball(GameEntity):
    def __init__(self, x, y, all_entities):
        GameEntity.__init__(self, x, y, 0, 0, "Sprites/ball.png", all_entities=all_entities)

    def handle_collisions(self, entities: [], dt, axis, collision_tolerance=0.3):
        filtered_entities = list(filter(lambda e: e != self and self.collision_region.colliderect(e.rect), entities))
        colliding_entities = []
        for entity in filtered_entities:
            if entity.can_collide and self.rect.colliderect(entity.rect):
                colliding_entities.append(entity)
        for e in entities:
            if e.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height):
                self.vx -= e.vx
                # self.vx = 0

            if e.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height):

                if self.vy < 0:
                    self.dy = e.rect.bottom - self.rect.top
                    self.vy -= self.dy
                elif self.vy >= 0:
                    self.dy = e.rect.top - self.rect.bottom
                    self.vy -= self.dy


def generate_baseplate(x, y, w, sprites: pygame.sprite.Group, entities):
    for i in range(w // 32):
        block = Block(x + i * 32, 512 - 32)
        sprites.add(block)
        entities.append(block)


class World:
    def __init__(self, background, w_width=1024, w_height=512):
        self.window = pygame.display.set_mode((w_width, w_height))
        pygame.display.set_caption("Stick")
        self.entities = []
        self.sprites = pygame.sprite.Group()
        self.gui_elements = []
        self.background = ImageBox(self.window, 0, 0, w_width, w_height, (0, 0, 0), background)
        self.w_width = w_width
        self.w_height = w_height
        self.events = pygame.event.get()
        self.inputs = []

    def draw_gui(self):
        for gui_element in self.gui_elements:
            gui_element.draw()

    def generate_flatworld_file(self):
        f = open("Level/flat.txt", "w")
        for i in range(self.w_width):
            f.write("BLOCK" + " " + str(i * 32) + " " + str(self.w_height - 32) + "\n")

    def generate_flatworld(self):
        for i in range(self.w_width):
            block = Block(i * 32, self.w_height - 32)
            self.sprites.add(block)
            self.entities.append(block)

    def load_world(self, fname):
        f = open(fname, "r")
        for line in f:
            entity = line.split(" ")

            if entity[0] == "BLOCK":
                x = int(entity[1])
                y = int(entity[2])
                block = Block(x, y)
                self.entities.append(block)
                self.sprites.add(block)

    def game_loop(self):
        player = Player(self.w_width // 2, self.w_height // 2, self.entities)
        self.entities.append(player)
        self.sprites.add(player)
        clock = pygame.time.Clock()
        dt = 0
        self.generate_flatworld()

        while True:
            for event in self.events:
                for i in self.inputs:
                    i.listen(event)

            self.sprites.update(self.events, dt)

            self.window.fill((0, 0, 0))
            self.background.draw()
            self.sprites.draw(self.window)
            pygame.display.update()
            dt = clock.tick(60)
