from os import walk
from csv import reader
import pygame
from settings import *


# Image Import from file
def import_folder(path):
    surface_list = []
    # gets the files from the path to gain all the paths to all the images in a folder
    for _,__,img_files in walk(path):
        for image in img_files:
            # make the full path
            full_path = path + "/" + image
            # putting all the images in a list of surface list
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)
    # returns surface list after the function is run
    return surface_list

# import the csv layout
def import_csv_layout(path):
    terrain_map = []
    # open the file map
    with open(path) as map:
        # then read all the values in the csv
        level = reader(map, delimiter=",")
        for row in level:
            # making the csv more readable in python with list
            terrain_map.append(list(row))
        # returns the terrain map list after the function is run
        return terrain_map

# Cutting the graphic images of the tilesets
def import_cut_graphic(path):
    # Creating variables and making the path of the image into a pygame img
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)
    cut_tiles = []
    # checking all the images by index to move them into rows and colloums
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            # Setting values back to 64 times 64 pixel value
            x = col * tile_size
            y = row * tile_size
            # create a new surface of the cut graphic
            new_surf = pygame.Surface((tile_size, tile_size), flags = pygame.SRCALPHA)
            # creates new image based on the 64 by 64 graphic image
            new_surf.blit(surface , (0,0), pygame.Rect(x,y,tile_size,tile_size))
            # putting all the images into a tile list
            cut_tiles.append(new_surf)
    # return the cut tiles value after the function is run
    return cut_tiles

# Particle class to run and make jump and land particle dust
class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()
        # Sets thee animation speed and frame index variable
        self.frame_index = 0
        self.animation_speed = animation_speed_rate
        # checks if inputted type is jump and imports the jump images
        if type == "jump":
            self.frames = import_folder("../images/dust_particles/jump")
        # checks if inputted type is land and imports the land imgaes
        if type == "land":
            self.frames = import_folder("../images/dust_particles/land")
        # reinputting variables to get the rect value of dust
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
    
    # animate function to kill all animations tht run with the particle effect class due to it being single use
    def animate(self):
        self.frame_index += self.animation_speed
        # checks frame index is equal to len of list frames
        if self.frame_index >= len(self.frames):
            # kills the particle effect
            self.kill()
        # continue the animation
        else:
            self.image = self.frames[int(self.frame_index)]

    # runs all the functions in particle effect
    def update(self, x_shift):
        self.animate()
        # makes the dust still follow the lvl so it doesnt look weird
        self.rect.x += x_shift

