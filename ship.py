import pygame
import os

# When raising these exceptions, provide a message as an argument
class PositionError(Exception):
    pass

class TransformError(Exception):
    pass

class Ship(pygame.sprite.Sprite):
    def __init__(self, size, square_size, image_name=None):
        pygame.sprite.Sprite.__init__(self)

        # Initialize variables
        self._angles = [0, 90]
        self._angle = 0
        if image_name == None:
            self.image_name = 'default.png'
        else:
            self.image_name = image_name
        self._square_size = square_size
        # How much space (squares) the ship takes on the gamegrid
        self.size = size
        # Square(s) that the ship is placed on. Updated when the ship is placed successfully
        self.__squares = None
        # Load image to surfaces
        self._default_surf = None
        self._rotated_surf = None
        self.rect = None
        self.image = self.load_image(self.image_name)
        # Scale the image size according to the square size
        self.scale_image(self._square_size)

    def transform_squares(self, square_size, new_squares):
        # Get the position of the ship's first square
        ship_pos = self.get_squares()[0].pos
        # Scale the ship's image to fit the new squares
        self.scale_image(square_size)
        # Loop through the new squares and try to find the corresponding square
        square_found = False
        for square in new_squares:
            if square.pos == ship_pos:
                square_found = True
                self.move_to(square.rect.x, square.rect.y)
        if square_found == False:
            message = "Corresponding square in new_squares was not found."
            raise TransformError(message)
        
    def update_squares(self, square_group):
        self.__squares = pygame.sprite.spritecollide(self, square_group, False)

    def get_squares(self):
        # Find the squares that the ship occupies currently
        # returns list
        if self.__squares == None:
            message = "Ship has not been placed yet."
            raise PositionError(message)
        else:
            return self.__squares

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

    def rotate(self, bounds = None):
        # A test rectangle is created first to check if the rotated ship is inside the boundaries
        # If the ship cannot be rotated, the function will return False
        if self._angle == self._angles[0]:
            test_rect = self._rotated_surf.get_rect()
        else:
            test_rect = self._default_surf.get_rect()
        test_rect.center = self.rect.center
        if self.size % 2 == 0:
            if self._angle == self._angles[0]:
                test_rect.x -= self._square_size[0] / 2
                test_rect.y += self._square_size[1] / 2
            else:
                test_rect.x += self._square_size[0] / 2
                test_rect.y -= self._square_size[1] / 2

        if bounds.contains(test_rect):
            # The test rect is in bounds so it is assigned to the ship's rect property
            self.rect = test_rect
            # Update the current angle and image surface
            if self._angle == self._angles[0]:
                self._angle = self._angles[1]
                self.image = self._rotated_surf
            else:
                self._angle = self._angles[0]
                self.image = self._default_surf
            return True
        else:
            return False

    def find_squares_group(self, square_group):
        # Find the squares that the ship occupies currently
        # returns pygame.sprite.Group() object
        square_list = pygame.sprite.spritecollide(self, square_group, False)
        squares = pygame.sprite.Group()
        for square in square_list:
            squares.add(square)
        return squares

    def scale_image(self, size):
        # Scales the image based on the size argument
        # Then assigns the scaled image to the surface attributes
        # and updates the rect attribute
        # Returns the updated image surface

        # Scale
        width = size[0]
        height = size[1]
        self._default_surf = pygame.transform.scale(self._default_surf, (width * self.size, height))
        self._rotated_surf = pygame.transform.scale(self._rotated_surf, (width, height * self.size))
        rotated = self._angles[1]
        if self._angle == rotated:
            self.image = self._rotated_surf.copy()
        else:
            self.image = self._default_surf.copy()

        # Update the rectangle of the ship
        current_x = self.rect.x
        current_y = self.rect.y
        self.rect = self.image.get_rect()
        self.move_to(current_x, current_y)
        
        return self.image

    def load_image(self, image_name):
        # Loads the image
        # Returns the updated image surface
        self.image = pygame.image.load(os.path.join('data', image_name)).convert_alpha() 
        self.image_name = image_name
        # Set the default surface
        self._default_surf = self.image.copy()
        # Set the rotated surface
        self._rotated_surf = pygame.transform.rotate(self.image.copy(), self._angles[1])
        # Update the rectangle of the ship
        self.rect = self.image.get_rect()

        return self.image

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class Carrier(Ship):
    def __init__(self, size, square_size):
        Ship.__init__(self, size, square_size)

class Battleship(Ship):
    def __init__(self, size, square_size):
        Ship.__init__(self, size, square_size)

class Cruiser(Ship):
    def __init__(self, size, square_size):
        Ship.__init__(self, size, square_size)

class Submarine(Ship):
    def __init__(self, size, square_size):
        Ship.__init__(self, size, square_size)

class PatrolBoat(Ship):
    def __init__(self, size, square_size):
        Ship.__init__(self, size, square_size)


