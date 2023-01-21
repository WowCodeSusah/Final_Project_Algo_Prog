import pygame
import sys
import os
from settings import *

pygame.init()
# Early Variable
screen = pygame.display.set_mode((screen_weight, screen_height))
lose_img = pygame.image.load("../lvl/background/u_lose.png")
lose_img = pygame.transform.scale(lose_img, (800, 600))
win_img = pygame.image.load("../lvl/background/u_win.jpg")
win_img = pygame.transform.scale(win_img, (600, 400))
clock = pygame.time.Clock()

# Win function that starts when you win the game
def win():
    while True:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit() 
                sys.exit()
        # Fills the screen for the background
        screen.fill("black")
        screen.blit(win_img.convert_alpha(),(300,100))
        pygame.display.update()
        clock.tick(60)
        # Resets the game to Menu
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            python = sys.executable
            os.execl(python, python, * sys.argv)

# Lose function that starts when you die 
def lose():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Fills the screen for the background
        screen.fill("gray")
        screen.blit(lose_img.convert_alpha(), (200,0))
        pygame.display.update()
        clock.tick(60)
        # Resets the game to Menu
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            python = sys.executable            
            os.execl(python, python, * sys.argv)