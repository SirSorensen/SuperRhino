import pygame
from shapely.geometry import LineString, Polygon, Point



class Environment:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.obstacle_walls = []
        self.create_floorplan()
        # Define starting positions near walls for simulation experiments
        self.create_starting_positions()


    def get_dimensions(self):
        return (self.width,self.height)
    def create_floorplan(self):
        # Create LineString objects for the walls
        left_wall = (LineString([(0, 0), (0, self.height)]), (255, 0, 255))  # purple
        bottom_wall = (LineString([(0, self.height), (self.width, self.height)]), (255, 0, 255))
        right_wall = (LineString([(self.width, self.height), (self.width, 0)]), (255, 0, 255))
        top_wall = (LineString([(self.width, 0), (0, 0)]), (255, 0, 255))

        #kitchen
        kitchen_wall1 = (LineString([(300, 0), (300, 150)]), (255, 0, 255))
        kitchen_wall2 = (LineString([(0, 500), (300, 500)]), (255, 0, 255))
        kitchen_wall3 = (LineString([(300, 400), (300, 500)]), (255, 0, 255))
        #room
        room_right_wall2 = (LineString([(800, 250), (800, 800)]), (255, 0, 255))


        box_1 = (LineString([(100, 380), (150,380)]), (255, 255, 0)) # yellow
        box_2 = (LineString([(100, 380), (100, 420)]), (255, 255, 0)) # yellow
        box_3 = (LineString([(100, 420), (150, 420)]), (255, 255, 0))  # yellow
        box_4 = (LineString([(150, 380), (150, 420)]), (255, 255, 0))  # yellow


        self.obstacle_walls = [left_wall,bottom_wall,right_wall,top_wall,kitchen_wall1,\
            kitchen_wall2,kitchen_wall3,\
                room_right_wall2,\
                               box_1,box_2,box_3,box_4]
    
    def create_starting_positions(self):
        """Define starting positions near walls for simulation (x, y, theta)."""
        # Margin from walls
        margin = 50
        from math import pi
        # Predefined positions: near left, top, right, bottom walls, facing away
        self.starting_positions = [
            (margin, self.height / 2, 0),               # left wall, facing right
            (self.width / 2, margin, pi / 2),           # top wall, facing down
            (self.width - margin, self.height / 2, pi), # right wall, facing left
            (self.width / 2, self.height - margin, 3 * pi / 2), # bottom wall, facing up
        ]

    def get_starting_positions(self):
        """Return the list of predefined starting positions."""
        return getattr(self, "starting_positions", [])


    def get_obstacles(self):
        return self.obstacle_walls
    
    def check_collision(self, pos, radius):
        # This is not a collision sensor. If you need that, define it as you wish
        for line, color in self.obstacle_walls:
            if line.distance(Point(pos.x, pos.y)) <= radius:
                return True
    
    def draw(self,screen):
        # Draw the walls
        for wall,color in self.obstacle_walls:
            pygame.draw.line(screen,color,(int(wall.xy[0][0]),int(wall.xy[1][0])),(int(wall.xy[0][1]),int(wall.xy[1][1])),4)# (screen, (255, 0, 0), False, wall.xy, 4)



