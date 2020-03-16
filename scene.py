import pygame
import ship
import menu
import settings
import grid
import networking.client
import networking.server
from networking.packet import Packet
import color
from crosshair import Crosshair
from hitmarker import Hitmarker
from missmarker import Missmarker
# Initialize fonts
title_font = pygame.freetype.SysFont("monospace", 70)
title_font.pad = True
title_font.strong = True
font = pygame.freetype.SysFont("Helvetica", 50)
font.pad = True
mono_font = pygame.freetype.SysFont("monospace", 50)
mono_font.pad = True
status_font = pygame.freetype.SysFont("Helvetica", 20)

settings = settings.Settings()
# TODO: Should these be in constants or settings file???
# Set the window settings
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

class SceneHandler():
    def __init__(self, start_scene, *args):
        self.scene = None
        # Set the scene to start scene
        self.switch(start_scene, *args)

    def switch(self, dest, *args):
        if dest == Scene.MAIN_MENU:
            self.scene = MainMenu(self, *args)
        elif dest == Scene.HOST_MENU:
            self.scene = HostMenu(self, *args)
        elif dest == Scene.WAIT_HOST_MENU:
            self.scene = WaitHostMenu(self, *args)
        elif dest == Scene.CONNECT_MENU:
            self.scene = ConnectMenu(self, *args)
        elif dest == Scene.WAIT_CONNECT_MENU:
            self.scene = WaitConnectMenu(self, *args)
        elif dest == Scene.PLACEMENT:
            self.scene = Placement(self, *args)
        elif dest == Scene.CLASH:
            self.scene = Clash(self, *args)
        elif dest == Scene.END:
            self.scene = End(self, *args)

class Scene():
    MAIN_MENU         = 1
    HOST_MENU         = 2
    WAIT_HOST_MENU    = 3
    CONNECT_MENU      = 4
    WAIT_CONNECT_MENU = 5
    PLACEMENT         = 6
    CLASH             = 7
    END               = 8

    def __init__(self):
        raise NotImplementedError

    def check_events(self):
        raise NotImplementedError

    def do_logic(self):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError

class MainMenu(Scene, menu.Menu):
    def __init__(self, scene_handler, screen):
        self.scene_handler = scene_handler
        # Get center of the screen
        center = screen.get_rect().center
        # Create labels
        self.title = menu.Label("MAIN", title_font, color.BLACK, color.GREY)
        self.title.rect.center = center
        self.title.rect.y = 50
        # Create buttons
        self.host_btn = menu.Button("Host a server", font)
        self.host_btn.rect.center = center
        self.host_btn.rect.y -= 75
        self.connect_btn = menu.Button("Connect to a server", font)
        self.connect_btn.rect.center = center
        self.exit_btn = menu.Button("Exit", font)
        self.exit_btn.rect.center = center
        self.exit_btn.rect.y += 100
        self.test_btn = menu.Button("TEST", font)
        self.test_btn.rect.center = center
        self.test_btn.rect.y += 200
        buttons = [self.host_btn, self.connect_btn, self.exit_btn, self.test_btn]
        # Pass created components to the menu base class
        menu.Menu.__init__(self, screen, [self.title], buttons)

    def check_events(self):
        selected = self.check_menu_events()
        if selected == self.exit_btn or selected == -1:
            exit()
        elif selected == self.host_btn:
            self.scene_handler.switch(Scene.HOST_MENU, self.screen, "localhost", 7777)
        elif selected == self.connect_btn:
            self.scene_handler.switch(Scene.CONNECT_MENU, self.screen, "localhost", 7777)
        elif selected == self.test_btn:
            self.scene_handler.switch(Scene.PLACEMENT, self.screen, settings, None)

    def do_logic(self):
        pass
        
    def draw(self):
        self.screen.fill(color.GREY)
        self.draw_components()

