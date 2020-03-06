import pygame
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 480
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

# Searches through your computer and finds a font that is similar to 'arial' font
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy

        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # self.offsetx = x
        # self.offsety = y
        self.image = pygame.Surface((50,40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # self.rect.x = (WIDTH / 2) - self.rect.width / 2
        # self.rect.y = HEIGHT - 500
        self.speedx = 1
        self.speedy = 10
        self.previous_pos = 0
        self.move_down = 0

    def update(self):
        # Move in the right direction
        if (self.previous_pos < self.rect.x and self.rect.x < WIDTH - (self.rect.width)) or (self.rect.x <= 0):
            self.previous_pos = self.rect.x
            self.rect.x += self.speedx
            if self.move_down == 1:
                self.rect.y += self.speedy
            self.move_down = 0

        else:
            self.previous_pos = self.rect.x
            self.rect.x -= self.speedx
            if self.move_down == 0:
                self.rect.y += self.speedy
            self.move_down = 1

# load all game graphics
background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
background_rect = background.get_rect()
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()

# Game loop
game_over = True
running = True
while running:
    if game_over:
        # show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        x = 20
        y = 20
        for mob_col in range(0, 4):
            for mob in range(0, 7):
                mob = Mob(x,y)
                all_sprites.add(mob)
                x += 65
            y += 50
            x = 20

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    all_sprites.update()

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    
    # *after* drawing everything, flip the display
    pygame.display.flip()

