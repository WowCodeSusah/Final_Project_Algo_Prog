import pygame 
import sys 
from settings import *
from lvl import *
from sprites import *
from lvl_setup import lvl_setup

pygame.init()
# Early Variable Background
screen = pygame.display.set_mode((screen_weight, screen_height))
# Background Image Variable
background_img = pygame.image.load("../lvl/background/bg.png")
background_img = pygame.transform.scale(background_img, (1200, 800))
# Lvl Text Image Variable
start_img = pygame.image.load("../lvl/background/text_lvl.png")
start_img = pygame.transform.scale(start_img, (600, 200))
# Regular Pygame Variable
clock = pygame.time.Clock()
level = lvl_setup(lvl_2, screen)

# Start Main Function For Level
def main(lvl):
    level = lvl_setup(lvl, screen)
    while True:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit() 
                sys.exit()
        # Load Image
        screen.blit(background_img.convert_alpha(),(0,0))
        # Runs the main function
        level.run()
        pygame.display.update()
        clock.tick(60)

# Start Menu Function for the Level Menu
def menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
        # Load Image
        screen.blit(background_img.convert_alpha(), (0,0))
        screen.blit(start_img.convert_alpha(), (350,250))
        pygame.display.update()
        clock.tick(60)
        # Picking Level Function
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            main(lvl_1)
        if keys[pygame.K_2]:
            main(lvl_2)
        if keys[pygame.K_3]:
            main(lvl_3)

# Starts the menu function
menu()