class HostMenu(Scene, menu.Menu):
    def __init__(self, scene_handler, screen, ip=None, port=None):
        self.scene_handler = scene_handler
        if ip == None:
            self.ip = "IP Address"
        else:
            self.ip = ip
        if port == None:
            self.port = "Port"
        else:
            self.port = port
        center = screen.get_rect().center
        # Create labels
        self.title = menu.Label("HOST A SERVER", title_font, color.BLACK, color.GREY)
        self.title.rect.center = center
        self.title.rect.y = 50
        # Create buttons for the menu
        self.settings_btn = menu.Button("Settings", font, color.BLACK, color.GREY)
        self.settings_btn.rect.center = center
        self.start_btn = menu.Button("Start the server", font, color.BLACK, color.GREY)
        self.start_btn.rect.center = center
        self.start_btn.rect.y += 75
        self.back_btn = menu.Button("Back", font, color.BLACK, color.GREY)
        self.back_btn.rect.center = center
        self.back_btn.rect.y += 175
        # Create text boxes
        self.ip_box = menu.TextBox(self.ip, mono_font, 15, color.BLACK, color.WHITE, None, None)
        self.ip_box.rect.center = center
        self.ip_box.rect.y -= 150
        self.port_box = menu.TextBox(str(self.port), mono_font, 15, color.BLACK, color.WHITE, None, None)
        self.port_box.rect.center = center
        self.port_box.rect.y -= 75
        selectables = [self.ip_box, self.port_box, self.settings_btn, self.start_btn, self.back_btn]
        # Create the menu and draw it
        menu.Menu.__init__(self, screen, [self.title], selectables)

    def check_events(self):
        selected = self.check_menu_events()
        if selected == self.back_btn or selected == -1:
            self.scene_handler.switch(Scene.MAIN_MENU, self.screen)
        elif selected == self.settings_btn: # settings
            print("Settings menu.")
        elif selected == self.start_btn: # start server
            ip = self.ip_box.get_text()
            port = int(self.port_box.get_text())
            self.scene_handler.switch(Scene.WAIT_HOST_MENU, self.screen, ip, port)
                    
    def do_logic(self):
        pass

    def draw(self):
        self.draw_components()

class WaitHostMenu(Scene, menu.Menu):
    def __init__(self, scene_handler, screen, ip, port):
        self.scene_handler = scene_handler
        self.ip = ip
        self.port = port
        center = screen.get_rect().center
        self.title = menu.Label("Waiting for a client...", font, color.BLACK, color.BLUE_GREY)
        self.title.rect.center = center
        self.title.rect.y = 150
        self.cancel_btn = menu.Button("Cancel", font, color.BLACK, color.BLUE_GREY)
        self.cancel_btn.rect.center = center
        self.cancel_btn.rect.y = 400
        popup_offset_x = 100
        popup_offset_y = 100
        pop_rect = pygame.Rect(popup_offset_x, popup_offset_y, SCREEN_WIDTH - popup_offset_x * 2, SCREEN_HEIGHT - popup_offset_y * 2)
        menu.Menu.__init__(self, screen, [self.title], [self.cancel_btn], pop_rect, color.BLUE_GREY)
        # Create the connection
        self.connection = networking.server.Server()
        server_thread = self.connection.create(ip, port)
        server_thread.start()

    def check_events(self):
        selected = self.check_menu_events()
        if selected != None:
            # Stop the connection effort
            self.connection.close()
            self.scene_handler.switch(Scene.HOST_MENU, self.screen, self.ip, self.port)

    def do_logic(self):
        if self.connection.connected:
            self.scene_handler.switch(Scene.PLACEMENT, self.screen, settings, self.connection)
       
    def draw(self):
        self.draw_components()
        pass
                
