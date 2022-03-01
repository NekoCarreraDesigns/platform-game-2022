import pygame
from tiles import Tile, StaticTile, Coins, Crate, Palms
from settings import tile_size, screen_width, screen_height
from enemy import Enemy
from player import Player
from decoration import Clouds, Sky, Water
# from particles import Particle_Effect
from support import import_csv_layout, import_cut_graphics


class Level:
    def __init__(self, level_data, surface):
        # screen
        self.display_surface = surface
        # scrolling
        self.world_shift = 0
        self.current_x = 0

        # player
        player_layout = import_csv_layout(level_data)
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        # terrain layout
        terrain_layout = import_csv_layout(level_data)
        self.terrain_sprites = self.setup_level(
            terrain_layout, 'terrain_tiles.png')

        # grass layout
        grass_layout = import_csv_layout(level_data)
        self.grass_sprites = self.setup_level(grass_layout, 'grass.png')

        # crates layout
        crate_layout = import_csv_layout(level_data)
        self.crate_sprites = self.setup_level(crate_layout, 'crate.png')

        # coins layout
        coins_layout = import_csv_layout(level_data)
        self.coins_sprites = self.setup_level(coins_layout, 'coins')

        # palms layout
        palms_layout = import_csv_layout(level_data)
        self.palms_sprites = self.setup_level(palms_layout, 'palms')

        # enemy layout
        enemy_layout = import_csv_layout(level_data)
        self.enemy_sprites = self.setup_level(enemy_layout, 'enemy')

        # constraints
        constraints_layout = import_csv_layout(level_data)
        self.constraints = self.setup_level(constraints_layout, 'constraints')

        # decorations
        self.sky = Sky(8)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 40, level_width)
        self.clouds = Clouds(400, level_width, 20)

    # def create_jump_particles(self, pos):
    #     if self.player.sprite.faces_right:
    #         pos -= pygame.math.Vector2(10, 5)
    #     else:
    #         pos += pygame.math.Vector2(10, 5)
    #     jump_particle_sprite = Particle_Effect(pos, 'jump')
    #     self.dust_sprite.add(jump_particle_sprite)

    def get_player_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    # def create_landing_particles(self):
    #     if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
    #         if self.player.sprite.faces_right:
    #             offset = pygame.math.Vector2(10, 15)
    #         else:
    #             offset = pygame.math.Vector2(-10, 15)
    #         fall_dust_particle = Particle_Effect(
    #             self.player.sprite.rect.midbottom - offset, 'land')
    #         self.dust_sprite.add(fall_dust_particle)

    def setup_level(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics(
                            './graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'grass':
                        grass_tile_list = import_cut_graphics(
                            './graphics/decorations/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == "crate":
                        sprite = Crate(tile_size, x, y)
                        sprite_group.add(sprite)
                    if type == 'coins':
                        if val == '0':
                            sprite = Coins(tile_size, x, y,
                                           './graphics/coins/gold.png')
                            sprite_group.add(sprite)
                        if val == '1':
                            sprite = Coins(tile_size, x, y,
                                           './graphics/coins/silver')
                            sprite_group.add(sprite)
                    if type == 'fg_palms':
                        sprite = Palms(tile_size, x, y,
                                       './graphics/terrain/palm_small', 38)
                        sprite_group.add(sprite)
                    if type == 'enemies':
                        sprite = Enemy(tile_size, x, y, './graphics/')
                        sprite_group.add(sprite)
                    if type == 'constraint':
                        sprite = Tile(tile_size, x, y)
                        sprite_group.add(sprite)

        return sprite_group

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    print("player")
                if val == '1':
                    hat_surface = pygame.image.load(
                        './graphics/character/hat.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add()

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraints, False):
                enemy.reverse()

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right < self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def run(self):
        # dust animation
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # decoration
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)

        # tiles
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)
        self.scroll_x()

        # enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraints.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)

        # crates
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

        # grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # coins
        self.coins_sprites.update(self.world_shift)
        self.coins_sprites.draw(self.display_surface)

        # palms
        self.palms_sprites.update(self.world_shift)
        self.palms_sprites.draw(self.display_surface)

        # player sprites
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        # water
        self.water.draw(self.display_surface, self.world_shift)

        # player
        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_ground()
        self.vertical_movement_collision()
        self.create_landing_particles()
        self.player.draw(self.display_surface)
