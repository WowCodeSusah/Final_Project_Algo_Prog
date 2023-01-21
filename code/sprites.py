import pygame
from settings import *
from import_img import *

# Tile slass which takes all my tile values
class Tile(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft = position)

    def update(self, x_shift):
        self.rect.x += x_shift

# Static tile to inherent all the Tile class atribute
class StaticTile(Tile):
    def __init__(self, position, size, surface):
        super().__init__(position, size)
        self.image = surface

# Player class which controls all the player functions
class Player(pygame.sprite.Sprite):
    def __init__(self, position, surface, create_jump_particle):
        super().__init__()
        # Base attribute
        self.import_character()
        self.frame_index = 0
        self.animation_speed = animation_speed_rate
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = position)
        # Dust assosiate attribute
        self.import_dust_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = animation_speed_rate
        self.display_surface = surface
        self.create_jump_particle = create_jump_particle
        # Movement assosiate attribute
        self.direction = pygame.math.Vector2(0,0)
        self.speed = player_velociy
        self.gravity = level_gravity
        self.jump = -player_jump_high
        # Status assosiate attribute
        self.status = "idle"
        self.facing_direction = "left"
        self.on_ground = False
        self.on_ceilling = False
        self.on_left = False
        self.on_right = False

    # Function to take all the images in the images file to gain all the animation key frames
    def import_character(self):
        # File path
        character_path = "../images/"
        # Full file path
        self.animations = {"idle":[],"run":[],"jump":[]}
        for animation in self.animations.keys():
            # Combining the file paths
            full_path = character_path + animation
            # Importing the file
            self.animations[animation] = import_folder(full_path)

    # Function to take all the dust particle in the file run
    def import_dust_particles(self):
        # taking the run particle effects
        self.dust_run_particles = import_folder("../images/dust_particles/run")

    # Animation function
    def animate(self):
        # checking which status is the player in
        animation = self.animations[self.status]
        # increasing frame index based on the animation speed
        self.frame_index += self.animation_speed
        # resetting the animation based on the amout of animations there is
        if self.frame_index >= len(animation):
            self.frame_index = 0
        # if player status is facing right run the animation as it is
        if self.facing_direction == "left":
            self.image = animation[int(self.frame_index)]
        # if player is facing right flip the animation 
        elif self.facing_direction == "right":
            self.image = pygame.transform.flip(animation[int(self.frame_index)], True, False)
        
        # Checks the player status to put the animations in the right place
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        if self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceilling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceilling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceilling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
        else:
            self.rect = self.image.get_rect(center = self.rect.center)

    # Running dust animation check
    def run_dust(self):
        # Check if the player is running or not
        if self.status == "run":
            # starts the dust animations
            self.dust_frame_index += self.dust_animation_speed
            # Resets the dust animation
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0
            # Runs the animation based on the frame index given
            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]
            # checking if the player is right or left to filp and position the dust particle
            if self.facing_direction == "right":
                self.display_surface.blit(dust_particle, self.rect.bottomleft - pygame.math.Vector2((6,10)))
            elif self.facing_direction == "left":
                self.display_surface.blit(pygame.transform.flip(dust_particle, True, False), self.rect.bottomright - pygame.math.Vector2((6,10)))

    # general inputs for the game or player
    def get_input(self):
        # setting up the key value
        keys = pygame.key.get_pressed()
        # checking if the right key is pressed on increase the direction of the player
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_direction = "right"
        # checking if the left key is pressed on increase the direction of the player
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_direction = "left"
        # resseting the player movement if no key is pressed
        else:
            self.direction.x = 0
        # Checks if the player is on ground and a space button is pressed to jump
        if keys[pygame.K_SPACE] and self.on_ground:
            # Starts the jump function
            self.jump_key()
            # Starts the jump particle as the player jumps
            self.create_jump_particle(self.rect.midbottom)

    # Makes statues for the player based on direction data
    def get_status(self):
        # checks if the player is in the air
        if self.direction.y < 0 or self.direction.y > 1:
            self.status = "jump"
        # checks if the is moving in any direction
        else:
            if self.direction.x != 0:
                self.status = "run"
            # checks if the  player is idle or not doing anything
            else:
                self.status ="idle"

    # applies gravity
    def apply_gravity(self):
        # adding a constant ammount of direction.y to keep pushing the player downwards
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
    
    # Jump Function
    def jump_key(self):
        # add a certain value of direction.y to increase the players high making a jump
        self.direction.y = self.jump

    # The update function to keep running all the other functions
    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust()
        