class ConnectMenu(Scene, menu.Menu):
    def __init__(self, scene_handler, screen, ip=None, port=None):
        self.scene_handler = scene_handler
        if ip == None:
            self.ip = "Ip Address"
        else:
            self.ip = ip
        if port == None:
            self.port = "Port"
        else:
            self.port = port
        center = screen.get_rect().center
        # Create a title
        self.title = menu.Label("CONNECT", title_font, color.BLACK, color.GREY)
        self.title.rect.center = center
        self.title.rect.y = 50
        # Create buttons for the menu
        self.connect_btn = menu.Button("Connect", font, color.BLACK, color.GREY)
        self.connect_btn.rect.center = center
        self.back_btn = menu.Button("Back", font, color.BLACK, color.GREY)
        self.back_btn.rect.center = center
        self.back_btn.rect.y += 100
        # Create text boxes
        self.ip_box = menu.TextBox(self.ip, mono_font, 15, color.BLACK, color.WHITE, None, None)
        self.ip_box.rect.center = center
        self.ip_box.rect.y -= 150
        self.port_box = menu.TextBox(str(self.port), mono_font, 15, color.BLACK, color.WHITE, None, None)
        self.port_box.rect.center = center
        self.port_box.rect.y -= 75
        selectables = [self.ip_box, self.port_box, self.connect_btn, self.back_btn]
        # Create the menu and draw it
        menu.Menu.__init__(self, screen, [self.title], selectables)

    def check_events(self):
        selected = self.check_menu_events()
        if selected == self.back_btn or selected == -1:
            self.scene_handler.switch(Scene.MAIN_MENU, self.screen)
        elif selected == self.connect_btn:
            ip = self.ip_box.get_text()
            port = int(self.port_box.get_text())
            self.scene_handler.switch(Scene.WAIT_CONNECT_MENU, self.screen, ip, port)
            #if wait_connect_menu(connection):
            #    placement(settings, connection, square_group, reserved_squares)
            #else:
            #    connection.interrupt_queue.put(True)

    def do_logic(self):
        pass

    def draw(self):
        self.screen.fill(color.GREY)
        self.draw_components()

class WaitConnectMenu(Scene, menu.Menu):
    def __init__(self, scene_handler, screen, ip, port):
        self.scene_handler = scene_handler
        self.settings = None
        self.ip = ip
        self.port = port
        center = screen.get_rect().center
        self.title = menu.Label("Awaiting response from server...", font, color.BLACK, color.BLUE_GREY)
        self.title.rect.center = center
        self.title.rect.y = 150
        popup_offset_x = 100
        popup_offset_y = 100
        self.cancel_btn = menu.Button("Cancel", font, color.BLACK, color.BLUE_GREY)
        self.cancel_btn.rect.center = center
        self.cancel_btn.rect.y = 400
        pop_rect = pygame.Rect(popup_offset_x, popup_offset_y, SCREEN_WIDTH - popup_offset_x * 2, SCREEN_HEIGHT - popup_offset_y * 2)
        menu.Menu.__init__(self, screen, [self.title], [self.cancel_btn], pop_rect, color.BLUE_GREY)
        # Create the connection
        self.connection = networking.client.Client()
        client_thread = self.connection.create(ip, port)
        client_thread.start()

    def do_logic(self):
        if self.connection.connected:
            self.scene_handler.switch(Scene.PLACEMENT, self.screen, settings, self.connection)
        
        if self.connection.check_closure() != None:
            print("Failed to connect!")
            self.scene_handler.switch(Scene.CONNECT_MENU, self.screen, self.ip, self.port)

    def check_events(self):
        selected = self.check_menu_events()

        # Cancel button or escape is pressed
        if selected != None:
            # Stop the connection effort
            self.connection.close()
            self.scene_handler.switch(Scene.CONNECT_MENU, self.screen, self.ip, self.port)

    def draw(self):
        self.draw_components()

