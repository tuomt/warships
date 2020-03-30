import pygame
import pygame.freetype
import color
from constants import TICK_RATE

pygame.freetype.init()
# TODO: see if fonts should be private variables

# TODO: See if classes' variables should be public instead of private

class Label():
    def __init__(self, text, font, fg_color=None, bg_color=None, scale_rect=None):
        self._text = text
        self._font = font
        if fg_color == None:
            self.fg_color = color.BLACK
        else:
            self.fg_color = fg_color
        if bg_color == None:
            self.bg_color = color.WHITE
        else:
            self.bg_color = bg_color
        self.scale_rect = scale_rect
        # Keeps the label centered on the same spot even if the text is changed
        self.keep_center = True
        properties = self._font.render(self.text, self.fg_color, self.bg_color)
        self.surf = properties[0]
        self.rect = properties[1]
        if scale_rect != None:
            # Scale the surface
            self.surf = pygame.transform.smoothscale(self.surf, (scale_rect.w, scale_rect.h))
            self.rect = scale_rect
        
    def update(self):
        # Returns a tuple: the new surface and the rectangle
        properties = self._font.render(self.text, self.fg_color, self.bg_color)
        new_surf = properties[0]
        new_rect = properties[1]
        if self.scale_rect != None:
            # Scale the surface
            new_surf = pygame.transform.smoothscale(new_surf, (self.scale_rect.w, self.scale_rect.h))
            new_rect = self.scale_rect
        if self.keep_center:
            new_rect.center = self.rect.center
        else:
            new_rect.x = self.rect.x
            new_rect.y = self.rect.y
        return (new_surf, new_rect)

    def get_surface(self):
        return self.surf

    def draw(self, dest):
        dest.blit(self.surf, self.rect)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        properties = self.update()
        self.surf = properties[0]
        self.rect = properties[1]

class TextBox():
    def __init__(self, text, font, size, fg_color = None, bg_color = None, bor_color = None):
        self._bor_w = 10
        self._text = text
        self._len = len(self._text) 
        #self._max_len = max_len
        self._font = font
        self._size = size
        if fg_color == None:
            self._fg_color = color.BLACK
        else:
            self._fg_color = fg_color
        if bg_color == None:
            self._bg_color = color.WHITE
        else:
            self._bg_color = bg_color
        if bor_color == None:
            self._bor_color = color.RED_BROWN
        else:
            self._bor_color = bor_color
        # Set the width of the textbox based on the size parameter
        # This only works correctly when using monospace fonts
        blank = ""
        for i in range(0, self._size):
            blank += "X"
        # Create a background surface and a rectangle
        (self._fg_surf, fg_rect) = font.render(blank, self._bg_color, self._bg_color) 
        bg_rect = fg_rect.copy()
        bg_rect.inflate_ip(self._bor_w, self._bor_w)
        self.rect = bg_rect
        self._bg_surf = pygame.Surface(bg_rect.size)
        self._bg_surf.fill(self._bor_color)
        # Render the text surface on the background surface
        self._surf = self.update_surf()
        # Clear textbox when user input is detected for the first time
        self._clear_text = True

    def update_surf(self):
        fg_surf = self._fg_surf.copy()
        new_surf = self._bg_surf.copy()
        self._font.render_to(fg_surf, (0,0), self._text, self._fg_color, self._bg_color)
        new_surf.blit(fg_surf, (self._bor_w / 2, self._bor_w / 2))
        return new_surf

    def enter(self, key, char):
        update = True
        if key == pygame.K_BACKSPACE and self._len > 0:
            if self._clear_text:
                self._text = ""
                self._clear_text = False
                self._len = 0
            else:
                self._text = self._text[:self._len - 1]
                self._len -= 1
        elif self._len < self._size and self.is_valid(char):
            if self._clear_text:
                self._text = ""
                self._clear_text = False
                self._len = 0
            self._text += char
            self._len += 1
        else:
            update = False

        if update:
            self._surf = self.update_surf()

    def get_rect(self):
        return self.rect

    def get_surface(self):
        return self._surf

    def get_text(self):
        return self._text

    def is_valid(self, char):
        # Returns true if the character can be printed in the textbox
        if char == '':
            return False
        c = ord(char)
        if c > 31 and c < 127:
            return True
        else:
            return False

    def draw(self, dest):
        dest.blit(self._surf, self.rect)

