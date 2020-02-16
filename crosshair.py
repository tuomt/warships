import pygame
import os

class Crosshair(pygame.sprite.Sprite):
    def __init__(self, square_size):
        pygame.sprite.Sprite.__init__(self)
        # Initialize variables
        self.image_name = 'crosshair.png'
        # Assign sprite attributes
        # Load image to surfaces
        self.rect = None
        self.load_image(self.image_name)
        self.scale_image(square_size)

    def move_to(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
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

    def load_image(self, image_name):
        # Loads the image to the self.image surface
        # Returns the updated image surface
        self.image = pygame.image.load(os.path.join('data', image_name)).convert_alpha() 
        self.image_name = image_name
        # Update the rectangle of the crosshair
        self.rect = self.image.get_rect()

        return self.image

    def scale_image(self, size):
        # Scales the image based on the size argument
        # Then assigns the scaled image to the surface attributes
        # and updates the rect attribute
        # Returns the updated image surface

        # Scale
        width = size[0]
        height = size[1]
        self.image = pygame.transform.scale(self.image, (width, height))

        # Update the rectangle of the crosshair
        current_x = self.rect.x
        current_y = self.rect.y
        self.rect = self.image.get_rect()
        self.move_to(current_x, current_y)
        
        return self.image

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
