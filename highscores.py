# Devrshi Modi, Raghu Alluri
# June 16th, 2020
# This program gets the highscores from the database and prints them into pygame screen

import pygame
import mainapp

#Initializes pygame
pygame.init()

#Setting important colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 255, 0)

#Gets screen dimensions
sw = 800
sh = 600

#Makes a pygame screen
screen = pygame.display.set_mode([sw, sh])
pygame.display.set_caption("High Scores")
clock = pygame.time.Clock()

#makes a back button for the instructions screen
def backButton(bc):

    pygame.draw.rect(screen, bc, [650, 500, 100, 50])

    text = pygame.font.SysFont('Arial', 40)
    TextSurf = text.render('Back', False, BLACK)
    screen.blit(TextSurf, [650, 500])

# gets the high scores from the database and blits it onto pygame
def displayHighScores(ny):

    # opening file and storing data in a variable
    file = open('gamescores.txt', 'r')
    scores = file.readline()
    file.close()

    # Sorting the list from highest number to the lowest number
    this_score = scores.split(',')
    new_scores = sorted(this_score, reverse = True)

    # Checking the length of the sorted list
    length = len(new_scores)

    # Making sure that the program only gets the top 3 scores
    if length > 4:
        length = 4

    # blits the top 3 ranking onto the pygame screen
    for i in range(length - 1):

        text = pygame.font.SysFont('Impact', 48)
        TextSurf = text.render(str(i + 1) + ': ' + str(new_scores[i]), False, BLACK)
        screen.blit(TextSurf, [330, 150 + ny])

        # ny is to be used as a spacer between the two rankings
        ny += 48

# Title of the screen is made into a function
def title():

    text = pygame.font.SysFont('Impact', 72)
    TextSurf = text.render('HighScores', False, BLACK)
    screen.blit(TextSurf, [228, 0])

# ________________ Main _____________________
def main_scores():

    button_color = WHITE

    spacey = 0

    # MAIN LOOP
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Defines cursor position and the clicked position
        cursor = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()

        #Fills the screen color
        screen.fill(RED)

        #Calls all functions needed for the program
        title()
        backButton(button_color)
        displayHighScores(spacey)

        # Highlights the bakc button when mouse is hovered on top
        if 650 < cursor[0] < 750 and 500 < cursor[1] < 550:
            button_color = ORANGE
            if clicked[0] == 1:
                mainapp.intro_screen()
        else:
            button_color = WHITE

        # Pygame display is updated
        pygame.display.update()

        # FPS rate is made
        clock.tick(30)

# Runs the __main__scores based on the equality of the if statement
if __name__ == "__main__":
    main_scores()
