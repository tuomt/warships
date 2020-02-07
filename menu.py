import pygame
import pygame.freetype
import color
from constants import TICK_RATE

pygame.freetype.init()
# TODO: see if fonts should be private variables

# TODO: See if classes' variables should be public instead of private

class Label():
    def __init__(self, text, font, fg_color = None, bg_color = None):
        self._text = text
        self._font = font
        fg_color = color.BLACK
        if fg_color != None:
            self.fg_color = fg_color
        self.bg_color = color.WHITE
        if bg_color != None:
            self.bg_color = bg_color
        # Keeps the label centered on the same spot even if the text is changed
        self.keep_center = True
        properties = self._font.render(self.text, self.fg_color, self.bg_color)
        self.surf = properties[0]
        self.rect = properties[1]
        
    def update_surf(self):
        # Returns a tuple: the new surface and the rectangle
        new_surf = self._font.render(self.text, self.fg_color, self.bg_color)
        if self.keep_center:
            new_surf[1].center = self.rect.center
        else:
            new_surf[1].x = self.rect.x
            new_surf[1].y = self.rect.y
        return new_surf

    def get_surface(self):
        return self.surf

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        properties = self.update_surf()
        self.surf = properties[0]
        self.rect = properties[1]

class TextBox():
    # TODO: fixed size txtbox in which you can type past the borders
    # TODO: initial text color, when the text hasn't been edited yet

    def __init__(self, text, font, size, fg_color = None, bg_color = None, bor_color = None, init_color = None):
        self._bor_w = 10
        self._text = text
        self._len = len(self._text) 
        #self._max_len = max_len
        self._font = font
        self._size = size
        self._fg_color = color.BLACK
        if fg_color != None:
            self._fg_color = fg_color
        self._bg_color = color.WHITE
        if bg_color != None:
            self._bg_color = bg_color
        self._bor_color = color.RED_BROWN
        if bor_color != None:
            self._bor_color = bor_color
        self._init_color = color.GREY
        if init_color != None:
            self._init_color = init_color
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

class Button():
    def __init__(self, text, font, fg_color=None, bg_color=None):
        self._text = text
        self._font = font
        self._fg_color = color.BLACK
        if fg_color != None:
            self._fg_color = fg_color
        self._bg_color = color.WHITE
        if bg_color != None:
            self._bg_color = bg_color
        # Create a surface and a rectangle
        (self._surf, self.rect) = font.render(text, fg_color, bg_color)

        self._action = None

    def get_rect(self):
        return self.rect

    def get_surface(self):
        return self._surf

class Popup():
    def __init__(self, text, font, rect, buttons=[], fg_color = None, bg_color = None):
        self.visible = False
        self.buttons = buttons
        self._text = text
        self._font = font
        fg_color = color.BLACK
        if fg_color != None:
            self.fg_color = fg_color
        self.bg_color = color.WHITE
        if bg_color != None:
            self.bg_color = bg_color
        # Keeps the label centered on the same spot even if the text is changed
        self.keep_center = True
        # Rectangle defines the size and position of the window
        self.rect = rect
        self._bg_surf = pygame.Surface(rect.size)
        self._bg_surf.fill(bg_color)
        self.surf = self._bg_surf.copy()
        properties = self._font.render(self.text, self.fg_color, color.RED)
        self._fg_surf = properties[0]
        self._fg_rect = properties[1]
        self._fg_rect.centerx = self.rect.centerx
        self._fg_rect.x -= self.rect.x
        self._fg_rect.y = 50
        self.surf.blit(self._fg_surf, self._fg_rect)
        for btn in self.buttons:
            self.surf.blit(btn.get_surface(), btn.get_rect())
        
    def draw(self, dest):
        dest.blit(self.surf, self.rect)

    def update_surf(self):
        # Returns a tuple: the new surface and the rectangle
        properties = self._font.render(self.text, self.fg_color, self.bg_color)
        if self.keep_center:
            properties[1].center = self._fg_rect.center
        else:
            properties[1].x = self._fg_rect.x
            properties[1].y = self._fg_rect.y
        return properties

    def get_surface(self):
        return self.surf

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        properties = self.update_surf()
        self._fg_surf = properties[0]
        self._fg_rect = properties[1]

class Menu():
    def __init__(self, labels=[], selectables=[], rect=None, bg_color=None):
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
            self.screen.blit(label.get_surface(), label.rect)
        for sel in self.selectables:
            self.screen.blit(sel.get_surface(), sel.get_rect())
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





