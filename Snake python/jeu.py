  
#from pygame import display, event, init, key, font, time
import pygame
from pygame.locals import *
from pygame.draw import circle, line
from math import cos, sin, pi
from random import randint
from os import popen

def getSystemResolutionOnLinux():
 screen = popen("xrandr -q -d :0").readlines()[0]
 tmp = screen.split()
 return int( tmp[7] ), int( tmp[9][:-1] )

def create_points(bg, pc, modulo):
 dtheta = 2 * pi / modulo
 alpha = 0
 
 for i in range(modulo):
  alpha = dtheta * i
  pc[i] = [ POS_CIRCLE[X] + int( R * sin(alpha) ) , POS_CIRCLE[Y] - int( R * cos(alpha) ) ]
  if ( i + 1 ) % ( modulo // 51 + 1 ) == 0 :#pour aérer le dessin (+ beau)
   circle(bg, BROWN, pc[i], R_, 0)
  
def create_texts(bg, texts, pos_texts, pc, modulo):
 dtheta = 2 * pi / modulo
 alpha = 0
 
 for i in range(modulo):
  if ( i + 1 ) % ( modulo // 51 + 1 ) == 0 :#pour aérer le dessin (+ beau)
   alpha = dtheta * i
   pos_texts[i].centerx = pc[i][X] + int( EPS * sin(alpha) )
   pos_texts[i].centery = pc[i][Y] - int( EPS * cos(alpha) )
   
   bg.blit(texts[i], pos_texts[i])

def create_lines(bg, pc, table, modulo):
 x = 0.0
 for i in range(modulo):
  x = table * i
  x %= modulo
  
  line(bg, GREEN, pc[i], pos_arriv(x, float(modulo)), 1)
  
def pos_arriv(b, modulo):
 x = float(POS_CIRCLE[X]) + R * sin( b / modulo * 2 * pi )
 y = float(POS_CIRCLE[Y]) - R * cos( b / modulo * 2 * pi )
 
 return ( int(round(x)) , int(round(y)) )
  
def init(texts, pos_texts, textsPara, pos_textsPara, pos_circles, font, modulo, tps, type_var, pause, var):
 textsPara += [ font.render( "variable : " + str(TYPE_VAR[type_var]), 1, BLACK) ]
 textsPara += [ font.render( "pause = " + str(pause), 1, BLACK) ]
 textsPara += [ font.render( "f = " + str( 1 / tps[DELAY][type_var] * 1e3 ) + " Hz", 1, BLACK) ]
 textsPara += [ font.render( "sens : " + str(SENS[var]), 1, BLACK) ]
 for i in range(len(textsPara)) :
  pos_textsPara += [ textsPara[i].get_rect() ]
  pos_textsPara[i].x = 0.02 * WIDTH_SC
  pos_textsPara[i].y = ( 0.02 + i * 0.05 ) * HEIGH_SC
 for i in range(modulo):
  pos_circles += [ [0,0] ]
  texts += [ font.render(str(i), 1, BLACK) ]
  pos_texts += [ texts[i].get_rect() ]
  pos_texts[i].centerx = 0
  pos_texts[i].centery = 0
  
def reinit(texts, pos_texts, pos_circles, font, modulo):
 if len(pos_circles) < modulo:
  pos_circles += [ [0,0] ]
  texts += [ font.render(str(len(texts)), 1, BLACK) ]
  pos_texts += [ texts[-1].get_rect() ]
  pos_texts[-1].centerx = 0
  pos_texts[-1].centery = 0
 else:
  pos_circles = pos_circles[:-1]
  texts = texts[:-1]
  pos_texts = pos_texts[:-1]
 
def reinitFont(bg, text_title, textpos, texts, font, table, modulo):
 text_title = font.render("Table de " + str(table) + " modulo " + str(modulo), 1, BLACK)
 textpos = text_title.get_rect()
 textpos.centerx = bg.get_rect().centerx
 textpos.centery = bg.get_rect().centery
 bg.fill(WHITE)
 bg.blit(text_title, textpos)
 
def reinitFontPara(bgFont, textsPara, pos_textsPara, font, tps, type_var, pause, var):
 textsPara[0] = font.render( "variable : " + str(TYPE_VAR[type_var]), 1, BLACK)
 textsPara[1] = font.render( "pause = " + str(pause), 1, BLACK)
 textsPara[2] = font.render( "f = " + str( 1 / tps[DELAY][type_var] * 1e3 ) + " Hz", 1, BLACK)
 textsPara[3] = font.render( "sens : " + str(SENS[var]), 1, BLACK)
 bgFont.fill(WHITE)
 for i in range(len(textsPara)) :
  bgFont.blit(textsPara[i], pos_textsPara[i])

def main():
 #init var
 table = randint(20,500) * 10e-1
 modulo = randint(100,119)
 start = True
 pos_circles = []
 texts = []
 textsPara = []
 pos_texts = []
 pos_textsPara = []
 tps = [ 0.0 , 0.0 , [ 20.0 , 100.0 ] ]
 pause = False
 var = INCREASE
 type_var = MODULO
 
 # Initialisation de la fenêtre d'affichage
 pygame.init()
 screen = pygame.display.set_mode((WIDTH_SC, HEIGH_SC))
 pygame.display.set_caption("Dessiner les tables de multiplication")
 pygame.key.set_repeat (500, 30)

 # Remplissage de l'arrière-plan
 bg = pygame.Surface(screen.get_size())
 bg.fill(WHITE)
 
 # Remplissage de l'arrière-plan font
 bgFont = pygame.Surface((WIDTH_SC * 0.22, HEIGH_SC * 0.22))
 bgFont.fill(WHITE)

 # Affichage d'un texte
 font = pygame.font.SysFont("arial", FONT_SIZE)
 text_title = font.render("Table de " + str(table) + " modulo " + str(modulo), 1, BLACK)
 textpos = text_title.get_rect()
 textpos.centerx = bg.get_rect().centerx
 textpos.centery = bg.get_rect().centery
 bg.blit(text_title, textpos)
 
 init(texts, pos_texts, textsPara, pos_textsPara, pos_circles, font, modulo, tps, type_var, pause, var)
 reinitFontPara(bgFont, textsPara, pos_textsPara, font, tps, type_var, pause, var)

 # Boucle d'évènements
 while 1:
  tps[PRES] = pygame.time.get_ticks()
  for event in pygame.event.get():
   if event.type == pygame.QUIT:
    exit()
   elif event.type == KEYDOWN and (event.unicode == 'x' or event.unicode == 'X') and 1 < modulo:
    modulo -= 1
    reinitFont(bg, text_title, textpos, texts, font, table, modulo)
    reinit(texts, pos_texts, pos_circles, font, modulo)
    start = True
   elif event.type == KEYDOWN and (event.unicode == 'c' or event.unicode == 'C'):
    modulo += 1
    reinitFont(bg, text_title, textpos, texts, font, table, modulo)
    reinit(texts, pos_texts, pos_circles, font, modulo)
    start = True
   elif event.type == KEYDOWN and (event.unicode == 'q' or event.unicode == 'Q'):
    table -= 1.0
    reinitFont(bg, text_title, textpos, texts, font, table, modulo)
    start = True
   elif event.type == KEYDOWN and ( event.unicode == 's' or event.unicode == 'S' ) :
    table -= 0.01
    reinitFont(bg, text_title, textpos, texts, font, table, modulo)
    start = True
   elif event.type == KEYDOWN and ( event.unicode == 'd' or event.unicode == 'D' ) :
    table += 0.01
    reinitFont(bg, text_title, textpos, texts, font, table, modulo)
    start = True
   elif event.type == KEYDOWN and (event.unicode == 'f' or event.unicode == 'F'):
    table += 1.0
    reinitFont(bg, text_title, textpos, text, font, table, modulo)
    start = True
   elif ( event.type == MOUSEBUTTONDOWN and event.button == MB_MIDDLE ) or ( event.type == KEYDOWN and event.key == K_SPACE ) :
    if pause:
     pause = False
    else:
     pause = True
    reinitFontPara(bgFont, textsPara, pos_textsPara, font, tps, type_var, pause, var)
    start = True
   elif ( event.type == MOUSEBUTTONDOWN and event.button == MB_RIGHT ) or ( event.type == KEYDOWN and event.key == K_BACKSPACE ) :
    if var:
     var = DECREASE
    else:
     var = INCREASE
    reinitFontPara(bgFont, textsPara, pos_textsPara, font, tps, type_var, pause, var)
    start = True
   elif ( event.type == MOUSEBUTTONDOWN and event.button == MB_LEFT ) or ( event.type == KEYDOWN and ( event.unicode == 't' or event.unicode == 'T' ) ) :
    if type_var == TABLE :
     type_var = MODULO
    else:
     type_var = TABLE
    reinitFontPara(bgFont, textsPara, pos_textsPara, font, tps, type_var, pause, var)
    start = True
   elif ( event.type == MOUSEBUTTONDOWN and event.button == MBSW_UP ) :#ajout d'un hertz
    if 10.1 < tps[DELAY][type_var] :
     tps[DELAY][type_var] = tps[DELAY][type_var] / ( 1.0 + tps[DELAY][type_var] * 1e-3 )
    reinitFontPara(bgFont, textsPara, pos_textsPara, font, tps, type_var, pause, var)
    start = True
   elif ( event.type == MOUSEBUTTONDOWN and event.button == MBSW_DOWN ) :
    if tps[DELAY][type_var] < 999.9 :
     tps[DELAY][type_var] = tps[DELAY][type_var] / ( 1.0 - tps[DELAY][type_var] * 1e-3 )
    reinitFontPara(bgFont, textsPara, pos_textsPara, font, tps, type_var, pause, var)
    start = True
    
  if not(pause) and ( tps[DELAY][type_var] <= tps[PRES] - tps[PAST] ):
   if type_var == TABLE:
    if var == DECREASE:
     table -= 0.01
    else:
     table += 0.01
   else:
    if var == DECREASE:
     if modulo != 1:
      modulo -= 1
     else:
      pause = True
    else:
     modulo += 1
    reinit(texts, pos_texts, pos_circles, font, modulo)
    
   reinitFont(bg, text_title, textpos, texts, font, table, modulo)
   start = True
   tps[PAST] = tps[PRES]
  
  if start == True:
   if not pause :
    circle(bg, BRIGHTBLUE, POS_CIRCLE, R, THICKNESS)
    create_points(bg, pos_circles, modulo)
    create_lines(bg, pos_circles, table, modulo)
    create_texts(bg, texts, pos_texts, pos_circles, modulo)
    screen.blit(bg, (0, 0))
   screen.blit(bgFont, (0, 0))
   pygame.display.flip()
   start = False


WIDTH_SC = getSystemResolutionOnLinux()
HEIGH_SC = int( WIDTH_SC[1] * 0.9 )
WIDTH_SC = int( WIDTH_SC[0] * 0.9 )

#Mouse Button, Scroll Wheel
MB_LEFT, MB_MIDDLE, MB_RIGHT, MBSW_UP, MBSW_DOWN = 1, 2, 3, 4, 5

R = int( HEIGH_SC * 0.45 )
R_ = int( 4 * WIDTH_SC / 1366 )
POS_CIRCLE = (WIDTH_SC/2, HEIGH_SC/2)
THICKNESS = 1
FONT_SIZE = int( 32 * WIDTH_SC / 1366 )
EPS = int( 30 * WIDTH_SC / 1366 )

#              R    G    B
WHITE      = (250, 250, 250)
BLACK      = ( 10,  10,  10)
GREEN      = (  0, 155,   0)
BRIGHTBLUE = (  0,  50, 255)
BROWN      = (174,  94,   0)


PAST, PRES, DELAY = 0, 1, 2
INCREASE, DECREASE = 1, 0
TABLE, MODULO = 0, 1
X, Y = 0, 1


TYPE_VAR = { TABLE : "TABLE" , MODULO : "MODULO" }
SENS = { DECREASE : "<-" , INCREASE : "->" }

if __name__ == '__main__' : main()

