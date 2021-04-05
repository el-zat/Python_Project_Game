import pygame
import random
from tkinter import *

from bird import Bird
from module_1 import Top, Bottom, Worm

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')
HG = pygame.transform.scale(pygame.image.load( "images/background.png"), (WIDTH, HEIGHT))

leaderboard_scores = [0, 0, 0]
leaderboard_names = ["NOBODY", "NOBODY", "NOBODY"]
        
def run_game():
    """
    contains main loop to play the game
    defines and initilizes object attributes and parameters
    calls other programme functions
    controls the bird,pipes and worm movement
    defines and stores game statistics
    -----------------
    return: none
    """
    run = True
    FPS = 60    # Frames per second
    
    #Properties of the Bird
    bird = Bird(380, 400)
    bird_vel = 4
    bird_jump = 15
    pipe_vel = 5
    
    # Properties of the pipes
    pipes_bottom = []
    pipes_top = []
    pipes_counter = 100
    
    # game statistics
    score = 0
    uni_font = pygame.font.SysFont("comicsans", 50)
    lives = 5
    worm_vel = 2
    worms = []
    worms_counter = 100
    würmer = 0
  
    clock = pygame.time.Clock() # Erfasst die aktuelle der Systemzeit
        
    def redraw_windows():
        """ 
        updates the window and displays initial gamestatistics
        -----------
        return: none
        """
        WIN.blit(HG,(0,0))
        score_label = uni_font.render(f"Score: {score}", 1, (255,255,255))
        lives_label = uni_font.render(f"Lives: {lives}", 1 ,(255,255,255))
        worm_label = uni_font.render(f"Worms: {würmer}", 1 ,(255,255,255))
        
        # call object method from module_1
        for worm in worms:
            worm.draw(WIN)
        for pipe in pipes_bottom:
            pipe.draw(WIN)
        for pipe in pipes_top:
            pipe.draw(WIN)
            
        # display objects on the window    
        WIN.blit(score_label, (10,10))
        WIN.blit(lives_label, (10,50))
        WIN.blit(worm_label, (10,90))
        
        bird.draw(WIN)
        
        pygame.display.update()
    
        
    while run:        
        clock.tick(FPS)    #legt Wiederholsgeschwindikeit fest des Programmes fest
        redraw_windows()
        bird.move(bird_vel) 
        
        if len(pipes_bottom) == 0:
            for i in range(0, pipes_counter): 
                xt = random.randrange(0, 250) # generiert eine zufällige Nummer zwischen 0 und 250
                                              # die, die vertikalen position des Rohres beinflusst.
                bottom = Bottom(1200 + i*300, 400 + xt)
                pipes_bottom.append(bottom)
                top = Top(1200 + i*300, -300 + xt)  # Die Differenz der beiden Y-Positionen (400 , -300) 
                                                    # bestimmt die Größe der Lücke zwischen den Rohren
                pipes_top.append(top)
              
        for bottom in pipes_bottom[:]:
            bottom.move(pipe_vel)
            # Da die List in den folgenden Kontrollstrukturen verändert wird, muss mit einer "shallow"-Copie der Liste gearbeite werden
            
            if bottom.x < -100: # wenn sich das "bottom_pipe" in eine negativen Lage befindet (links neben dem Bildschrimm befindet):
                pipes_bottom.remove(bottom)
                score += 10 # und erhöht den Score um 10 Punkten
            elif bird.collide(bottom): # wenn das "bottom_pipe" und "bird" kollidieren: 
                pipes_bottom.remove(bottom) # löscht das aktuelle kollidierende rohr 
                lives -= 1
                          
        for top in pipes_top[:]: # identisches Vorgehenweise wie "pipes_bottom"
            top.move(pipe_vel)
            
            if top.x < -100:
                pipes_top.remove(top)
                score += 10
            elif bird.collide(top):
                pipes_top.remove(top)
                lives -= 1
                             
        if len(worms) == 0: # identisches Vorgehenweise wie "pipes_bottom"
            for i in range(0, worms_counter):
                xt = random.randrange(-300, 650)
                worm = Worm(600 + i*300,  xt)
                worms.append(worm)
                
        for worm in worms[:]:
            worm.move(worm_vel)
            
            if worm.x < -100:
                worms.remove(worm)
            elif bird.collide(worm):
                worms.remove(worm)
                score += 25
                würmer += 1
                if würmer % 3 == 0 :
                    lives += 1                    
                
        keys = pygame.key.get_pressed() # Welche aktionen gehören zu welcher Taste
        if (keys[pygame.K_SPACE] or bird.y + bird_vel + 30 > HEIGHT) and (bird.y - bird_jump >= 0): 
            bird.y -= bird_jump       
        # "pygame.key.get_pressed()":  Hier erhält einen booleschen Werte, welcher den Status der zu überprüfende Taste repräsentiert
                                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()                
        # "pygame.event.get()": Überprüft eine Liste mit möglichen "Events" (z.B klicken auf Schließsymbols)
        # ist ein Event eingetretten ergibt dies True
    
                        
        if lives < 0:
            run = False
            
            lost_label = uni_font.render("you are a LOSER!!", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 400)) 
            pygame.display.update()

            fenster = Tk()
            fenster.geometry("200x200")
            fenster.title("Whats your name?")
            label = Label(fenster, text="Whats your name?")
            label.pack()
            eingabe = Entry(fenster)
            eingabe.pack()
            
            XPOS = 855
            YPOS = 300
            fenster.geometry("+%d+%d" % (XPOS, YPOS))

            def lesen():
                """
                Der Spieler kann hier seinen Namen eingeben
                """
                global name 
                name = eingabe.get()
                fenster.destroy()
                
            knopf1 = Button(fenster, text="submit", command=lesen)
            knopf1.pack()
            fenster.mainloop()
            
            create_leader_board(score, name)
  
