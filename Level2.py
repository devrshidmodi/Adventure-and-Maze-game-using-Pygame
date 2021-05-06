import pygame
import mainapp
import maze2

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
COLOR = (24, 128, 148)
RED = (255, 0, 0)
PURPLE = (148,0,211)
MUTATE = (247,8,157)

sw = 800
sh = 600

screen = pygame.display.set_mode([sw, sh])

clock = pygame.time.Clock()

jungle = pygame.image.load("jungle.jpg")
standing = pygame.image.load("CQ.png")
coinImg = pygame.image.load("coin.png")
congratsImg = pygame.image.load("rainbowbackground.jpg")

class Player(pygame.sprite.Sprite):

    def __init__(self, position, images):

        #super().__init__()

        pygame.sprite.Sprite.__init__(self)

        size = (58, 70)

        self.rect = pygame.Rect(position, size)
        self.images = images
        self.images_right = images
        self.images_left = [pygame.transform.flip(image, True, False) for image in images]
        self.index = 0
        self.image = images[self.index]

        self.move_x = 0
        self.move_y = 0

        self.animation_frames = 6
        self.current_frame = 0


        #self.level = None

    def update_frame_dependant(self):
        if self.move_x > 0:
            self.images = self.images_right
        elif self.move_x < 0:
            self.images = self.images_left

        self.current_frame += 1
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

    def update(self):
        #Move the Player

        self.update_frame_dependant()

        #Gravity
        self.gravity()

        #Moving left or right
        self.rect.x += self.move_x

        #Check for any collision
        collide_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in collide_list:
            if self.move_x > 0:
                self.rect.right = block.rect.left
            elif self.move_x < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.move_y

        collide_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in collide_list:
            if self.move_y > 0:
                self.rect.bottom = block.rect.top
            elif self.move_y < 0:
                self.rect.top = block.rect.bottom

                self.change_y = 0

    def gravity(self):

        if self.move_y == 0:
            self.move_y = 1
        else:
            self.move_y += 0.40

        if self.rect.y >= sh - self.rect.height and self.move_y >= 0:
            self.move_y = 0
            self.rect.y = sh - self.rect.height

    def jump(self):

        self.rect.y += 2
        collide_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        if  len(collide_list) > 0 or self.rect.bottom >= sh:
            self.move_y = -10

    def move_left(self):

        self.move_x = -5

    def move_right(self):

        self.move_x = 5

    def stop(self):

        self.move_x = 0

class Enemy(pygame.sprite.Sprite):

    def __init__(self):

        #super().__init__()

        pygame.sprite.Sprite.__init__(self)
        width = 40
        height = 40
        self.image = pygame.Surface([width, height])
        self.image.fill(COLOR)

        self.rect = self.image.get_rect()

        self.changex = 0
        self.changey = 0

    def update(self):

        self.grav()

        self.rect.y += self.changey

    def grav(self):

        if self.changey == 0:
            self.changey = 1
        else:
            self.changey = 0.4

        if self.rect.y >= sh - self.rect.height and self.changey >= 0:
            self.changey = 0
            self.rect.y = sh - self.rect.height