class Placement(Scene):
    def __init__(self, scene_handler, screen, settings, connection):
        self.scene_handler = scene_handler
        self.screen = screen
        self.connection = connection
        self.ready_msg_sent = False
        self.ready_msg_received = False
        # Create a game grid
        grid_offset_w = 50
        grid_offset_h = 50
        grid_width = SCREEN_WIDTH - 2 * grid_offset_w
        grid_height = SCREEN_HEIGHT - 2 * grid_offset_h
        self.grid = grid.Grid((grid_offset_w, grid_offset_h, grid_width, grid_height), settings.rows, settings.columns, 2, color.BLACK)
        # Create sprite groups 
        self.square_group = self.grid.get_square_group(color.GREEN)
        self.reserved_squares = pygame.sprite.Group()
        self.colliding_squares = []
        # Create a sprite group for the ships
        self.unplaced_ships = pygame.sprite.LayeredUpdates()
        # Is normal sprite group enough?
        self.placed_ships = pygame.sprite.LayeredUpdates() 
        self.square_size = self.grid.get_square_size_abs()
        # Normal sprite groups are not ordered, so this might return something else than the top left square
        self.start_square = self.grid.get_square((0,0))
        # Add every ship to the ships group
        grid_rect = self.grid.get_rect()
        for i in range(0, settings.carrier_count):
            carrier = ship.Ship(settings.carrier_size, self.square_size, grid_rect, self.square_group)
            carrier.move_to(self.start_square.rect.x, self.start_square.rect.y)
            self.unplaced_ships.add(carrier)
        for i in range(0, settings.battleship_count):
            battleship = ship.Ship(settings.battleship_size, self.square_size, grid_rect, self.square_group)
            battleship.move_to(self.start_square.rect.x, self.start_square.rect.y)
            self.unplaced_ships.add(battleship)
        for i in range(0, settings.cruiser_count):
            cruiser = ship.Ship(settings.cruiser_size, self.square_size, grid_rect, self.square_group)
            cruiser.move_to(self.start_square.rect.x, self.start_square.rect.y)
            self.unplaced_ships.add(cruiser)
        for i in range(0, settings.submarine_count):
            submarine = ship.Ship(settings.submarine_size, self.square_size, grid_rect, self.square_group)
            submarine.move_to(self.start_square.rect.x, self.start_square.rect.y)
            self.unplaced_ships.add(submarine)
        for i in range(0, settings.patrol_boat_count):
            patrol_boat = ship.Ship(settings.patrol_boat_size, self.square_size, grid_rect, self.square_group)
            patrol_boat.move_to(self.start_square.rect.x, self.start_square.rect.y)
            self.unplaced_ships.add(patrol_boat)

        self.awaiting_ship = self.unplaced_ships.get_sprite(0)
        self.collides = self.check_collision()
        self.ready = False

    def check_events(self):
        moved = False
        # Check events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                if self.ready:
                    # Return because all ships have been placed and we don't need to check movement keys anymore
                    return
                elif event.key == pygame.K_d:
                    print(f"Ship coords:", awaiting_ship.rect.x, awaiting_ship.rect.y)
                elif event.key == pygame.K_r:
                    self.awaiting_ship.rotate(self.grid.get_rect())
                    moved = True
                elif event.key == pygame.K_UP:
                    self.awaiting_ship.move_up()
                    moved = True
                elif event.key == pygame.K_DOWN:
                    self.awaiting_ship.move_down()
                    moved = True
                elif event.key == pygame.K_RIGHT:
                    self.awaiting_ship.move_right()
                    moved = True
                elif event.key == pygame.K_LEFT:
                    self.awaiting_ship.move_left()
                    moved = True
                # Collisions are checked again if the ship has been moved
                if moved:
                    self.collides = self.check_collision()
                elif event.key == pygame.K_RETURN:
                    self.try_place()
                    
    def check_collision(self):
        self.colliding_squares = []
        collides = False
        # Find the ship's position and check if it's reserved
        for square in self.awaiting_ship.get_squares():
            current_colliding_squares = pygame.sprite.spritecollide(square, self.reserved_squares, False)
            if len(current_colliding_squares) > 0:
                self.colliding_squares.append(square)
                collides = True
        if collides:
            return True
        else:
            return False
    
    def do_logic(self):
        # Check if the connection was closed
        controlled_closure = self.connection.check_closure()
        if controlled_closure != None:
            if controlled_closure:
                msg = "The connection was closed by the opponent."
            else:
                msg = "The connection was closed unexpectedly."
            print(msg)
            self.scene_handler.switch(Scene.MAIN_MENU, self.screen)

        if self.ready_msg_sent == False and self.ready:
            packet = Packet([1], Packet.T_READY)
            self.connection.send_queue.put(packet)
            self.ready_msg_sent = True

        if self.ready_msg_received == False:
            ready_packet = self.connection.get_packet(Packet.T_READY)
            if ready_packet != None:
                self.ready_msg_received = True

        if self.ready_msg_sent and self.ready_msg_received:
            self.scene_handler.switch(Scene.CLASH, self.screen, settings, self.connection, self.placed_ships)
           
    def draw(self):
        # Draw (order is important)
        self.screen.fill(color.GREY)
        self.grid.draw(self.screen)