class Button():
    def __init__(self, text, font, fg_color=None, bg_color=None):
        self._text = text
        self._font = font
        if fg_color == None:
            self._fg_color = color.BLACK
        else:
            self._fg_color = fg_color
        if bg_color == None:
            self._bg_color = color.WHITE
        else:
            self._bg_color = bg_color
        # Create a surface and a rectangle
        (self._surf, self.rect) = font.render(text, fg_color, bg_color)

    def get_rect(self):
        return self.rect

    def get_surface(self):
        return self._surf

    def draw(self, dest):
        dest.blit(self._surf, self.rect)

class Menu():
    def __init__(self, screen, labels=[], selectables=[], rect=None, bg_color=None):
        self.screen = screen
        self.rect = rect
        self.labels = labels
        self.selectables = selectables
        self._sel_inflation = 6
        if bg_color == None:
            self.bg_color = color.GREY
        else:
            self.bg_color = bg_color
        if len(self.selectables) > 0:
            # Create a rectangle around the currently selected button
            self.sel_num = 0
            self.sel_obj = self.selectables[self.sel_num]
            self.sel_rect = self.sel_obj.get_rect().copy()
            # Inflate the rectangle so it doesn't obscure the text
            self.sel_rect.inflate_ip(self._sel_inflation, self._sel_inflation)
        else:
            self.sel_num = None
            self.sel_obj = None
            self.sel_rect = None

    def reset_selection(self):
        if len(self.selectables) > 0:
            self.sel_num = 0
            self.sel_obj = self.selectables[self.sel_num]
            self.sel_rect = self.sel_obj.get_rect().copy()
            self.sel_rect.inflate_ip(self._sel_inflation, self._sel_inflation)

    def check_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if isinstance(self.sel_obj, TextBox):
                    self.sel_obj.enter(event.key, event.unicode)
                if event.key == pygame.K_RETURN:
                    if isinstance(self.sel_obj, Button):
                        return self.sel_obj
                elif event.key == pygame.K_ESCAPE:
                    return -1
                elif event.key == pygame.K_UP:
                    if len(self.selectables) > 0:
                        self.sel_num = self.select_prev(len(self.selectables), self.sel_num)
                        self.sel_obj = self.selectables[self.sel_num]
                        self.sel_rect = self.sel_obj.get_rect().copy()
                        self.sel_rect.inflate_ip(self._sel_inflation,self._sel_inflation)
                elif event.key == pygame.K_DOWN:
                    if len(self.selectables) > 0:
                        self.sel_num = self.select_next(len(self.selectables), self.sel_num)
                        self.sel_obj = self.selectables[self.sel_num]
                        self.sel_rect = self.sel_obj.get_rect().copy()
                        self.sel_rect.inflate_ip(self._sel_inflation,self._sel_inflation)
        return None

    def draw_components(self):
        if self.rect == None:
            self.screen.fill(self.bg_color)
        else:
            new_surf = pygame.Surface(self.rect.size)
            new_surf.fill(self.bg_color)
            self.screen.blit(new_surf, self.rect)
        for label in self.labels:
            label.draw(self.screen)
        for sel in self.selectables:
            sel.draw(self.screen)
        # Draw selection rectangle
        pygame.draw.rect(self.screen, color.GREEN, self.sel_rect, 5)

    def select_prev(self, length, pos):
        if pos == 0:
            return length - 1
        else:
            return pos - 1

    def select_next(self, length, pos):
        if pos == length - 1:
            return 0
        else:
            return pos + 1





