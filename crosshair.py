from gridcomponent import GridComponent

class Crosshair(GridComponent):
    """
    A subclass of GridComponent for displaying the crosshair on the enemy grid.

    :parent: gridcomponent.GridComponent
    """
    def __init__(self, square_size, grid_rect, square_group):
        """
        The constructor.

        :param tuple square_size: the size (width, height) of a square on the grid
        :param pygame.Rect grid_rect: the rectangle of the grid's boundaries
        :param pygame.sprite.Group() square_group: the squares of the grid
        """
        image_name = 'crosshair.png'
        GridComponent.__init__(self, square_size, grid_rect, square_group, image_name)
