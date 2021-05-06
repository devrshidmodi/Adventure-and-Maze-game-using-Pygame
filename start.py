

def intro_screen():

    background = pygame.Surface(size)
    background = background.convert()
    background = pygame.image.load("startscreen.jpg")

    gray = (140,140,145)
    light_gray = (190,190,200)
    white = (255,255,255)

    button1 = pygame.Rect(100,100,150,25)
    button2 = pygame.Rect(100,200,150,25)
    button3 = pygame.Rect(100,300,150,25)
    button4 = pygame.Rect(100,400,150,25)

    my_font = pygame.font.SysFont("comicsansms", 48)
    my_font2 = pygame.font.SysFont("opensans",30)
    label = my_font.render("Dungeon Dweller", True, white)
    Play = my_font2.render("Play", True, white)
    Instructions = my_font2.render("Instructions", True, white)
    Credits = my_font2.render("Credits", True, white)
    Quit = my_font2.render("Quit", True, white)

    screen.blit(background, (0,0))
    screen.blit(label, (250, 20))

    timer = pygame.time.Clock()

    sets = True
    while sets:
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = e.pos

                if button1.collidepoint(mouse_pos):
                    #print("Play")
                    main1.starteverything()
                elif button2.collidepoint(mouse_pos):
                    print("Instructions")
                elif button3.collidepoint(mouse_pos):
                    print("Credits")
                elif button4.collidepoint(mouse_pos):
                    print("Quit")

            must = pygame.mouse.get_pos()

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

        screen.blit(Play, (150,100))
        screen.blit(Instructions, (112,200))
        screen.blit(Credits, (140,300))
        screen.blit(Quit, (150,400))


        pygame.display.update()