class Coin(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        pygame.sprite.Sprite.__init__(self)
        width = 40
        height = 40
        self.image = coinImg

        self.rect = self.image.get_rect()

class ExitDoor(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        pygame.sprite.Sprite.__init__(self)
        width = 20
        height = 60
        self.image = pygame.Surface([width, height])
        self.image.fill(PURPLE)

        self.rect = self.image.get_rect()


class Platform(pygame.sprite.Sprite):

    def __init__(self, width, height):

        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()


class Level:

    def __init__(self, player):

        self.platform_list = pygame.sprite.Group()
        self.player = player

        self.background = None

    def update(self):

        self.platform_list.update()

    def draw(self, screen):

        self.platform_list.draw(screen)


class Level_1(Level):

    def __init__(self, player):

        Level.__init__(self, player)

        # List containing the width, height, x position and y position of the platform
        level = [[500, 20, 400, 480],
                 [300, 20, 0, 250],
                 [200, 20, 400, 350],
                 [400, 20, 400, 120],
                 ]

        #Go through the array and add the platform blocks
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

def healthBar(bw):

    livesbar = pygame.draw.rect(screen, RED, [200, 20, bw, 20])

    font = pygame.font.SysFont('Impact', 24)
    TextSurf = font.render("Health: ", False, WHITE)
    screen.blit(TextSurf, [120, 15])

def gameScoreDisplay(rt):

    font = pygame.font.SysFont('Impact', 24)
    TextSurf = font.render("Success Rate: " + str(rt), True, WHITE)
    screen.blit(TextSurf, [600, 15])

def writeScores(rt):

    # File is opened and the lines are stored into an array
    file = open('gamescores.txt', 'r')
    score_list = file.readlines()
    file.close()

    score_list.append(str(rt) + ',')

    #The lines in the array are then appended into the database with the player's code
    file = open("gamescores.txt", 'w')
    file.writelines(score_list)
    file.close()



def gameOver(rt):

    checkPoint = 0
    clock = pygame.time.Clock()

    writeScores(rt)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(BLACK)

        my_font = pygame.font.SysFont('Impact', 100)
        TextSurf = my_font.render('Game Over!', False, RED)
        screen.blit(TextSurf, [135, 200])

        my_font2 = pygame.font.SysFont('Impact', 70)
        TextSurf2 = my_font2.render('Score: '+ str(rt), False, WHITE)
        screen.blit(TextSurf2, [135, 300])

        checkPoint += 1

        if checkPoint == 35:
            mainapp.intro_screen()

        pygame.display.update()
        clock.tick(20)

def congrats(rt):

    checkPoint = 0
    clock = pygame.time.Clock()

    writeScores(rt)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(congratsImg, [0, 0])

        my_font = pygame.font.SysFont('Impact', 100)
        TextSurf = my_font.render('Congrats', False, WHITE)
        screen.blit(TextSurf, [135, 200])

        my_font2 = pygame.font.SysFont('Impact', 64)
        TextSurf2 = my_font2.render('Now complete the maze', False, WHITE)
        screen.blit(TextSurf2, [50, 400])

        checkPoint += 1

        if checkPoint == 35:
            maze2.main_maze()

        pygame.display.update()

        clock.tick(20)


def main():
    # Main Function
    images = [pygame.image.load('CQ.png'), pygame.image.load('CR1.png'), pygame.image.load('CR2.png'), pygame.image.load('CR3.png'), pygame.image.load('CR4.png'), pygame.image.load('CR5.png'), pygame.image.load('CR6.png'), pygame.image.load('CR7.png'), pygame.image.load('CR8.png'), pygame.image.load('CR9.png')]

    player = Player(position = (340, 530), images = images)

    enemy = Enemy()
    enemy2 = Enemy()
    enemy3 = Enemy()
    enemy4 = Enemy()

    # Coins on the first platform
    coin = Coin()
    coin2 = Coin()
    coin3 = Coin()
    # Coins on the second platform
    coin4 = Coin()
    coin5 = Coin()
    coin6 = Coin()
    # Coins on the last platform
    coin7 = Coin()
    coin8 = Coin()

    door = ExitDoor()

    level_list = []
    level_list.append(Level_1(player))

    level_now = level_list[0]

    sprite_list = pygame.sprite.Group()
    player.level = level_now

    player.rect.x = 340
    player.rect.y = sh - player.rect.height
    sprite_list.add(player)

    enemy.rect.x = 0
    enemy.rect.y = sh - enemy.rect.height
    sprite_list.add(enemy)
    enx = 5

    enemy2.rect.x = 400
    enemy2.rect.y = 350 - enemy.rect.height
    sprite_list.add(enemy2)
    enx2 = 5

    enemy3.rect.x = 0
    enemy3.rect.y = 250 - enemy.rect.height
    sprite_list.add(enemy3)
    enx3 = 5

    enemy4.rect.x = 400
    enemy4.rect.y = 120 - enemy.rect.height
    enemy4.image.fill(MUTATE)
    sprite_list.add(enemy4)
    enx4 = 5

    # Coin positioning
    coin.rect.x = 700
    coin.rect.y = sh - coin.rect.height
    sprite_list.add(coin)

    coin2.rect.x = 600
    coin2.rect.y = sh - coin2.rect.height
    sprite_list.add(coin2)

    coin3.rect.x = 500
    coin3.rect.y = 120 - coin3.rect.height
    sprite_list.add(coin3)

    coin4.rect.x = 450
    coin4.rect.y = 350 - coin4.rect.height
    sprite_list.add(coin4)

    coin5.rect.x = 575
    coin5.rect.y = 350 - coin5.rect.height
    sprite_list.add(coin5)

    coin6.rect.x = 680
    coin6.rect.y = 120 - coin6.rect.height
    sprite_list.add(coin6)

    coin7.rect.x = 100
    coin7.rect.y = 250 - coin7.rect.height
    sprite_list.add(coin7)

    coin8.rect.x = 250
    coin8.rect.y = 250 - coin8.rect.height
    sprite_list.add(coin8)

    #exit Door
    door.rect.x = 780
    door.rect.y = 120 - door.rect.height
    sprite_list.add(door)

    barwidth = 200

    rate = None

    pygame.display.set_caption('Dungeon Dweller Game')

    game = False

    while not game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move_left()
                if event.key == pygame.K_RIGHT:
                    player.move_right()
                if event.key == pygame.K_SPACE:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.move_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.move_x > 0:
                    player.stop()


        #player.update()
        screen.blit(jungle, [0, 0])

        sprite_list.update()

        level_now.update()

        healthBar(barwidth)

        rate = int((barwidth / 200) * 100)

        gameScoreDisplay(rate)

        enemy.rect.x += enx
        enemy2.rect.x += enx2
        enemy3.rect.x += enx3
        enemy4.rect.x += enx4

        if enemy.rect.right > sw:
            enx = -5
        elif enemy.rect.left <= 0:
            enx = 5

        if enemy2.rect.right >= 600:
            enx2 = -5
        elif enemy2.rect.left <= 400:
            enx2 = 5

        if enemy3.rect.right >= 300:
            enx3 = -5
        elif enemy3.rect.left <= 0:
            enx3 = 5

        if enemy4.rect.right >= 800:
            enx4 = -6
        elif enemy4.rect.left <= 400:
            enx4 = 6

        #Player and slime blob  collisions
        # if player.rect.y < enemy.rect.y + enemy.rect.height:
        #     if player.rect.x > enemy.rect.x and player.rect.x < enemy.rect.x + enemy.rect.width or player.rect.x + player.rect.width > enemy.rect.x and player.rect.x + player.rect.width < enemy.rect.x + enemy.rect.width:
        #         print("YOU GOT HIT")

        if player.rect.colliderect(enemy):
            barwidth -= 4

        if player.rect.colliderect(enemy2):
            barwidth -= 4

        if player.rect.colliderect(enemy3):
            barwidth -= 4

        if player.rect.colliderect(enemy4):
            barwidth -= 3

        #Collisions with the coin
        if player.rect.colliderect(coin):
            coin.rect.x = 850
        if player.rect.colliderect(coin2):
            coin2.rect.x = 850
        if player.rect.colliderect(coin3):
            coin3.rect.x = 850
        if player.rect.colliderect(coin4):
            coin4.rect.x = 850
        if player.rect.colliderect(coin5):
            coin5.rect.x = 850
        if player.rect.colliderect(coin6):
            coin6.rect.x = 850
        if player.rect.colliderect(coin7):
            coin7.rect.x = 850
        if player.rect.colliderect(coin8):
            coin8.rect.x = 850

        if player.rect.colliderect(door):
            if coin.rect.x > 800 and coin2.rect.x > 800 and coin3.rect.x > 800 and coin4.rect.x > 800 and coin5.rect.x > 800 and coin6.rect.x > 800 and coin7.rect.x > 800 and coin8.rect.x > 800:
                congrats(rate)
            else:
                player.rect.x = door.rect.right



        if player.rect.right > sw:
            player.rect.right = sw

        if player.rect.left < 0:
            player.rect.left = 0

        if barwidth <= 0:
            gameOver(rate)

        #Check to see if there are collisions between the slime blob and the character
        #hits = pygame.sprite.spritecollide(enemy, player, True, True)

        level_now.draw(screen)
        sprite_list.draw(screen)

        clock.tick(60)
        pygame.display.update()

    pygame.quit()
    quit()
