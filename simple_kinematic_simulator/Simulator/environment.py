import pygame
from shapely.geometry import LineString, Point



class Environment:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.obstacle_walls = []
        self.create_floorplan()


    def get_dimensions(self):
        return (self.width,self.height)
    def create_floorplan(self):
        # Create LineString objects for the walls
        left_wall = (LineString([(0, 0), (0, self.height)]), (255, 0, 255))  # purple
        bottom_wall = (LineString([(0, self.height), (self.width, self.height)]), (255, 0, 255))
        right_wall = (LineString([(self.width, self.height), (self.width, 0)]), (255, 0, 255))
        top_wall = (LineString([(self.width, 0), (0, 0)]), (255, 0, 255))


        self.obstacle_walls = [left_wall,bottom_wall,right_wall,top_wall]


    def get_obstacles(self):
        return self.obstacle_walls

    def check_collision(self, pos: float, radius: float):
        # This is not a collision sensor. If you need that, define it as you wish
        for line, color in self.obstacle_walls:
            if line.distance(Point(pos.x, pos.y)) <= radius:
                return True

    def draw(self,screen: tuple[int, int]):
        # Draw the walls
        for wall,color in self.obstacle_walls:
            pygame.draw.line(screen,color,(int(wall.xy[0][0]),int(wall.xy[1][0])),(int(wall.xy[0][1]),int(wall.xy[1][1])),4)# (screen, (255, 0, 0), False, wall.xy, 4)



