import pygame
import time

res = (640,480)
screen = pygame.display.set_mode(res,pygame.RESIZABLE)

timer = pygame.time.Clock()
erreur = 0
launched = True
jeu_en_cours = 0
blue_clair = (173,216,230)
red_color = (255,0,0)
rose_color= (255, 40, 193)
green_color = (0,255,0)
black_color = (0,0,0)
white_color = (255,255,255)
x_debut = 100
y_debut = 200
speeddebut_x = 5
speeddebut_y = 5
x_rect = 120
y_rect = 200
speed_x = 5
speed_y = 5
carre_debut = pygame.Rect(x_debut,y_debut,20,20)
player = pygame.Rect(x_rect,y_rect,20,20)
button = pygame.Rect(240,300,145,50)
button2 = pygame.Rect(240,300,145,50)
mur = pygame.Rect(0,0,640,10)
mur2 = pygame.Rect(0,470,640,10)
mur3 = pygame.Rect(0,0,10,480)
mur4 = pygame.Rect(630,0,10,480)
mur5 = pygame.Rect(20,40,10,400)
mur6 = pygame.Rect(600,40,10,400)
pygame.mixer.init()
DTF100_song = pygame.mixer.Sound("C:\\Users\\David\\Desktop\\Nouveau dossier\\pygames\\monkey_song.mp3")
DTF100_song.play()
start_time = time.time()
obstacles = [
    pygame.Rect(92,370,50,20),
    pygame.Rect(423,128,30,30),
    pygame.Rect(564,310,20,80),
    pygame.Rect(325,200,15,50),
    pygame.Rect(340,200,25,15),
    pygame.Rect(285,356,40,15),
    pygame.Rect(325,356,15,60),
    pygame.Rect(340,356,40,15),
    pygame.Rect(540,35,50,15),
    pygame.Rect(575,50,15,50),
    pygame.Rect(80,80,60,15),
    pygame.Rect(140,80,15,60),
    pygame.Rect(155,125,40,15),
    pygame.Rect(337,29,20,79),
    pygame.Rect(490,235,60,15),
    pygame.Rect(75,200,15,79)
]

def draw_hearts():
    if erreur < 1:
      pygame.draw.circle(screen, rose_color, (35, 40), 5)
      pygame.draw.circle(screen, rose_color, (45, 40), 5)  
      pygame.draw.polygon(screen, rose_color, [(30, 40), (50, 40), (40, 50)])
      pygame.draw.circle(screen, rose_color, (75, 40), 5)
      pygame.draw.circle(screen, rose_color, (85, 40), 5)  
      pygame.draw.polygon(screen, rose_color, [(70, 40), (90, 40), (80, 50)])
      pygame.draw.circle(screen, rose_color, (115, 40), 5)
      pygame.draw.circle(screen, rose_color, (125, 40), 5)  
      pygame.draw.polygon(screen, rose_color, [(110, 40), (130, 40), (120,50)])
      pygame.display.flip()
    if erreur < 2:
      pygame.draw.circle(screen, rose_color, (75, 40), 5)
      pygame.draw.circle(screen, rose_color, (85, 40), 5)  
      pygame.draw.polygon(screen, rose_color, [(70, 40), (90, 40), (80, 50)])
      pygame.draw.circle(screen, rose_color, (115, 40), 5)
      pygame.draw.circle(screen, rose_color, (125, 40), 5)  
      pygame.draw.polygon(screen, rose_color, [(110, 40), (130, 40), (120,50)])
      pygame.display.flip()
    if erreur < 3:
      pygame.draw.circle(screen, rose_color, (115, 40), 5)
      pygame.draw.circle(screen, rose_color, (125, 40), 5)  
      pygame.draw.polygon(screen, rose_color, [(110, 40), (130, 40), (120,50)])
      pygame.display.flip()
      
def demarrage():
    global x_debut, speeddebut_x
    screen.fill(black_color)
    pygame.draw.rect(screen,green_color,button)
    arial_text = pygame.font.SysFont("arial",40,False,True) #(nom de la police,taille,gras=True,italic=True)
    texte1 = arial_text.render("The Game", True,white_color) #("texte",True,couleur)
    screen.blit(texte1,[220,100])
    arial_text = pygame.font.SysFont("arial",40,False,True) #(nom de la police,taille,gras=True,italic=True)
    texte1 = arial_text.render("START", True,white_color) #("texte",True,couleur)
    screen.blit(texte1,[245,300])
    pygame.draw.rect(screen,red_color,carre_debut)
    pygame.draw.rect(screen,blue_clair,mur5)
    pygame.draw.rect(screen,blue_clair,mur6)
    x_debut += speeddebut_x
    carre_debut.topleft = (x_debut,y_debut)
    if carre_debut.colliderect(mur5) or carre_debut.colliderect(mur6):
       speeddebut_x = -speeddebut_x
    pygame.display.flip()


