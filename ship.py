from pygame import transform
from gridcomponent import GridComponent

class Ship(GridComponent):
    """
    A subclass of GridComponent for the warships to be placed on the game grid.

    :attr int self.size: how many squares the ship takes on the grid
    :attr tuple self._angles: the two angles the ship can be rotated to
    :attr bool self.rotated: is the ship rotated
    :attr pygame.Surface self._default_surf: the non-rotated surface
    :attr pygame.Surface self._rotated_surf: the rotated surface
    :parent: gridcomponent.GridComponent
    """
    def __init__(self, size, square_size, grid_rect, square_group, image_name=None):
        """
        The constructor.

        :param int size: how many squares the ship takes on the grid
        :param tuple square_size: the size (width, height) of a square on the grid
        :param pygame.Rect grid_rect: the rectangle of the grid's boundaries
        :param pygame.sprite.Group() square_group: the squares of the grid
        :param str image_name: the filename of the image with the file extension included
        """
        self.size = size
        self._angles = (0, 90)
        self.rotated = False

        self._default_surf = None
        self._rotated_surf = None

        if image_name == None:
            img = 'default.png'
        else:
            img = image_name

        GridComponent.__init__(self, square_size, grid_rect, square_group, img)
                
    def rotate(self, bounds=None):
        """
        Rotate the ship if it's in bounds.

        :param pygame.Rect bounds: the boundaries of the grid on which the ship is placed on
        :return: True if the ship was rotated, False if the new position was out of bounds
        :rtype: bool
        """
        # A test rectangle is created first to check if the rotated ship is inside the boundaries
        # If the ship cannot be rotated, the function will return False
        if self.rotated:
            test_rect = self._default_surf.get_rect()
        else:
            test_rect = self._rotated_surf.get_rect()
        test_rect.center = self.rect.center
        if self.size % 2 == 0:
            if self.rotated:
                test_rect.x += self.square_size[0] / 2
                test_rect.y -= self.square_size[1] / 2
            else:
                test_rect.x -= self.square_size[0] / 2
                test_rect.y += self.square_size[1] / 2

        if bounds.contains(test_rect):
            # The test rect is in bounds so it is assigned to the ship's rect property
            self.rect = test_rect
            # Update the current angle and image surface
            if self.rotated:
                self.image = self._default_surf
                self.rotated = False
            else:
                self.image = self._rotated_surf
                self.rotated = True
            self.update_squares()
            return True
        else:
            return False

    def scale_image(self, size):
        """
        Scale the image according to the size parameter.
        Then assing the scaled image to the self.image attribute.
        Takes in account the rotation of the ship.
        Update the self.rect attribute.
        Overrides the method of the base class.

        :param tuple size: the size (width, height) the image is scaled to
        :return: the scaled image
        :rtype: pygame.Surface
        """
        # Scale
        width = size[0]
        height = size[1]
        self._default_surf = transform.scale(self._default_surf, (width * self.size, height))
        self._rotated_surf = transform.scale(self._rotated_surf, (width, height * self.size))
        rotated = self._angles[1]
        if self.rotated:
            self.image = self._rotated_surf.copy()
        else:
            self.image = self._default_surf.copy()

        # Update the rectangle
        current_x = self.rect.x
        current_y = self.rect.y
        self.rect = self.image.get_rect()
        self.move_to(current_x, current_y)
        
        return self.image

    def load_image(self, image_name):
        """
        Load an image to the self.image surface by calling base class load_image method.
        Set the default and rotated surfaces.
        Overrides the method of the base class.

        :param str image_name: the filename of the image with the file extension included
        :return: the loaded image
        :rtype: pygame.Surface
        """
        self.image = GridComponent.load_image(self, image_name)
        # Set the default surface
        self._default_surf = self.image.copy()
        # Set the rotated surface
        self._rotated_surf = transform.rotate(self.image.copy(), self._angles[1])

        return self.image
