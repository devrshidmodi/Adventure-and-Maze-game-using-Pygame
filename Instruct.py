def main_instructor():

    WHITE = (255,255,255)
    PINK = (255,0,72)

    sw=800
    sh=600

    screen = py.display.set_mode((sw,sh))
    py.display.set_caption("Instructions 1")

    background_image = py.image.load("forestcave1.png")

    def textx():
        buttonx=py.draw.rect(screen,PINK,[650,500,100,50])
        myfont=py.font.SysFont("Impact",40)
        TextSurf=myfont.render("Next",False,WHITE)
        screen.blit(TextSurf,[650,500])

    def text1():
        myfont=py.font.SysFont("Impact",40)
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
        for event in py.event.get():
            if event.type == py.QUIT:
                crashed = True

        cursor = py.mouse.get_pos()
        clicked = py.mouse.get_pressed()

        screen.blit(background_image , [0 , 0])

        if 650 < cursor[0] < 750 and 500 < cursor[1] < 550:
            if clicked[0] == 1:
                dhokla()

        text1()
        textx()
        py.display.update()



def dhokla():
    def BACKTEXT():
        buttonx=py.draw.rect(screen,PINK,[150,500,100,50])
        myfont=py.font.SysFont("Impact",40)
        TextSurf=myfont.render("BACK",False,WHITE)
        screen.blit(TextSurf,[150,500])
    def text2():
        myfont=py.font.SysFont("Impact",25)
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
        for devrshi in py.event.get():
            if devrshi.type == py.QUIT:
                py.quit()
                quit()

        screen.blit(background_image, (0, 0))
        text2()
        BACKTEXT()
        py.display.flip()

py.quit()
quit()