def restart():
    global x_debut, speeddebut_x
    screen.fill(black_color)
    pygame.draw.rect(screen,green_color,button2)
    arial_text = pygame.font.SysFont("arial",50,False,True) #(nom de la police,taille,gras=True,italic=True)
    texte1 = arial_text.render("SORRY...", True,white_color) #("texte",True,couleur)
    screen.blit(texte1,[210,100])
    arial_text = pygame.font.SysFont("arial",30,False,True) #(nom de la police,taille,gras=True,italic=True)
    texte1 = arial_text.render("RESTART", True,white_color) #("texte",True,couleur)
    screen.blit(texte1,[245,300])
    pygame.draw.rect(screen,red_color,carre_debut)
    pygame.draw.rect(screen,blue_clair,mur5)
    pygame.draw.rect(screen,blue_clair,mur6)
    x_debut += speeddebut_x
    carre_debut.topleft = (x_debut,y_debut)
    if carre_debut.colliderect(mur5) or carre_debut.colliderect(mur6):
       speeddebut_x = -speeddebut_x
    pygame.display.flip()

def begin():
  global launched,jeu_en_cours,x_rect,y_rect,speed_x,speed_y,erreur,screen
  while launched:
    pygame.init()
    pygame.display.set_caption("Mon programme pygame") 
    for event in pygame.event.get():
          if event.type == pygame.QUIT:
              launched = False
          elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if button.collidepoint(pos) or button2.collidepoint(pos):
              erreur = 0
              jeu_en_cours = 1
              
    if jeu_en_cours == 0:
        demarrage()
    if jeu_en_cours == 1:
      draw_hearts()
      if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_UP:
                speed_y = 5.5
                speed_y = -speed_y
                speed_x = 0
          if event.key == pygame.K_DOWN:
                speed_y = 5.5
                speed_y = speed_y
                speed_x = 0
          if event.key == pygame.K_LEFT:
                speed_x = 5.5
                speed_x = -speed_x
                speed_y = 0
          if event.key == pygame.K_RIGHT:
                speed_x = 5.5
                speed_x = speed_x
                speed_y = 0
          if event.key == pygame.K_SPACE:
                speed_y = 0
                speed_x = 0
          if event.key == pygame.K_c:
                pygame.mixer.pause()  #mise en pause
          if event.key == pygame.K_p:
                pygame.mixer.unpause()  #relecture

      x_rect += speed_x
      y_rect += speed_y
      player.topleft = (x_rect,y_rect)

      if player.colliderect(mur) or player.colliderect(mur2) or player.colliderect(mur3) or player.colliderect(mur4):
        speed_y = -speed_y
        speed_x = -speed_x

      for obs in obstacles:
          if player.colliderect(obs):
              speed_y = -speed_y
              speed_x = -speed_x
              erreur += 1

      screen.fill(black_color)
      arial_text = pygame.font.SysFont("arial",40,False,True) #(nom de la police,taille,gras=True,italic=True)
      texte1 = arial_text.render("The Game", True,white_color) #("texte",True,couleur)
      screen.blit(texte1,[220,100])
      pygame.draw.rect(screen,red_color,player)
      pygame.draw.rect(screen,blue_clair,mur)
      pygame.draw.rect(screen,blue_clair,mur2)
      pygame.draw.rect(screen,blue_clair,mur3)
      pygame.draw.rect(screen,blue_clair,mur4)
      for obs in obstacles:
          pygame.draw.rect(screen, blue_clair, obs)
      
      pygame.display.flip()
      print(erreur)

      if erreur == 3:
        jeu_en_cours = 2
        

      timer.tick(60)

    if jeu_en_cours == 2:
        restart()

  pygame.quit()

if __name__ == "__main__":
    begin()


"""  
    if (time.time() - start_time) >= 1:
       largeur += 5
       player.width = largeur
       start_time = time.time() #en vrai c'est nul mais c'est juste pour melanger avec pygame avec time
"""