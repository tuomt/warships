import pygame
from os import path

class TransformError(Exception):
    pass

class GridComponent():
    """
    A base class for components to be placed on a grid.

    :attr tuple self.square_size: the size (width, height) of a square on the grid
    :attr pygame.Rect self.grid_rect: the rectangle of the grid's boundaries
    :attr pygame.sprite.Group() self.square_group: the squares of the grid
    :attr pygame.sprite.Group() self._squares: the squares that the component occupies
    :attr pygame.Rect self.rect: the rectangle of the component
    :attr str image_name: the filename of the image with the file extension included
    :attr pygame.Surface self.image: the image surface of the component
    """
    def __init__(self, square_size, grid_rect, square_group, image_name):
        """ 
        The constructor.

        :param tuple square_size: the size (width, height) of a square on the grid
        :param pygame.Rect grid_rect: the rectangle of the grid's boundaries
        :param pygame.sprite.Group() square_group: the squares of the grid
        :param str image_name: the filename of the image with the file extension included
        """
        self.square_size = square_size
        self.grid_rect = grid_rect
        self.square_group = square_group

        self._squares = pygame.sprite.Group()
        self.rect = None
        self.image_name = image_name
        self.image = self.load_image(image_name)
        self.scale_image(self.square_size)

        start_pos = self.square_group.sprites()[0].rect.topleft
        self.move_to(start_pos[0], start_pos[1])

    def load_image(self, image_name):
        """
        Load an image to the self.image surface.
        Updates the self.image_name and self.rect attributes aswell.

        :param str image_name: the filename of the image with the file extension included
        :return: the loaded image
        :rtype: pygame.Surface
        """
        self.image = pygame.image.load(path.join('data', image_name)).convert_alpha() 
        self.image_name = image_name
        self.rect = self.image.get_rect()

        return self.image

    def scale_image(self, size):
        """
        Scale the image according to the size parameter.
        Then assings the scaled image to the self.image attribute.
        Updates the self.rect attribute aswell.

        :param tuple size: the size (width, height) the image is scaled to
        :return: the scaled image
        :rtype: pygame.Surface
        """
        # Scale
        width = size[0]
        height = size[1]
        self.image = pygame.transform.scale(self.image, (width, height))

        # Update the rectangle
        current_x = self.rect.x
        current_y = self.rect.y
        self.rect = self.image.get_rect()
        self.move_to(current_x, current_y)
        
        return self.image

    def draw(self, surface):
        """
        Draw the component on a surface.

        :param pygame.Surface surface: the surface on which the component will be drawn on
        :return: None-object
        :rtype: None
        """
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def get_squares(self):
        """
        Get the squares that the component occupies currently.

        :return: A group of the squares
        :rtype: pygame.sprite.Group()
        """
        return self._squares

    def update_squares(self):
        """
        Update the square position of the component.
        In other words, update the squares which the component is placed on.

        :return: None-object
        :rtype: None
        """
        # Remove the old squares
        self._squares.empty()
        
        # Add the new squares
        square_list = pygame.sprite.spritecollide(self, self.square_group, False)
        self._squares.add(square_list)

    def transform(self, square_size, new_squares):
        """
        Transform the current position of the component to a position on a new grid.

        :param tuple square_size: the size (width, height) of a square on the new grid
        :param pygame.sprite.Group new_squares: squares of the new grid
        :return: None-object
        :rtype: None
        """
        # Get the position of the ship's first square
        ship_pos = self.get_squares().sprites()[0].pos
        # Scale the ship's image to fit the new squares
        self.scale_image(square_size)
        # Loop through the new squares and try to find the corresponding square
        square_found = False
        for square in new_squares:
            if square.pos == ship_pos:
                square_found = True
                self.move_to(square.rect.x, square.rect.y) # Move the component to the corresponding position
                break
        if square_found == False:
            message = "Corresponding square in new_squares was not found."
            raise TransformError(message)

    def move_to(self, x, y):
        """
        Move the component to specific coordinates.

        :param int x: the x-coordinate
        :param int y: the y-coordinate
        :return: None-object
        :rtype: None
        """
        self.rect.x = x
        self.rect.y = y
        self.update_squares()
    
    def move_up(self):
        """
        Move the component up by one square.
        The movement distance depends on the self.square_size attribute.

        :return: None-object
        :rtype: None
        """
        bounds = self.grid_rect
        test_rect = self.rect.move(0, -self.square_size[1])
        if bounds.contains(test_rect):
            self.rect.move_ip(0, -self.square_size[1])
        self.update_squares()

    def move_down(self):
        """
        Move the component down by one square.
        The movement distance depends on the self.square_size attribute.

        :return: None-object
        :rtype: None
        """
        bounds = self.grid_rect
        test_rect = self.rect.move(0, self.square_size[1])
        if bounds.contains(test_rect):
            self.rect.move_ip(0, self.square_size[1])
        self.update_squares()

    def move_right(self):
        """
        Move the component right by one square.
        The movement distance depends on the self.square_size attribute.

        :return: None-object
        :rtype: None
        """
        bounds = self.grid_rect
        test_rect = self.rect.move(self.square_size[0], 0)
        if bounds.contains(test_rect):
            self.rect.move_ip(self.square_size[0], 0)
        self.update_squares()

    def move_left(self):
        """
        Move the component left by one square.
        The movement distance depends on the self.square_size attribute.

        :return: None-object
        :rtype: None
        """
        bounds = self.grid_rect
        test_rect = self.rect.move(-self.square_size[0], 0)
        if bounds.contains(test_rect):
            self.rect.move_ip(-self.square_size[0], 0)
        self.update_squares()
