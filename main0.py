# Devrshi Modi, Raghu Alluri
#June 16th, 2020
# This program is coded for a platformer game slightly similar to that of Mario

# Importing the pygame module and the neccessary files
import pygame
import maze
import highscores
import Level2

# Initializing pygame functionalities
pygame.init()

# Defining colors needed for the game
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
COLOR = (24, 128, 148)
RED = (255, 0, 0)
PURPLE = (148,0,211)
MUTATE = (247, 8, 159)

# Defining the screen width and height
sw = 800
sh = 600

# Starting up the screen (Window)
screen = pygame.display.set_mode([sw, sh])

# Defining a clock to keep track for the FPS
clock = pygame.time.Clock()

# Importing all needed images for this game
jungle = pygame.image.load("jungle.jpg")
standing = pygame.image.load("CQ.png")
coinImg = pygame.image.load("Coin.png")
congratsImg = pygame.image.load("rainbowbackground.jpg")
gradient = pygame.image.load("gradient.jpg")

# A class is created to make the player sprite and have him move around
class Player(pygame.sprite.Sprite):

    # Initializes the player sprite
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

    # Updates the frame to show the sprite animation
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

    # Updates the player to show his new position relative to his surroundings
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

    # Calculates gravity for the player
    def gravity(self):

        if self.move_y == 0:
            self.move_y = 1
        else:
            self.move_y += 0.40

        if self.rect.y >= sh - self.rect.height and self.move_y >= 0:
            self.move_y = 0
            self.rect.y = sh - self.rect.height


    # Controls the jumping of the player
    def jump(self):

        self.rect.y += 2
        collide_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        if  len(collide_list) > 0 or self.rect.bottom >= sh:
            self.move_y = -10

    # Control the x and y movement of the player

    def move_left(self):

        self.move_x = -5

    def move_right(self):

        self.move_x = 5

    def stop(self):

        self.move_x = 0

# Another class is created for the enemy
class Enemy(pygame.sprite.Sprite):

    # The sprite is initialized
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

    # Updates to show new position
    def update(self):

        self.grav()

        self.rect.y += self.changey

    # Calculates gravity for the enemy
    def grav(self):

        if self.changey == 0:
            self.changey = 1
        else:
            self.changey = 0.4

        if self.rect.y >= sh - self.rect.height and self.changey >= 0:
            self.changey = 0
            self.rect.y = sh - self.rect.height

