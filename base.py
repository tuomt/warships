# Import modules and packages 
import pygame
import os
import grid
import settings
import scene
import color
from constants import TICK_RATE

# Initialize the game engine
pygame.init()

# Set the window settings
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
main_grid_offset_w = 50
main_grid_offset_h = 50
main_grid_width = SCREEN_WIDTH - 2 * main_grid_offset_w
main_grid_height = SCREEN_HEIGHT - 2 * main_grid_offset_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
pygame.display.set_caption("Battleships")

# Create global objects
clock = pygame.time.Clock()
settings = settings.Settings()
reserved_squares = pygame.sprite.Group()
main_grid = grid.Grid((main_grid_offset_w, main_grid_offset_h, main_grid_width, main_grid_height), settings.rows, settings.columns, 2, color.BLACK)
square_group = main_grid.get_square_group(color.GREEN)

# TODO: when error is caught and game is halted, close all threads
#test_packet = Packet(0, "TESTI")
#print("test_packet.data", test_packet.data)

class Game():
    def __init__(self):
        pass

    def main(self):
        scene_handler = scene.SceneHandler(scene.Scene.MAIN_MENU, screen)

        done = False
        while not done:
            # Time between refreshing
            clock.tick(TICK_RATE)
            # Check events
            if pygame.event.get(pygame.QUIT):
                exit()
            scene_handler.scene.check_events()
            # Do logic here
            scene_handler.scene.do_logic()
            # Draw
            scene_handler.scene.draw()
            # This MUST happen after all the other drawing commands.
            pygame.display.flip()

gg = Game()
gg.main()
