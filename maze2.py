import pygame
import mainapp

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 255, 0)

sw = 800
sh = 600

screen = pygame.display.set_mode([sw, sh])

clock = pygame.time.Clock()

background = pygame.image.load("shotbackground.png")
treasure = pygame.image.load("Treasure.png")
complete = pygame.image.load('complete.png')

class Guy(pygame.sprite.Sprite):

    def  __init__(self):

        super().__init__()

        pygame.sprite.Sprite.__init__(self)

        width = 50
        height = 50
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()

        self.velx = 0
        self.vely = 0

    def update(self):

        self.rect.x += self.velx

        bump_list = pygame.sprite.spritecollide(self, self.maze.stage_list, False)
        for block in bump_list:
            if self.velx > 0:
                self.rect.right = block.rect.left
            elif self.velx < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.vely

        bump_list = pygame.sprite.spritecollide(self, self.maze.stage_list, False)
        for block in bump_list:
            if self.vely > 0:
                self.rect.bottom = block.rect.top
            elif self.vely < 0:
                self.rect.top = block.rect.bottom

    def leftMovement(self):

        self.velx = -5

    def rightMovement(self):

        self.velx = 5

    def upMovement(self):

        self.vely = -5

    def downMovement(self):

        self.vely = 5

    def stop(self):

        self.velx = 0
        self.vely = 0

class Treasure(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        pygame.sprite.Sprite.__init__(self)

        width = 60
        height = 58
        self.image = treasure

        self.rect = self.image.get_rect()


class Stage(pygame.sprite.Sprite):

    def __init__(self, width, height):

        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()


class Maze:

    def __init__(self, guy):

        self.stage_list = pygame.sprite.Group()
        self.guy = guy

        self.background = None

    def update(self):

        self.stage_list.update()

    def draw(self, screen):

        self.stage_list.draw(screen)


class Maze_1(Maze):

    def __init__(self, guy):

        Maze.__init__(self, guy)

        # List containing the width, height, x position and y position of the platform
        maze = [[20, 475, 160, 0],
                 [20, 370, 320, 125],
                 [20, 320, 480, 0],
                 [20, 475, 640, 275],
                 [160, 20, 160, 475],
                 [160, 20, 480, 475],
                 [180, 20, 480, 125],
                 [70, 20, 730, 400]
                 ]

        #Go through the array and add the platform blocks
        for stage in maze:
            block = Stage(stage[0], stage[1])
            block.rect.x = stage[2]
            block.rect.y = stage[3]
            block.player = self.guy
            self.stage_list.add(block)

def completion():

    checkPoint = 0
    clock = pygame.time.Clock()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(complete, [0, 0])

        font = pygame.font.SysFont('Impact', 52)
        TextSurf = font.render('You Have Completed The Game!', False, ORANGE)
        screen.blit(TextSurf, [50, 200])

        checkPoint += 1

        if checkPoint == 35:
            mainapp.intro_screen()

        pygame.display.flip()
        clock.tick(20)

def main_maze():

    guy = Guy()
    treasure = Treasure()

    maze_list = []
    maze_list.append(Maze_1(guy))

    current_maze = maze_list[0]

    sprites = pygame.sprite.Group()
    guy.maze = current_maze

    guy.rect.x = 0
    guy.rect.y = 50 - guy.rect.height
    sprites.add(guy)

    treasure.rect.x = sw - treasure.rect.width
    treasure.rect.y = sh - treasure.rect.height
    sprites.add(treasure)

    pygame.display.set_caption("The Maze")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    guy.leftMovement()
                elif event.key == pygame.K_RIGHT:
                    guy.rightMovement()
                elif event.key == pygame.K_UP:
                    guy.upMovement()
                elif event.key == pygame.K_DOWN:
                    guy.downMovement()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and guy.velx < 0:
                    guy.stop()
                elif event.key == pygame.K_RIGHT and guy.velx > 0:
                    guy.stop()
                elif event.key == pygame.K_UP and guy.vely < 0:
                    guy.stop()
                elif event.key == pygame.K_DOWN and guy.vely > 0:
                    guy.stop()

        screen.blit(background, [0, 0])

        sprites.update()

        current_maze.update()

        if guy.rect.right > sw:
            guy.rect.right = sw

        if guy.rect.left < 0:
            guy.rect.left = 0

        if guy.rect.bottom > sh:
            guy.rect.bottom = sh

        if guy.rect.top < 0:
            guy.rect.top = 0


        if guy.rect.colliderect(treasure):
            treasure.rect.x = 810
            completion()


        current_maze.draw(screen)
        sprites.draw(screen)


        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    main_maze()