def create_leader_board(score, name):
    """
    creates and stores game statistics
    shows the three highest scores since the game was started
    if latest score is higher than the smallest score in highest 
    it removes the smalles highscore value and stores the latest score in the highscores list
    return:none
    """
    run = True
    title_font = pygame.font.SysFont("comicsans", 50)
    highscore_font = pygame.font.SysFont("comicsans", 150 )
    
    if score >= min(leaderboard_scores):
        leaderboard_scores.append(score)

    leaderboard_scores.sort(reverse = True)

    for counter, value in enumerate(leaderboard_scores):
        if value == score:
            leaderboard_names.insert(counter, name)
            break

    leaderboard_scores.pop() 
    leaderboard_names.pop() 
    
    while run:
        
        WIN.blit(HG, (0,0))
        
        highscore_label = highscore_font.render("Highscores", 1, (255,255,255))
        score_1 = title_font.render(f"1. Platz: {leaderboard_names[0]} mit {leaderboard_scores[0]} Punkte", 1, (255,255,255))
        score_2 = title_font.render(f"2. Platz: {leaderboard_names[1]} mit {leaderboard_scores[1]} Punkte", 1, (255,255,255)) 
        score_3 = title_font.render(f"3. Platz: {leaderboard_names[2]} mit {leaderboard_scores[2]} Punkte", 1, (0,0,0))
        return_label = title_font.render("press ENTER to return to the main menu", 1, (255,255,255))
        WIN.blit(highscore_label, (WIDTH/2 - highscore_label.get_width()/2, 100))
        WIN.blit(score_1, (WIDTH/2 - score_1.get_width()/2, 350))
        WIN.blit(score_2, (WIDTH/2 - score_2.get_width()/2, 450))
        WIN.blit(score_3, (WIDTH/2 - score_3.get_width()/2, 550))
        WIN.blit(return_label, (WIDTH/2 - return_label.get_width()/2, 700))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()              
            if keys[pygame.K_RETURN]:
                show_main_menu()
                run = False
                
    pygame.quit()    
    
def show_main_menu():
    """
    display inital game window, shows labels and titles
    return: none
    """
    run = True
    title_font = pygame.font.SysFont("comicsans", 50)
    big_title_font = pygame.font.SysFont("comicsans", 135)
    design_font = pygame.font.SysFont("comicsans", 25)
    
    while run:
        WIN.blit(HG, (0,0))
        
        big_title_label = big_title_font.render("THE BIRD GAME", 1, (255,255,255))
        title_label = title_font.render("for Start press SPACE", 1, (255,255,255))

        
        WIN.blit(big_title_label, (WIDTH/2 - big_title_label.get_width()/2, 200))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 400))

        pygame.display.update()
        
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()              
            if keys[pygame.K_SPACE]:
                run_game()
                
    pygame.quit()

show_main_menu() 

