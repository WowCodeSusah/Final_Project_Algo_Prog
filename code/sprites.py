import pygame
from settings import *
from import_img import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft = position)

    def update(self, x_shift):
        self.rect.x += x_shift

class StaticTile(Tile):
    def __init__(self, position, size, surface):
        super().__init__(position, size)
        self.image = surface

class Player(pygame.sprite.Sprite):
    def __init__(self, position, surface, create_jump_particle):
        super().__init__()
        self.import_character()
        self.frame_index = 0
        self.animation_speed = animation_speed_rate
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = position)
        # Dust
        self.import_dust_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = animation_speed_rate
        self.display_surface = surface
        self.create_jump_particle = create_jump_particle
        
        # Movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = player_velociy
        self.gravity = level_gravity
        self.jump = -player_jump_high
        # Status
        self.status = "idle"
        self.facing_direction = "left"
        self.on_ground = False
        self.on_ceilling = False
        self.on_left = False
        self.on_right = False

    def import_character(self):
        character_path = "../images/"
        self.animations = {"idle":[],"run":[],"jump":[]}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_particles(self):
        self.dust_run_particles = import_folder("../images/dust_particles/run")

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        if self.facing_direction == "left":
            self.image = animation[int(self.frame_index)]
        elif self.facing_direction == "right":
            self.image = pygame.transform.flip(animation[int(self.frame_index)], True, False)
        
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

    def run_dust(self):
        if self.status == "run":
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0
            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]
            if self.facing_direction == "right":
                self.display_surface.blit(dust_particle, self.rect.bottomleft - pygame.math.Vector2((6,10)))
            elif self.facing_direction == "left":
                self.display_surface.blit(pygame.transform.flip(dust_particle, True, False), self.rect.bottomright - pygame.math.Vector2((6,10)))

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_direction = "right"
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_direction = "left"
        else:
            self.direction.x = 0
        
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump_key()
            self.create_jump_particle(self.rect.midbottom)

    def get_status(self):
        if self.direction.y < 0 or self.direction.y > 1:
            self.status = "jump"
        else:
            if self.direction.x != 0:
                self.status = "run"
            else:
                self.status ="idle"

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
    
    def jump_key(self):
        self.direction.y = self.jump

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust()
        