#            square_group.draw(screen)
        self.placed_ships.draw(self.screen)
        if not self.ready:
            self.awaiting_ship.draw(self.screen)
            pygame.draw.rect(self.screen, color.GREEN, self.awaiting_ship.rect, 2)
        # Draw a transparent surface on top of the colliding squares
        for s in self.colliding_squares:
            transparent_surf = pygame.Surface((s.rect.width, s.rect.height))
            transparent_surf.set_alpha(128)
            transparent_surf.fill(color.RED)
            self.screen.blit(transparent_surf, (s.rect.x, s.rect.y)) 
        # Status
        #screen.blit(status.surf, status.rect)

    def try_place(self):
        # If the position is not reserved, the ship is placed there
        if self.collides == False:
            # Add the ship to the group of placed ships
            self.placed_ships.add(self.awaiting_ship)
            # Reserve the squares
            self.reserved_squares.add(self.awaiting_ship.get_squares())
            # Remove the ship from awaiting ships
            self.unplaced_ships.remove(self.awaiting_ship)
            if len(self.unplaced_ships) > 0:
                self.awaiting_ship = self.unplaced_ships.get_sprite(0)
                self.collides = self.check_collision()
            else:
                # When all ships have been placed, set state to ready
                self.ready = True
            return True
        else:
            return False

class DisconnectMenu(Scene, menu.Menu):
    def __init__(self, screen):
        self.visible = False
        center = screen.get_rect().center
        self.title = menu.Label("Exit to main menu?", font, color.BLACK, color.BLUE_GREY)
        self.title.rect.center = center
        self.title.rect.y = 250
        popup_offset_x = 200
        popup_offset_y = 200
        pop_rect = pygame.Rect(popup_offset_x, popup_offset_y, SCREEN_WIDTH - popup_offset_x * 2, SCREEN_HEIGHT - popup_offset_y * 2)
        self.yes_btn = menu.Button("Yes", font, color.BLACK, color.BLUE_GREY)
        self.yes_btn.rect.center = pop_rect.center
        self.yes_btn.rect.y += 25
        self.no_btn = menu.Button("No", font, color.BLACK, color.BLUE_GREY)
        self.no_btn.rect.center = pop_rect.center
        self.no_btn.rect.y += 100
        menu.Menu.__init__(self, screen, [self.title], [self.no_btn, self.yes_btn], pop_rect, color.BLUE_GREY)

