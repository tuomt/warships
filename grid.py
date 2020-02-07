import pygame

class SquareSprite(pygame.sprite.Sprite):
    def __init__(self, left, top, width, height, pos, color=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        #self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.move_ip(left, top)
        self.pos = pos
        self.width = width
        self.height = height

class Grid: # Change init to use settings object as argument instead
    def __init__(self, rect, rows, columns, thickness, color = (0, 0, 0)):
        # It is possible to pass the rect argument as instance of pygame.Rect
        # or as coordinates (top, left, width, height)
        if isinstance(rect, pygame.Rect):
            self._rect = rect.copy()
        else:
            self._rect = pygame.Rect(rect)
        # The square size has to be rounded or otherwise there will be problems with calculations that involve multiplication
        # These errors affect drawing, as pixels are integer values (for example, you cannot draw half a pixel)
        # This means that the size of the grid may not be exactly the same as the rectangle you passed as an argument
        self._square_size_y = int(round(self._rect.height / rows))
        self._square_size_x = int(round(self._rect.width / columns))
        # Set width and height to rounded values
        #print("rect1:", self._rect)
        self._rect.width = (columns) * self._square_size_x
        self._rect.height = (rows) * self._square_size_y
        #print("rect2:", self._rect)
        self._columns = columns
        self._rows = rows
        self._thickness = thickness
        self._color = color

    def get_rect(self):
        return self._rect

    def get_reserved_squares(self, squares, ships):
        reserved_squares = pygame.sprite.Group()
        for square in squares:
            if pygame.sprite.spritecollideany(square, ships) is not None:
                reserved_squares.add(square)
        return reserved_squares       

    def get_square_group(self, color):
        square_size = self.get_square_size_abs()
        rows = self._rows
        columns = self._columns
        group = pygame.sprite.Group()
        for x in range(0, rows):
            for y in range(0, columns):
                x1 = self._rect.x + (x * square_size[0])
                y1 = self._rect.y + (y * square_size[1])
                square = SquareSprite(x1, y1, square_size[0], square_size[1], (x, y), color)
                group.add(square)
        return group

    def get_square(self, pos):
        # Get square in grid position
        square_size = self.get_square_size_abs()
        square = pygame.sprite.Sprite()
        x1 = self._rect.x + (pos[0] * square_size[0])
        y1 = self._rect.y + (pos[1] * square_size[1])
        return SquareSprite(x1, y1, square_size[0], square_size[1], (pos[0], pos[1]))

    def draw_with_alpha(self, colorkey, alpha):
        # NOT UP TO DATE
        grid_surface = pygame.Surface((self._rect.width, self._rect.height))
        grid_surface.set_colorkey(colorkey)
        grid_surface.set_alpha(alpha)
        for i in range(0, self._line_count_y):
            y = i * self._square_size_y
            pygame.draw.line(grid_surface, self._color, [0, y], [self._rect.width, y], self._thickness)
            
        for i in range(0, self._line_count_x):
            x = i * self._square_size_x
            pygame.draw.line(grid_surface, self._color, [x, 0], [x, self._rect.height], self._thickness)
        pygame.Surface.blit(self._screen, grid_surface, (0, 0))
    
    def draw(self, surface):
        for i in range(0, self._columns + 1):
            x = self._rect.x + (i * self._square_size_x) 
            pygame.draw.line(surface, self._color, [x, self._rect.y], [x, self._rect.bottom], self._thickness)

        for i in range(0, self._rows + 1):
            y = self._rect.y + (i * self._square_size_y)
            pygame.draw.line(surface, self._color, [self._rect.x, y], [self._rect.right, y], self._thickness)
         
    def get_square_size_abs(self):
        return (self._square_size_x, self._square_size_y)
    
    def get_square_size(self): #without border
        t = self._thickness
        return (self._square_size_x - t, self._square_size_y - t)

    def get_square_center(self, square_x, square_y):
        square_size_abs = self.get_square_size_abs()
        square_size = self.get_square_size()
        x = square_x * square_size_abs[0] + (square_size[0] / 2) + self._thickness
        y = square_y * square_size_abs[1] + (square_size[1] / 2) + self._thickness
        return (x, y)

    def center_rect(self, square_x, square_y, rect_w, rect_h):
        square_size = self.get_square_size()
        square_size_abs = self.get_square_size_abs()
        if rect_w > square_size[0] or rect_h > square_size[1]:
            return (0, 0)

        x = (square_x * square_size_abs[0]) + (self._thickness / 2) + ((square_size[0] - rect_w) / 2)
        y = (square_y * square_size_abs[1]) + (self._thickness / 2) + ((square_size[1] - rect_h) / 2)
        x += 1
        y += 1
        return (x, y)


