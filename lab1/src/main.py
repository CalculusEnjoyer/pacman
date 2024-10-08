import os

import pyglet
from game import Game
from map import Map
from ghost import Ghost
from pacman import Pacman
import random 

# Map generation seed
random.seed()

def texture_set_mag_filter_nearest( texture ):
	pyglet.gl.glBindTexture( texture.target, texture.id )
	pyglet.gl.glTexParameteri( texture.target, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST )
	pyglet.gl.glBindTexture( texture.target, 0 )

def start_game():
    TILE_SIZE = 14
    MAP_SIZE = 80
    os.chdir('/Users/user/unv/is-labs/lab1')
    wall_image = pyglet.image.load('sprites/wall.png')
    texture_set_mag_filter_nearest(wall_image.get_texture())

    small_apple_image = pyglet.image.load('sprites/small_apple.png')
    texture_set_mag_filter_nearest(small_apple_image.get_texture())

    big_apple_image = pyglet.image.load('sprites/big_apple.png')
    texture_set_mag_filter_nearest(big_apple_image.get_texture())

    map = Map(wall_image, small_apple_image, big_apple_image, MAP_SIZE, TILE_SIZE)

    ghost_sheet = pyglet.image.load('sprites/ghost_w.png')
    ghost_images = pyglet.image.ImageGrid(ghost_sheet, 1, 4)
    for image in ghost_images:
        texture_set_mag_filter_nearest(image.get_texture())

    pacman_sheet = pyglet.image.load('sprites/pacman.png')
    pacman_images = pyglet.image.ImageGrid(pacman_sheet, 1, 4)
    for image in pacman_images:
        texture_set_mag_filter_nearest(image.get_texture())

    NUMBER_OF_GHOSTS = 4

    GHOST_COLORS = [
        (255, 0, 0),
        (255, 183, 255),
        (0, 255, 255),
        (255, 3, 81),
        (255, 54, 81),
        (12, 183, 81)
    ]

    ghosts = []

    for i in range(NUMBER_OF_GHOSTS):
        ghost_sprites = []

        for j in range(4):
            ghost_image = ghost_images[j]
            ghost_sprite = pyglet.sprite.Sprite(img=ghost_image)
            ghost_sprite.color = GHOST_COLORS[i]
            ghost_sprite.width, ghost_sprite.height = TILE_SIZE, TILE_SIZE
            ghost_sprites.append(ghost_sprite)

        ghost = Ghost(ghost_sprites, i)
        ghosts.append(ghost)


    pacman_sprites = []
    for i in range(4):
        pacman_image = pacman_images[i]
        pacman_sprite = pyglet.sprite.Sprite(img=pacman_image)
        pacman_sprite.width, pacman_sprite.height = TILE_SIZE, TILE_SIZE
        pacman_sprites.append(pacman_sprite)

    LIVES = 10

    pacman = Pacman(pacman_sprites, LIVES)

    game = Game(map, ghosts, pacman)

    window = pyglet.window.Window(width=game.map.size * TILE_SIZE, height=game.map.size * TILE_SIZE)
    pyglet.gl.glClearColor(0,0,0,1)

    # Entity movement seed
    random.seed()

    @window.event
    def on_draw():
        window.clear()
        game.on_draw(TILE_SIZE)

    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            window.close()
        elif symbol == pyglet.window.key.R:
            game.restart_game()
        elif symbol == pyglet.window.key.SPACE:
            game.is_updating = not game.is_updating
        elif symbol == pyglet.window.key.P:
            game.show_pacman_costs = not game.show_pacman_costs


    def update(dt):
        if not game.is_updating:
            return
        
        game.frame += 1
        game.update(dt)

    pyglet.clock.schedule_interval(update, 1/60)

    pyglet.app.run()

if __name__ == "__main__":
    start_game()