class Clash(Scene):
    def __init__(self, scene_handler, screen, settings, connection, placed_ships):
        self.scene_handler = scene_handler
        self.screen = screen
        self.settings = settings
        self.connection = connection
        self.disconnect_menu = DisconnectMenu(screen)
        # Create the grids
        offset_x = 50
        offset_y = 50
        width = (SCREEN_WIDTH - 3 * offset_x) / 2
        #height = SCREEN_HEIGHT - 2 * offset_y
        height = SCREEN_HEIGHT / 2
        self.my_grid = grid.Grid((offset_x, offset_y, width, height), settings.rows, settings.columns, 2, color.BLACK)
        enemy_offset_x = offset_x + width + offset_x
        self.enemy_grid = grid.Grid((enemy_offset_x, offset_y, width, height), settings.rows, settings.columns, 2, color.BLACK)
        self.square_size = self.my_grid.get_square_size_abs()
        self.my_squares = self.my_grid.get_square_group(color.GREEN)
        self.enemy_squares = self.enemy_grid.get_square_group(color.GREEN)
        start_square = self.enemy_squares.sprites()[0]
        # Create spritegroups for the ships and strikes
        self.my_ships = placed_ships
        self.my_strikes = pygame.sprite.Group()
        self.my_hits = pygame.sprite.Group()
        self.my_misses = pygame.sprite.Group()
        self.enemy_strikes = pygame.sprite.Group()
        self.enemy_hits = pygame.sprite.Group()
        self.enemy_misses = pygame.sprite.Group()
        # Create a crosshair
        self.crosshair = Crosshair(self.square_size, self.enemy_grid.get_rect(), self.enemy_squares)
        # Transform the placed ships to the new grid
        for ship in self.my_ships:
            ship.transform(self.square_size, self.my_squares)
        # Decide who goes first
        self.your_turn = True
        going_first = 0
        is_host = False
        if is_host:
            going_first = random.randint(0, 1)
            if going_first == 0:
                # Send "go first" -message to the opponent
                pass

    def check_events(self):
        if self.disconnect_menu.visible:
            selection = self.disconnect_menu.check_menu_events()
            if selection == self.disconnect_menu.no_btn or selection == -1:
                self.disconnect_menu.visible = False
            elif selection == self.disconnect_menu.yes_btn:
                self.connection.close()
                self.scene_handler.switch(Scene.MAIN_MENU, self.screen)
        else:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.disconnect_menu.visible = True
                    if self.your_turn:
                        if event.key == pygame.K_UP:
                            self.crosshair.move_up()
                        elif event.key == pygame.K_DOWN:
                            self.crosshair.move_down()
                        elif event.key == pygame.K_RIGHT:
                            self.crosshair.move_right()
                        elif event.key == pygame.K_LEFT:
                            self.crosshair.move_left()
                        elif event.key == pygame.K_RETURN:
                            if self.try_strike():
                                target_square = self.crosshair.get_squares().sprites()[0]
                                self.my_strikes.add(target_square)
                                strike_pos = target_square.pos
                                # Send the strike coordinates to opponent
                                strike_packet = Packet(strike_pos, Packet.T_STRIKE)
                                self.connection.send_queue.put(strike_packet)
                                self.your_turn = False

    def try_strike(self):
        """
        Try to strike a square on the grid.

        :return: True if the strike was done, False if the position had already been struck
        :rtype: bool
        """
        target_square = self.crosshair.get_squares().sprites()[0]
        already_struck = False
        for square in self.my_strikes:
            if square == target_square:
                already_struck = True
                break

        if already_struck:
            return False
        else:
            return True

    def get_square_in_coordinates(self, square_group, position):
        position = tuple(position)
        for square in square_group:
            if square.pos == position:
                return square

    def evaluate_enemy_strike(self, strike_pos):
        """
        Check whether the enemy strike hit any of our ships.

        :param tuple strike_pos: the position where the enemy strike hit in grid coordinates (x, y)
        :return: 1 if the strike hit our ship, 0 if the strike missed
        :rtype: int
        """
        hit = False
        target_square = self.get_square_in_coordinates(self.my_squares, strike_pos)
        for ship in self.my_ships:
            for square in ship.get_squares():
                if square.pos == strike_pos:
                    hit = True
            
        if hit:
            hitmarker = Hitmarker(self.square_size, self.my_grid.get_rect(), self.my_squares)
            hitmarker.move_to(target_square.rect.x, target_square.rect.y)
            self.enemy_hits.add(hitmarker)
            return 1
        else:
            missmarker = Missmarker(self.square_size, self.my_grid.get_rect(), self.my_squares)
            missmarker.move_to(target_square.rect.x, target_square.rect.y)
            self.enemy_misses.add(missmarker)
            return 0

    def check_strike_result(self, data):
        """
        Check the result of our own strike given by the opponent. 
        Add a hitmarker or missmarker on the enemy grid depending on the result.

        :param list data: data of the result packet
        """
        result = data[0]
        strike_pos = [data[1], data[2]]
        target_square = self.get_square_in_coordinates(self.enemy_squares, strike_pos)
        if result == 1:
            hitmarker = Hitmarker(self.square_size, self.enemy_grid.get_rect(), self.enemy_squares)
            hitmarker.move_to(target_square.rect.x, target_square.rect.y)
            self.my_hits.add(hitmarker)
        else:
            missmarker = Missmarker(self.square_size, self.enemy_grid.get_rect(), self.enemy_squares)
            missmarker.move_to(target_square.rect.x, target_square.rect.y)
            self.my_misses.add(missmarker)

    def do_logic(self):
        # Check if the connection was closed
        controlled_closure = self.connection.check_closure()
        if controlled_closure != None:
            if controlled_closure:
                msg = "The connection was closed by the opponent."
            else:
                msg = "The connection was closed unexpectedly."
            print(msg)
            self.scene_handler.switch(Scene.MAIN_MENU, self.screen)

        # Enemy strike
        enemy_strike_packet = self.connection.get_packet(Packet.T_STRIKE)
        if enemy_strike_packet != None:
            strike_pos = enemy_strike_packet.get_data(include_header=False)
            result = self.evaluate_enemy_strike(tuple(strike_pos))
            data = [result, strike_pos[0], strike_pos[1]]
            enemy_result_packet = Packet(data, Packet.T_STRIKE_RESULT)
            self.connection.send_queue.put(enemy_result_packet)
            # Check if our fleet has been destroyed
            if len(self.enemy_hits) == self.settings.total_reserved_squares:
                # Send game over message
                game_over = Packet([1], Packet.T_GAME_OVER)
                self.connection.send_queue.put(game_over)
                # Hide the disconnect menu if it's open
                self.disconnect_menu.visible = False
                self.draw()
                self.scene_handler.switch(Scene.END, self.screen, self.settings, self.connection)
            else:
                self.your_turn = True

        # Result of own strike
        result_packet = self.connection.get_packet(Packet.T_STRIKE_RESULT)
        if result_packet != None:
            data = result_packet.get_data(include_header=False)
            self.check_strike_result(data)

        game_over_packet = self.connection.get_packet(Packet.T_GAME_OVER)
        if game_over_packet != None:
            self.draw()
            print("Victory!")
            self.scene_handler.switch(Scene.END, self.screen, self.settings, self.connection)

    def draw(self):
        self.screen.fill(color.GREY)
        self.my_grid.draw(self.screen)
        self.enemy_grid.draw(self.screen)
        #self.enemy_squares.draw(self.screen)
        self.my_ships.draw(self.screen)
        if len(self.enemy_strikes) > 0:
            self.enemy_strikes.draw(self.screen)
        if self.your_turn:
            self.crosshair.draw(self.screen)
        for s in self.my_ships:
            pygame.draw.rect(self.screen, color.RED, s.rect, 1)
        self.my_hits.draw(self.screen)
        self.my_misses.draw(self.screen)
        self.enemy_hits.draw(self.screen)
        self.enemy_misses.draw(self.screen)
        if self.disconnect_menu.visible:
            self.disconnect_menu.draw_components()

