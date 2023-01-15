import pygame
import sys 
from settings import *
from lvl import *
from sprites import *
from lvl_setup import *

pygame.init()
screen = pygame.display.set_mode((screen_weight, screen_height))
background_img = pygame.image.load("../lvl/background/bg.png")
background_img = pygame.transform.scale(background_img, (1200, 800))
clock = pygame.time.Clock()
level = lvl_setup(lvl_1, screen)

while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit()
    screen.blit(background_img.convert_alpha(),(0,0))
    level.run()
    pygame.display.update()
    clock.tick(60)
