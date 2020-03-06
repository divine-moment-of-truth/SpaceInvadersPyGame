import pygame
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

##  CONSTANTS ##

## Player Constants ##
PLAYERWIDTH = 40
PLAYERHEIGHT = 10
PLAYERCOLOR = GREEN
PLAYER1 = 'Player 1'
PLAYERSPEED = 5

## Enemy Constants ##
ENEMYWIDTH = 25
ENEMYHEIGHT = 25
ENEMYNAME = "Enemy"
ENEMYGAP = 20
ARRAYWIDTH = 10
ARRAYHEIGHT = 4
MOVETIME = 1000
MOVEX = 10
MOVEY = ENEMYHEIGHT
TIMEOFFSET = 300

## Display Constants ##
GAMETITLE = "Space Invaders!"
DISPLAYWIDTH = 640
DISPLAYHEIGHT = 480
BGCOLOR = NEARBLACK
XMARGIN = 50
YMARGIN = 50
FPS = 60

## Direction Dictionary ##
## This dictionary allows for shooting bullets while moving without ##
## the inputs interupting each other.                               ##
DIRECT_DICT = {pygame.K_LEFT  : (-1),
               pygame.K_RIGHT : (1)}

##  COLOURS ##
#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (0, 0, 0)
RED       = (255, 0, 0)
GREEN     = (0, 255, 0)
BLUE      = (0, 0, 255)
YELLOW    = (255, 255, 0)
NEARBLACK = ( 19,  15,  48)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = PLAYERWIDTH
        self.height = PLAYERHEIGHT
        self.image = pygame.Surface((self.width, self.height))
        self.color = PLAYERCOLOR
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.name = PLAYER1
        self.speed = PLAYERSPEED
        self.vectorx = 0


        self.rect.centerx = DISPLAYWIDTH / 2
        self.rect.bottom = ARRAYHEIGHT - 10
        self.speedx = 0
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

    def update(self, keys, *args):
        for key in DIRECT_DICT:
            if keys[key]:
                self.rect.x += keys[key] * self.speed

            self.checkForSides(self)
            self.image.fill(self.color)

    def checkForSides(self)
        if self.rect.right > DISPLAYWIDTH:
            self.rect.right = DISPLAYWIDTH
            self.vectorx = 0
        elif self.rect.left < 0:
            self.rect.left = 0
            self.vectorx = 0      

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

class Enemy(pygame.sprite.Sprite):
    def __init__(self, row, column):
        pygame.sprite.Sprite.__init__(self)
        self.width = ENEMYWIDTH
        self.height = ENEMYHEIGHT
        self.row = row
        self.column = column
        self.image = self.setImage()
        self.rect = self.rect.get_rect()
        self.name = 'enemy'
        self.vectorx = 1
        self.moveNumber = 0
        self.moveTime = MOVETIME
        self.timeOffset = row * TIMEOFFSET
        self.timer = pygame.time.get_ticks() - self.timeOffset

    def update(self, keys, currentTime):
        if current - self.timer > self.moveTime
            if self.moveNumber < 6:
                self.rect.x += MOVEX * self.vectorx
                self.moveNumber =+ 1
            elif self.moveNumber >= 6:
                self.vectorx *= -1
                self.moveNumber = 0
                self.rect.y += MOVEY
                if self.moveTime > 100:
                    self.moveTime -= 50
            self.timer = currentTime

    def setImage(self):
        if self.row == 0:
            image = pygame.image.load('alien1.png')
        elif self.row == 1:
            image = pygame.image.load('alien2.png')
        elif self.row == 2:
            image = pygame.image.load('alien3.png')
        else:
            image = pygame.image.load('alien1.png')
        image.convert_alpha()
        image = pygame.transform.scale(image, (self.width, self.height))

        return image


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
        # self.rect.x = (DISPLAYWIDTH / 2) - self.rect.DISPLAYWIDTH / 2
        # self.rect.y = ARRAYHEIGHT - 500
        self.speedx = 5
        self.speedy = 10
        self.previous_pos = 0
        self.move_down = 0
        self.move_right_count = 0
        self.move_left_count = 0

    def update(self):
        # Move in the right direction
        if self.move_right_count < 10:
            if self.move_left_count == 9 and self.move_right_count == 0:
                self.rect.y += self.speedy
            else:
                self.rect.x += self.speedx
            self.move_right_count += 1
            if self.move_right_count == 9:
                self.move_left_count = 0
                # self.rect.y += self.speedy
        elif self.move_left_count < 10:
            if self.move_right_count == 9 and self.move_left_count == 0:
                self.rect.y += self.speedy
            else:
                self.rect.x -= self.speedx
            self.move_left_count += 1
            if self.move_left_count == 9:
                self.move_right_count = 0
                # self.rect.y += self.speedy


