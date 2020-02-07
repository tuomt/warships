import pygame

class Settings:

    def __init__(self):
        self.rows = 10
        self.columns = 10
        # Ship counts
        self.carrier_count = 1
        self.battleship_count = 1
        self.cruiser_count = 0
        self.submarine_count = 0
        self.patrol_boat_count = 0
        self.ship_count = self.carrier_count + self.battleship_count + self.cruiser_count + self.submarine_count + self.patrol_boat_count

        # Ship sizes
        self.carrier_size = 6
        self.battleship_size = 4
        self.cruiser_size = 3
        self.submarine_size = 2
        self.patrol_boat_size = 1
