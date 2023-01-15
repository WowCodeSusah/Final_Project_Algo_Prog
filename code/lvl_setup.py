import pygame
from sprites import *
from settings import *
from import_img import *

class lvl_setup:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.player_setup(level_data)
        self.world_update = 0
        self.current_x = 0
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        terrain_layout = import_csv_layout(level_data["terrain"])
        self.terrain_sprites = self.create_tile_group(terrain_layout, "terrain")

        area_art_layout = import_csv_layout(level_data["area_art"])
        self.area_art_sprites = self.create_tile_group(area_art_layout, "area_art")

        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)
    
    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for coloum_index, t in enumerate(row):
                if t != "-1":
                    x = coloum_index * tile_size
                    y = row_index * tile_size
                    if type == "terrain":
                        terrain_tile_list = import_cut_graphic("../lvl/area_art/Rocky_Grass.png")
                        tile_surface = terrain_tile_list[int(t)]
                        sprite = StaticTile((x, y), tile_size, tile_surface)
                    if type == "area_art":
                        area_art_tile_list = import_cut_graphic("../lvl/area_art/Decoraciones.png")
                        tile_surface = area_art_tile_list[int(t)]
                        sprite = StaticTile((x,y), tile_size, tile_surface)
                    sprite_group.add(sprite)
        return sprite_group

    def player_setup(self,layout):
        for row_index, row in enumerate(layout):
            for col_index,val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == "0":
                    sprite = Player((x,y),self.display_surface,self.create_jump_particle)
                    self.player.add(sprite)
                if val == "1":
                    relic_surface = pygame.image.load("../images/relic/t_1.png").convert_alpha()
                    sprite = StaticTile((x,y), tile_size, relic_surface)
                    self.goal.add(sprite)

    def create_jump_particle(self,pos):
        jump_particle_sprite = ParticleEffect(pos, "jump")
        self.dust_sprite.add(jump_particle_sprite)

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            offset = pygame.math.Vector2(0,20)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, "land")
            self.dust_sprite.add(fall_dust_particle)
    
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player_x < screen_weight / screen_weight_movement and direction_x < 0:
            self.world_update = player_velociy
            player.speed = 0
        elif player_x > screen_weight - (screen_weight / screen_weight_movement) and direction_x > 0:
            self.world_update = -player_velociy
            player.speed = 0
        else:
            self.world_update = 0
            player.speed = player_velociy

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = sprite.rect.left
        
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        elif player.on_right and (player.rect.right < self.current_x or player.direction.x <= 0):
            player.on_right = False
        


    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        for sprite in self.terrain_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceilling = True
            if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
                player.on_ground = False
            if player.on_ceilling and player.direction.y > 0:
                player.on_ceilling = False                    

    def run(self):
        # Dust
        self.dust_sprite.update(self.world_update)
        self.dust_sprite.draw(self.display_surface)
        
        # Tiles
        self.terrain_sprites.update(self.world_update)
        self.terrain_sprites.draw(self.display_surface)
        self.area_art_sprites.update(self.world_update)
        self.area_art_sprites.draw(self.display_surface)
        self.scroll_x()
        
        # Player
        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()
        self.player.draw(self.display_surface)