class app(object):
    def __init__(self):
        pygame.init()
        self.displaySurf, self.displayRect = self.makeScreen()
        self.gameStart = True
        self.gameOver = False 
        self.beginGame = False

    def resetGame(self):
        self.gameStart = True
        self.needToMakeEnemies = True

        self.introMessage1 = Text('orena.ttf', 25,
                                    'Welcome to Space Invaders!',
                                    GREEN, self.displayRect,
                                    self.displaySurf)

        self.introMessage2 = Text('orena.ttf', 20,
                                  'Press Any Key to Continue',
                                  GREEN, self.displayRect,
                                  self.displaySurf)

        self.introMessage2.rect.top = self.introMessage1.rect.bottom + 5

        self.gameOverMessage = Text('orena.ttf', 25,
                                    'GAME OVER', GREEN,
                                    self.displayRect, self.displaySurf)

        self.player = self.makePlayer()
        self.bullets = pygame.sprite.Group()
        self.greenBullets = pygame.sprite.Group()
        # self.blockerGroup1 = self.makeBlocker(0)
        # self.blockerGroup2 = self.makeBlocker(1)
        # self.blockerGroup3 = self.makeBlocker(2)
        # self.blockerGroup4 = self.makeBlocker(3)
        # self.allBlockers = pygame.sprite.Group(self.blockerGroup1, self.blockerGroup2, 
                                                self.blockerGroup3, self.blockerGroup4)

        self.allsprites = pygame.sprite.Group(self.player) # , self.allBlockers)
        self.keys = pygame.key.get_pressed()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.enemyMove = 0
        self.enemyBulletTimer = pygame.time.get_ticks()
        self.gameOver = False
        self.gameOverTime = pygame.time.get_ticks()


    #def makeBlockers(self, number=1):
    #    blockGroup = pygame.sprite.Group()

    #    for row in range(5):
    #        for column in range(7):
    #            blocker = Blocker(10, GREEN, row, column)

    #    for blocker in blockerGroup:
    #                if (blocker.column == 0 and blocker.row == 0
    #                    or blocker.column == 6 and blocker.row == 0):
    #                    blocker.kill()

    #            return blockerGroup


    def makeScreen(self):
        pygame.display.set_caption(GAMETITLE)
        displaySurf = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT))
        displayRect = displaySurf.get_rect()
        displaySurf.fill(BGCOLOR)
        displaySurf.convert()

        return displaySurf, displayRect

    def makePlayer(self):
        player = Player()
        ##Place the player centerx and five pixels from the bottom
        player.rect.centerx = self.displayRect.centerx
        player.rect.bottom = self.displayRect.bottom - 5

        return player

    def makeEnemies(self):
        enemies = pygame.sprite.Group()

        for row in range(ARRAYHEIGHT):
            for column in range(ARRAYWIDTH)
                enemy = Enemy(row, column)
                enemy.rect.x = XMARGIN + (column * (ENEMYWIDTH + ENEMYGAP))
                enemy.rect.y = YMARGIN + (row * (ENEMYHEIGHT + ENEMYGAP))
                enemies.add(enemy)

        return enemies

    def draw_text(surf, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def checkInput(self):
        for event in pygame.event.get():
            self.keys = pygame.key.get_pressed()
            if event.type == QUIT:
                self.terminate()

            # elif event.type == KEYDOWN:
            #     if event.key == K_SPACE and len(self.greenBullets) < 1:
            #         bullet = Bullet(self.player.rect, GREEN, -1, 20)
            #         self.greenBullets.add(bullet)
            #         self.bullets.add(self.greenBullets)
            #         self.allSprites.add(self.bullets)
            #         self.laserSound.play()
            #     elif event.key == K_ESCAPE:
            #         self.terminate()

    def gameStartInput(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.terminate()
            elif event.type == KEYUP:
                self.gameOver = False
                self.gameStart = False
                self.beginGame = True

    def gameOverInput(self):
        for event in pygame.event.get():
            self.key = pygame.key.get_pressed()
            if event.type == QUIT:
                self.terminate()

            elif event.type = KEYUP:
                self.gameStart= True
                self.beginGame = False
                self.gameOver = False

    def checkGameOver(self):
        if len(self.enemies) == 0:
            self.gameOver = True
            self.gameStart = False
            self.beginGame = False
            self.gameOverTime = pygame.time.get_ticks()



    def terminate(self):
        pygame.quit()
        sys.exit()

    # Game loop
    def mainLoop(self):
        while True:
            if self.gameStart:
                self.resetGame()
                self.gameOver = False
                self.displaySurf.fill(BGCOLOR)
                self.introMessage1.draw(self.displaySurf)
                self.introMessage2.draw(self.displaySurf)
                self.gameStartInput()
                pygame.display.update()

            elif self.gameOver:
                self.displaySurf.fill(BGCOLOR)
                self.gameOverMessage.draw(self.displaySurf)
                #prevent users from exiting the GAME OVER screen
                #too quickly
                if (pygame.time.get_ticks() - self.gameOverTime) > 2000:
                    self.gameOverInput()
                pygame.display.update()

            elif self.beginGame:
                if self.needToMakeEnemies:
                    self.enemies = self.makeEnemies()
                    self.allsprites.add(self.enemies)
                    self.needToMakeEnemies = False
                    pygame.event.clear()

                else:
                    currentTime = pygame.time.get_ticks()
                    self.displaySurf.fill(BGCOLOR)
                    self.checkInput()
                    self.allsprites.update(self.keys, currentTime)
                    if len(self.enemies) > 0:
                        # self.fineEnemyShooter()
                        # self.shootEnemyBullet(self.shooter.rect)
                    # self.checkCollisions()
                    self.allsprites.draw(self.displaySurf)
                    self.blockerGroup1.draw(self.displaySurf)
                    pygame.display.update()
                    self.checkGameOver()
                    self.clock.tick(self.fps)

            if game_over:
                # show_go_screen()
                game_over = False
                all_sprites = pygame.sprite.Group()
                mob_sprites = pygame.sprite.Group()
                player = Player()
                all_sprites.add(player)
                x = 123
                y = 20
                for mob_col in range(0, 4):
                    for mob in range(0, 7):
                        mob = Mob(x,y)
                        # all_sprites.add(mob)
                        mob_sprites.add(mob)
                        x += 65
                    y += 50
                    x = 123

            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
            all_sprites.update()

            mob_sprites.update()

            # Draw / render
            screen.fill(BLACK)
            screen.blit(background, background_rect)
            all_sprites.draw(screen)

            mob_sprites.draw(screen)
            
            # *after* drawing everything, flip the display
            pygame.display.flip()




## OLD PROG ##

pygame.mixer.init()
screen = pygame.display.set_mode((DISPLAYWIDTH, ARRAYHEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

# load all game graphics
background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
background_rect = background.get_rect()
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()

# Searches through your computer and finds a font that is similar to 'arial' font
font_name = pygame.font.match_font('arial')
        