import pygame
from sprites import *
from settings import *
from import_img import *
from end import *

class lvl_setup:
    def __init__(self, level_data, surface):
        # Lvl_Setup Variables
        self.display_surface = surface
        self.player_setup(level_data)
        self.world_update = 0
        self.current_x = 0
        # Setting up the sprites variable
        self.dust_sprite = pygame.sprite.GroupSingle()
        # Setting current status
        self.player_on_ground = False

        # Loading terrain function and puts them in the lvl surface
        terrain_layout = import_csv_layout(level_data["terrain"])
        self.terrain_sprites = self.create_tile_group(terrain_layout, "terrain")

        # Loading decoration function and puts them in the lvl surface
        area_art_layout = import_csv_layout(level_data["area_art"])
        self.area_art_sprites = self.create_tile_group(area_art_layout, "area_art")

        # Loading dungeon function and puts them in the lvl surface
        dungeon_layout = import_csv_layout(level_data["dungeon"])
        self.dungeon_sprites = self.create_tile_group(dungeon_layout, "dungeon")

        # Loading dungeon background function and puts them in the lvl surface
        dungeon_background_layout = import_csv_layout(level_data["dungeon_background"])
        self.dungeon_background_sprites = self.create_tile_group(dungeon_background_layout, "dungeon_background")

        # Loading the player function and setting up the sprite group for the goal and the player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)
    
    # function for creating all the tiles in the background and foreground of the screen surface
    def create_tile_group(self, layout, type):
        # Creating the sprite group
        sprite_group = pygame.sprite.Group()
        # getting all the variables from the csv file and inputting them to get readable values
        for row_index, row in enumerate(layout):
            for coloum_index, t in enumerate(row):
                # Checking all the empty values
                if t != "-1":
                    x = coloum_index * tile_size
                    y = row_index * tile_size
                    # checking each value and cutting up the graphics based on a 64 by 64 tile size
                    # Then putting them in the screen surface based on the values gain from the csv file
                    # gaining all files from terrarin
                    if type == "terrain":
                        terrain_tile_list = import_cut_graphic("../lvl/area_art/Rocky_Grass.png")
                        tile_surface = terrain_tile_list[int(t)]
                        sprite = StaticTile((x, y), tile_size, tile_surface)
                    # gaining all files from area_art
                    if type == "area_art":
                        area_art_tile_list = import_cut_graphic("../lvl/area_art/Decoraciones.png")
                        tile_surface = area_art_tile_list[int(t)]
                        sprite = StaticTile((x,y), tile_size, tile_surface)
                    # gaining all files from dungeon
                    if type == "dungeon":
                        dungeon_tile_list = import_cut_graphic("../lvl/area_art/Dungeon_Bricks_Plain.png")
                        tile_surface = dungeon_tile_list[int(t)]
                        sprite = StaticTile((x,y), tile_size, tile_surface)
                    # gaining all files from dungeon background
                    if type == "dungeon_background":
                        dungeon_background_tile_list = import_cut_graphic("../lvl/area_art/Dungeon_Bricks_Shadow.png")
                        tile_surface = dungeon_background_tile_list[int(t)]
                        sprite = StaticTile((x,y), tile_size, tile_surface)
                    # Add all the sprites into the sprite group
                    sprite_group.add(sprite)
        # returns all the sprites generated
        return sprite_group

    # Same as create_tile_group but for the player
    def player_setup(self,layout):
        # Checking all the csv value fro the player.csv file
        # Making them into a readable value
        for row_index, row in enumerate(layout):
            for col_index,val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                # 0 in the file makes it so that its a player spawn
                if val == "0":
                    sprite = Player((x,y),self.display_surface,self.create_jump_particle)
                    self.player.add(sprite)
                # 1 in the file makes it so that its a goal spawn
                if val == "1":
                    relic_surface = pygame.image.load("../images/relic/t_1.png").convert_alpha()
                    sprite = StaticTile((x,y), tile_size, relic_surface)
                    self.goal.add(sprite)

    # Add the jump particles into the player
    def create_jump_particle(self,pos):
        # Starts the particles effect class to create the dust
        jump_particle_sprite = ParticleEffect(pos, "jump")
        self.dust_sprite.add(jump_particle_sprite)

    # Sets the player status if on ground for the second time
    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    # Add the landing particles into the player
    def create_landing_dust(self):
        # Checking if the player is not on ground and dust particles are not running to start to create landing dust
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            # Offsets the particle to make it look better
            offset = pygame.math.Vector2(0,20)
            # Starts the particles effect class to create the dust
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, "land")
            self.dust_sprite.add(fall_dust_particle)
    
    # Scrolls the game window based on the players movement direction
    def scroll_x(self):
        # set player values
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        # Set the world movement speed to the player velocity and sets the player speed to 0 in the right
        if player_x < screen_weight / screen_weight_movement and direction_x < 0:
            self.world_update = player_velociy
            player.speed = 0
        # Set the world movement speed to the player velovity and sets the player speeed to 0 in the left
        elif player_x > screen_weight - (screen_weight / screen_weight_movement) and direction_x > 0:
            self.world_update = -player_velociy
            player.speed = 0
        # Resets the value for the player if the player direction stops or goes to the other side of the screen
        else:
            self.world_update = 0
            player.speed = player_velociy

    # checks if the player sprite has exceeded the screen height and activates the lose screen
    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
            # lose screen
           lose()

    # checks if the player sprite has collided with the goal sprite and activates the win screen
    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite,self.goal,False):
            # win screen
            win()

    # Collision for horizontal movement
    def horizontal_movement_collision(self):
        # Sets the variables
        player = self.player.sprite
        # Taking the player movement value as a variable
        player.rect.x += player.direction.x * player.speed
        # Checks if the player collides with one of the terrain sprites or the dungeon sprites horizontally
        for sprite in self.terrain_sprites.sprites() + self.dungeon_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                # if the player hits a wall make so the player is put on the right side of the object
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    # Sets the status of the player
                    player.on_left = True
                    self.current_x = player.rect.left
                # if the player hits a wall make so the player is put on the left side of the object
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    # Sets the status of the player
                    player.on_right = True
                    self.current_x = sprite.rect.left
        # Checks if the player has stop moving or move to the other direction to change the status
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        elif player.on_right and (player.rect.right < self.current_x or player.direction.x <= 0):
            player.on_right = False
        
    # Collision for veritcal movement    
    def vertical_movement_collision(self):
        # Sets the variables
        player = self.player.sprite
        # Taking the player gravity value as a variable
        player.apply_gravity()
        # Checks if the player collides with one of the terrain sprites or the dungeon sprites horizontally
        for sprite in self.terrain_sprites.sprites() + self.dungeon_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                # if the player hits a wall make so the player is put on the top side of the object
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    # resets the gravity of the player so the value is consistent
                    player.direction.y = 0
                    # Set player status
                    player.on_ground = True
                # if the player hits a wall make so the player is put on the bottom side of the object
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    # resets the gravity of the player so the value is consistent
                    player.direction.y = 0
                    # Set player status
                    player.on_ceilling = True
            # Checks if the player has moved or jump to change the status
            if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
                player.on_ground = False
            if player.on_ceilling and player.direction.y > 0:
                player.on_ceilling = False                    

    # General run function to run all other functions
    def run(self):
        ## Tiles
        # Terrain
        self.terrain_sprites.update(self.world_update)
        self.terrain_sprites.draw(self.display_surface)
        # Decoration
        self.area_art_sprites.update(self.world_update)
        self.area_art_sprites.draw(self.display_surface)
        # Dungeon Background
        self.dungeon_background_sprites.update(self.world_update)
        self.dungeon_background_sprites.draw(self.display_surface)
        # Dungeon
        self.dungeon_sprites.update(self.world_update)
        self.dungeon_sprites.draw(self.display_surface)
        # Scroll fucntion
        self.scroll_x()
        
        ## Dust
        self.dust_sprite.update(self.world_update)
        self.dust_sprite.draw(self.display_surface)
        
        ## Player
        # Goal
        self.goal.update(self.world_update)
        self.goal.draw(self.display_surface)
        # Player update possition
        self.player.update()
        self.player.draw(self.display_surface)
        # Checks collision horizontally
        self.horizontal_movement_collision()
        # Checks ground status
        self.get_player_on_ground()
        # Checks collision vertically
        self.vertical_movement_collision()
        # Make landing dust
        self.create_landing_dust()
        # Checks death and win conditions
        self.check_death()
        self.check_win()