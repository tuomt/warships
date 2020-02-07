import pygame
import os

class Crosshair(pygame.sprite.Sprite):
    def __init__(self, square_size):
        pygame.sprite.Sprite.__init__(self)

        # Initialize variables
        self._image_name = 'crosshair.png'

        # Assign sprite attributes
        # Load image to surfaces
        self.image = self.load_image(square_size)
        # Assign image dimensions to a rect
        self.rect = self.image.get_rect()

    def move(self, x, y):
        self.rect.move_ip(x, y)
    
    def move_up(self, pixels, bounds = None):
        if bounds != None:
            rect_copy = self.rect.copy()
            rect_copy.move_ip(0, -pixels)
            if bounds.contains(rect_copy):
                self.rect.move_ip(0, -pixels)
                return True
            else:
                return False
        else:
            self.rect.move_ip(0, -pixels)
            return True

    def move_down(self, pixels, bounds = None):
        if bounds != None:
            rect_copy = self.rect.copy()
            rect_copy.move_ip(0, pixels)
            if bounds.contains(rect_copy):
                self.rect.move_ip(0, pixels)
                return True
            else:
                return False
        else:
            self.rect.move_ip(0, pixels)
            return True

    def move_right(self, pixels, bounds = None):
        if bounds != None:
            rect_copy = self.rect.copy()
            rect_copy.move_ip(pixels, 0)
            if bounds.contains(rect_copy):
                self.rect.move_ip(pixels, 0)
                return True
            else:
                return False
        else:
            self.rect.move_ip(pixels, 0)
            return True

    def move_left(self, pixels, bounds = None):
        if bounds != None:
            rect_copy = self.rect.copy()
            rect_copy.move_ip(-pixels, 0)
            if bounds.contains(rect_copy):
                self.rect.move_ip(-pixels, 0)
                return True
            else:
                return False
        else:
            self.rect.move_ip(-pixels, 0)
            return True

#TODO: edit
    def get_square(self, square_group):
        square_list = pygame.sprite.spritecollide(self, square_group, False)
        # There should be only one square
        return square_list[0]
   
    def load_image(self, square_size):
        # Loads the image and then scales by the width and height arguments
        # Then assigns the scaled image to the surface attributes
        # Returns the updated default surface
        scale_w = int(square_size[0])
        scale_h = int(square_size[1])
        img_surface = pygame.image.load(os.path.join('data', self._image_name)).convert_alpha()
        self.image = pygame.transform.scale(img_surface.copy(), (scale_w, scale_h))
        return self.image

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