# A new class for the coins
class Coin(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        pygame.sprite.Sprite.__init__(self)
        width = 40
        height = 40
        self.image = coinImg

        self.rect = self.image.get_rect()

# Class for the exit door in the game
class ExitDoor(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        pygame.sprite.Sprite.__init__(self)
        width = 20
        height = 60
        self.image = pygame.Surface([width, height])
        self.image.fill(PURPLE)

        self.rect = self.image.get_rect()

# A class is created for instruction and characteristic of the platforms
class Platform(pygame.sprite.Sprite):

    # Initializes the platform class
    def __init__(self, width, height):

        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()

# A Level class is made specifically for Level characteristics
class Level:

    # Level characteristics are initialized
    def __init__(self, player):

        self.platform_list = pygame.sprite.Group()
        self.player = player

        self.background = None

    def update(self):

        self.platform_list.update()

    def draw(self, screen):

        self.platform_list.draw(screen)

# A class is made for the actual Level 1 and how it will look like
class Level_1(Level):

    # Initializes the Level 1
    def __init__(self, player):

        Level.__init__(self, player)

        # List containing the width, height, x position and y position of the platform
        level = [[500, 20, 0, 480],
                 [300, 20, 400, 350],
                 [400, 20, 0, 220],
                 ]

        # Go through the array and add the platform blocks
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

# Function for the introductory screen when the user opens the program
def intro_screen():

    size = [800, 600]

    # Background is set for this screen
    background = pygame.Surface(size)
    background = background.convert()
    background = pygame.image.load("startscreen.jpg")

    # A few colors are defined
    gray = (140,140,145)
    light_gray = (190,190,200)
    white = (255,255,255)

    # Buttons shapes are made
    button1 = pygame.Rect(100,100,150,25)
    button2 = pygame.Rect(100,200,150,25)
    button3 = pygame.Rect(100,300,150,25)
    button4 = pygame.Rect(100,400,150,25)

    # Fonts are made and displayed
    my_font = pygame.font.SysFont("comicsansms", 48)
    my_font2 = pygame.font.SysFont("opensans",30)
    label = my_font.render("Dungeon Dweller", True, white)
    Play = my_font2.render("Play", True, white)
    Instructions = my_font2.render("Instructions", True, white)
    Credits = my_font2.render("Highscores", True, white)
    Quit = my_font2.render("Quit", True, white)

    # The background and labels are blitted onto the screen
    screen.blit(background, (0,0))
    screen.blit(label, (250, 20))

    # A timer is set for the FPS
    timer = pygame.time.Clock()

    sets = True
    while sets:
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Gets the mouse position and see's if anything has been clicked
            if e.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = e.pos

                if button1.collidepoint(mouse_pos):
                    #print("Play")
                    main()
                elif button2.collidepoint(mouse_pos):
                    #print("Instructions")
                    main_instructor()
                elif button3.collidepoint(mouse_pos):
                    #print("High Scores")
                    highscores.main_scores()
                elif button4.collidepoint(mouse_pos):
                    pygame.quit()
                    quit()

            # Gets the mouse position
            must = pygame.mouse.get_pos()

            # Highlights the button of the mouse is over it
            if 100+150 > must[0] > 100 and 100+25 > must[1] > 100:
                pygame.draw.rect(screen, (255,0,0), button1)

            else:
                pygame.draw.rect(screen, (200,20,20) ,button1)

            if 100+150 > must[0] > 100 and 200+25 > must[1] > 200:
                pygame.draw.rect(screen, light_gray, button2)

            else:
                pygame.draw.rect(screen, gray, button2)

            if 100+150 > must[0] > 100 and 300+25 > must[1] > 300:
                pygame.draw.rect(screen, light_gray, button3)

            else:
                pygame.draw.rect(screen, gray, button3)

            if 100+150 > must[0] > 100 and 400+25 > must[1] > 400:
                pygame.draw.rect(screen, light_gray, button4)

            else:
                pygame.draw.rect(screen, gray, button4)

        # Blits the buttons onto the screen at their positions
        screen.blit(Play, (150,100))
        screen.blit(Instructions, (112,200))
        screen.blit(Credits, (140,300))
        screen.blit(Quit, (150,400))

        # Display is updated
        pygame.display.update()

def main_instructor():

    WHITE = (255,255,255)
    PINK = (255,0,72)

    sw=800
    sh=600

    screen = pygame.display.set_mode((sw,sh))
    pygame.display.set_caption("Instructions 1")

    background_image = pygame.image.load("forestcave1.png")

    def textx():
        buttonx=pygame.draw.rect(screen,PINK,[650,500,100,50])
        myfont=pygame.font.SysFont("Impact",40)
        TextSurf=myfont.render("Next",False,WHITE)
        screen.blit(TextSurf,[650,500])

    def text1():
        myfont=pygame.font.SysFont("Impact",40)
        TextSurf=myfont.render("Our brave hero needs your help",False,WHITE)
        screen.blit(TextSurf,[145,100])
        TextSurf=myfont.render("He must travel through the jungles of Sauron",False,WHITE)
        screen.blit(TextSurf,[55,170])
        TextSurf=myfont.render("And through the treacherous caves of Devrshi",False,WHITE)
        screen.blit(TextSurf,[55,240])
        TextSurf=myfont.render("All to find the golden tresure",False,WHITE)
        screen.blit(TextSurf,[170,310])




    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

        cursor = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()

        screen.blit(background_image , [0 , 0])

        if 650 < cursor[0] < 750 and 500 < cursor[1] < 550:
            if clicked[0] == 1:
                dhokla()

        text1()
        textx()
        pygame.display.update()



def dhokla():
    def BACKTEXT():
        buttonx=pygame.draw.rect(screen,PINK,[150,500,100,50])
        myfont=pygame.font.SysFont("Impact",40)
        TextSurf=myfont.render("BACK",False,WHITE)
        screen.blit(TextSurf,[150,500])
    def text2():
        myfont=pygame.font.SysFont("Impact",25)
        TextSurf=myfont.render("In order to move ",False,WHITE)
        screen.blit(TextSurf,[10,100])
        TextSurf=myfont.render("Press --> to move right",False,WHITE)
        screen.blit(TextSurf,[10,170])
        TextSurf=myfont.render("Press <-- to move left",False,WHITE)
        screen.blit(TextSurf,[10,240])
        TextSurf=myfont.render("Press Space to jump",False,WHITE)
        screen.blit(TextSurf,[10,310])
        TextSurf=myfont.render("Collect ......",False,WHITE)
        screen.blit(TextSurf,[400,100])
        TextSurf=myfont.render("Avoid ..........",False,WHITE)
        screen.blit(TextSurf,[400,170])
        TextSurf=myfont.render("Collect golden ..... for double points",False,WHITE)
        screen.blit(TextSurf,[400,240])
        TextSurf=myfont.render("Best of luck finding the tresure",False,WHITE)
        screen.blit(TextSurf,[400,310])

    while True:
        for devrshi in pygame.event.get():
            if devrshi.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(background_image, (0, 0))
        text2()
        BACKTEXT()
        pygame.display.flip()

# A Health Bar is created in this function
def healthBar(bw):

    livesbar = pygame.draw.rect(screen, RED, [200, 20, bw, 20])

    font = pygame.font.SysFont('Impact', 24)
    TextSurf = font.render("Health: ", False, WHITE)
    screen.blit(TextSurf, [120, 15])

# A display is made for the game score
def gameScoreDisplay(rt):

    font = pygame.font.SysFont('Impact', 24)
    TextSurf = font.render("Success Rate: " + str(rt), True, WHITE)
    screen.blit(TextSurf, [600, 15])

# A function is made to show a screen for gameover
def gameOver():

    checkPoint = 0
    clock = pygame.time.Clock()

    # Events are obtained and checked for quit
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(BLACK)

        # Text is blitted onto the screen to show Game Over and score acheived
        my_font = pygame.font.SysFont('Impact', 100)
        TextSurf = my_font.render('Game Over!', False, RED)
        screen.blit(TextSurf, [135, 200])

        my_font2 = pygame.font.SysFont('Impact', 70)
        TextSurf2 = my_font2.render('Success Rate: '+ str(rt), False, WHITE)
        screen.blit(TextSurf2, [135, 300])

        checkPoint += 1

        # Automatically goes into the maze code after a time delay
        if checkPoint == 35:
            intro_screen()

        pygame.display.update()
        clock.tick(20)

# A function is made for the completion of the first level
def congrats():

    checkpoint = 0
    clock = pygame.time.Clock()

    # Writes the scores of the player into a local database

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(congratsImg, [0, 0])

        # Shows text of congradualtions
        my_font = pygame.font.SysFont('Impact', 100)
        TextSurf = my_font.render('Congrats', False, WHITE)
        screen.blit(TextSurf, [135, 200])

        my_font2 = pygame.font.SysFont('Impact', 64)
        TextSurf2 = my_font2.render('Now complete the maze', False, WHITE)
        screen.blit(TextSurf2, [50, 400])

        checkpoint += 1

        # Goes to the main maze after a time delay
        if checkpoint == 30:
            maze.main_maze()

        pygame.display.update()

        clock.tick(20)

# This function writes the score of the user into a local database (text file)
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


# This is a function for the gateway to Level 2
def proceed():

    checkpoint = 0
    clock = pygame.time.Clock()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(gradient, [0, 0])

        # Font for dislaying Level 2 text
        my_font = pygame.font.SysFont('Impact', 100)
        TextSurf = my_font.render('Level 2', False, WHITE)
        screen.blit(TextSurf, [135, 200])

        checkpoint += 1

        # Automatically proceeds to Level 2
        if checkpoint == 30:
            Level2.main()

        pygame.display.flip()

        clock.tick(20)

# The main function is what runs the whole code put together
def main():
    # Main Function

    #Images are put in a list for the player sprite
    images = [pygame.image.load('CQ.png'), pygame.image.load('CR1.png'), pygame.image.load('CR2.png'), pygame.image.load('CR3.png'), pygame.image.load('CR4.png'), pygame.image.load('CR5.png'), pygame.image.load('CR6.png'), pygame.image.load('CR7.png'), pygame.image.load('CR8.png'), pygame.image.load('CR9.png')]

    # Player sprite is defined
    player = Player(position = (340, 530), images = images)

    # Enemy sprites are defined
    enemy = Enemy()
    enemy2 = Enemy()
    enemy3 = Enemy()

    # Coins on the first platform defined
    coin = Coin()
    coin2 = Coin()
    coin3 = Coin()
    # Coins on the second platform defined
    coin4 = Coin()
    coin5 = Coin()
    coin6 = Coin()
    # Coins on the last platform defined
    coin7 = Coin()
    coin8 = Coin()

    # Exit door sprite defined
    door = ExitDoor()

    # A level list is made for Level 1
    level_list = []
    level_list.append(Level_1(player))

    # Level _ now tells the program that it is on level 1
    level_now = level_list[0]

    # A sprite list is made for all sprites
    sprite_list = pygame.sprite.Group()
    player.level = level_now

    #Player's position is given and is added to the sprite_list
    player.rect.x = 340
    player.rect.y = sh - player.rect.height
    sprite_list.add(player)

    #Enemys positions are given and added to the sprite list
    enemy.rect.x = 0
    enemy.rect.y = sh - enemy.rect.height
    sprite_list.add(enemy)
    enx = 5

    enemy2.rect.x = 400
    enemy2.rect.y = 350 - enemy.rect.height
    enemy2.image.fill(MUTATE)
    sprite_list.add(enemy2)
    enx2 = 5

    enemy3.rect.x = 0
    enemy3.rect.y = 220 - enemy.rect.height
    sprite_list.add(enemy3)
    enx3 = 5

    # Coin positioning and appendage to the sprite list
    coin.rect.x = 700
    coin.rect.y = sh - coin.rect.height
    sprite_list.add(coin)

    coin2.rect.x = 600
    coin2.rect.y = sh - coin2.rect.height
    sprite_list.add(coin2)

    coin3.rect.x = 200
    coin3.rect.y = 480 - coin3.rect.height
    sprite_list.add(coin3)

    coin4.rect.x = 450
    coin4.rect.y = 350 - coin4.rect.height
    sprite_list.add(coin4)

    coin5.rect.x = 575
    coin5.rect.y = 350 - coin5.rect.height
    sprite_list.add(coin5)

    coin6.rect.x = 680
    coin6.rect.y = 350 - coin6.rect.height
    sprite_list.add(coin6)

    coin7.rect.x = 100
    coin7.rect.y = 220 - coin7.rect.height
    sprite_list.add(coin7)

    coin8.rect.x = 250
    coin8.rect.y = 220 - coin8.rect.height
    sprite_list.add(coin8)

    #exit Door and added to sprite list
    door.rect.x = 0
    door.rect.y = 220 - door.rect.height
    sprite_list.add(door)

    # Score variable is set
    rate = None

    # Bar width of the health bar is set
    barwidth = 200

    # A caption for the display is also set
    pygame.display.set_caption('Dungeon Dweller Game')

    game = False

    ### MAIN LOOP ###
    while not game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = True

            # Checks events for key presses or releases and moves the player accordingly
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

        # Blits the wallpaper of the screen
        screen.blit(jungle, [0, 0])

        # Updates eveything in the sprite list
        sprite_list.update()

        # Updates the current level (1)
        level_now.update()

        # Shows the health bar
        healthBar(barwidth)

        #Gets the success rate
        rate = int((barwidth / 200) * 100)

        # Displays the success rate
        gameScoreDisplay(rate)

        # Enemy movement
        enemy.rect.x += enx
        enemy2.rect.x += enx2
        enemy3.rect.x += enx3

        #Defnining Enemy Boundaries and changes direction accordingly
        if enemy.rect.right > sw:
            enx = -5
        elif enemy.rect.left <= 0:
            enx = 5

        if enemy2.rect.right >= 700:
            enx2 = -5
        elif enemy2.rect.left <= 400:
            enx2 = 5

        if enemy3.rect.right >= 400:
            enx3 = -5
        elif enemy3.rect.left <= 0:
            enx3 = 5

        # Checks for the collisions between the player and the enemy
        if player.rect.colliderect(enemy):
            barwidth -= 4

        if player.rect.colliderect(enemy2):
            barwidth -= 4

        if player.rect.colliderect(enemy3):
            barwidth -= 4

        #Collisions with the coin and the player
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

        # Collision witht the door and the player
        if player.rect.colliderect(door):
            if coin.rect.x > 800 and coin2.rect.x > 800 and coin3.rect.x > 800 and coin4.rect.x > 800 and coin5.rect.x > 800 and coin6.rect.x > 800 and coin7.rect.x > 800 and coin8.rect.x > 800:
                congrats()
            else:
                player.rect.x = door.rect.right


        # Setting player boundaries
        if player.rect.right > sw:
            player.rect.right = sw

        if player.rect.left < 0:
            player.rect.left = 0

        # Checking when it is game over
        if barwidth <= 0:
            gameOver()

        #Check to see if there are collisions between the slime blob and the character
        #hits = pygame.sprite.spritecollide(enemy, player, True, True)

        # Draws all sprites and level into the screen
        level_now.draw(screen)
        sprite_list.draw(screen)

        # Sets FPS rate for the game
        clock.tick(60)
        pygame.display.update()

    # Quits pygame and the python program
    pygame.quit()
    quit()

# Acts as a measure to run the main program if the following is according
if __name__ == "__main__":
    intro_screen()