class End(Scene):
    class EndMenu(menu.Menu):
        def __init__(self, screen):
            popup_offset_x = 500
            popup_offset_y = 450
            pop_rect = pygame.Rect(popup_offset_x, popup_offset_y, 300, 200)
            center = pop_rect.center
            self.play_again_btn = menu.Button("Play again", font)
            self.play_again_btn.rect.center = center
            self.play_again_btn.rect.y -= 50
            self.exit_btn = menu.Button("Exit to menu", font)
            self.exit_btn.rect.center = center
            self.exit_btn.rect.y += 50
            menu.Menu.__init__(self, screen, [], [self.play_again_btn, self.exit_btn], pop_rect, color.BLUE_GREY)

    def __init__(self, scene_handler, screen, settings, connection):
        self.scene_handler = scene_handler
        self.screen = screen
        self.settings = settings
        self.connection = connection
        self.menu = self.EndMenu(screen)

    def check_events(self):
        selection = self.menu.check_menu_events()
        if selection == -1:
            exit()

        if selection == self.menu.exit_btn:
            self.connection.close()
            self.scene_handler.switch(Scene.MAIN_MENU, self.screen)
        
    def do_logic(self):
        controlled_closure = self.connection.check_closure()
        if controlled_closure != None:
            if controlled_closure:
                msg = "The connection was closed by the opponent."
            else:
                msg = "The connection was closed unexpectedly."
            print(msg)
            self.scene_handler.switch(Scene.MAIN_MENU, self.screen)

    def draw(self):
        self.menu.draw_components()
        pass
