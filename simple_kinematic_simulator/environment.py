try:
    import pygame
except ImportError:
    pygame = None
from shapely.geometry import LineString, Point


class Environment:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.obstacle_walls = []
        self.create_floorplan()

    def get_dimensions(self):
        return (self.width, self.height)

    def create_floorplan(self):
        # Create LineString objects for the walls
        left_wall = (LineString([(0, 0), (0, self.height)]), (255, 0, 255))  # purple
        bottom_wall = (
            LineString([(0, self.height), (self.width, self.height)]),
            (255, 0, 255),
        )
        right_wall = (
            LineString([(self.width, self.height), (self.width, 0)]),
            (255, 0, 255),
        )
        top_wall = (LineString([(self.width, 0), (0, 0)]), (255, 0, 255))

        # Internal walls
        # Vertical corridor in left third
        vertical1 = (LineString([(100, 0), (100, 300)]), (0, 255, 0))  # green
        vertical2 = (LineString([(100, 400), (100, self.height)]), (0, 255, 0))

        # Horizontal block across the middle
        horizontal1 = (LineString([(100, 300), (300, 300)]), (0, 255, 0))
        horizontal2 = (LineString([(300, 300), (300, 500)]), (0, 255, 0))

        # Box-style room in top-right
        box1 = (
            LineString([(self.width - 200, 0), (self.width - 200, 200)]),
            (0, 255, 0),
        )
        box2 = (
            LineString([(self.width - 200, 200), (self.width - 50, 200)]),
            (0, 255, 0),
        )
        box3 = (LineString([(self.width - 50, 200), (self.width - 50, 0)]), (0, 255, 0))

        # U-shaped obstacle near center
        u_left = (LineString([(400, 400), (400, 550)]), (0, 255, 0))
        u_bottom = (LineString([(400, 550), (600, 550)]), (0, 255, 0))
        u_right = (LineString([(600, 550), (600, 400)]), (0, 255, 0))

        self.obstacle_walls = [
            left_wall,
            bottom_wall,
            right_wall,
            top_wall,
            vertical1,
            vertical2,
            horizontal1,
            horizontal2,
            box1,
            box2,
            box3,
            u_left,
            u_bottom,
            u_right,
        ]

    def get_obstacles(self):
        return self.obstacle_walls

    def check_collision(self, pos, radius):
        # This is not a collision sensor. If you need that, define it as you wish
        for line, color in self.obstacle_walls:
            if line.distance(Point(pos.x, pos.y)) <= radius:
                return True

    def draw(self, screen):
        # Draw the walls
        for wall, color in self.obstacle_walls:
            pygame.draw.line(
                screen,
                color,
                (int(wall.xy[0][0]), int(wall.xy[1][0])),
                (int(wall.xy[0][1]), int(wall.xy[1][1])),
                4,
            )  # (screen, (255, 0, 0), False, wall.xy, 4)
