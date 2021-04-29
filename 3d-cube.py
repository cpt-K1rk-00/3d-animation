import pygame
import math


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def coods(self):
        return self.x, self.y, self.z


class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Object:
    def __init__(self, lines):
        self.lines = lines


# gets Points and calculates its new Position
def calculate_new_position_3d(point, angle):
    matrix = [[math.cos(angle), 0, math.sin(angle)],
              [0, 1, 0],
              [-math.sin(angle), 0, math.cos(angle)]]
    # calculate new point
    new_coods = multiplication(matrix, point)
    point.x = new_coods[0]
    point.y = new_coods[1]
    point.z = new_coods[2]


# gets 3d-Points and converts them to 2d-Points
def create_2d_point(point):
    new_x = point.x - 0.5 * point.z + 300
    new_y = point.y + 0.5 * point.z + 300
    return new_x, new_y


# takes matrix and vector and calculates product (3d)
def multiplication(matrix, point):
    new_x = point.x * matrix[0][0] + point.y * matrix[0][1] + point.z * matrix[0][2]
    new_y = point.x * matrix[1][0] + point.y * matrix[1][1] + point.z * matrix[1][2]
    new_z = point.x * matrix[2][0] + point.z * matrix[2][1] + point.z * matrix[2][2]
    return new_x, new_y, new_z


# main programm
if __name__ == "__main__":

    clock = pygame.time.Clock()

    # setup pygame
    pygame.init()
    dis = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("3d-cube")
    black = (0, 0, 0)
    white = (255, 255, 255)

    # create Cube
    c1 = Point(100, -75, 100)
    c2 = Point(100, -75, -100)
    c3 = Point(-100, -75, 100)
    c4 = Point(-100, -75, -100)
    c5 = Point(100, 75, 100)
    c6 = Point(100, 75, -100)
    c7 = Point(-100, 75, 100)
    c8 = Point(-100, 75, -100)
    cube = Object([Line(c1, c2), Line(c2, c4), Line(c3, c4), Line(c1, c3),
                   Line(c5, c6), Line(c6, c8), Line(c7, c8), Line(c5, c7),
                   Line(c1, c5), Line(c2, c6), Line(c3, c7), Line(c4, c8)])

    # create octaeder
    o1 = Point(100, 0, 100)
    o2 = Point(100, 0, -100)
    o3 = Point(-100, 0, 100)
    o4 = Point(-100, 0, -100)
    o5 = Point(0, -150, 0)
    o6 = Point(0, 150, 0)
    octaeder = Object([Line(o1, o2), Line(o2, o4), Line(o3, o4), Line(o1, o3),
                       Line(o1, o5), Line(o2, o5), Line(o3, o5), Line(o4, o5),
                       Line(o1, o6), Line(o2, o6), Line(o3, o6), Line(o4, o6)])

    # start main loop
    running = True
    akt_obj = octaeder

    # extra mode only for points
    only_points = False
    while running:

        # check for end-event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # switch between objects
                if event.key == pygame.K_c:
                    akt_obj = cube
                elif event.key == pygame.K_o:
                    akt_obj = octaeder
                # switch between modes
                elif event.key == pygame.K_p:
                    only_points = not only_points

        # clear screen and draw new
        pygame.draw.rect(dis, black, (0, 0, 600, 600))

        for line in akt_obj.lines:
            new_coods_start = create_2d_point(line.start)
            new_coods_end = create_2d_point(line.end)
            pygame.draw.circle(dis, white, new_coods_start, 3)
            pygame.draw.circle(dis, white, new_coods_end, 3)
            if not only_points:
                pygame.draw.line(dis, white, new_coods_start, new_coods_end)

        # calculate new Points
        for line in akt_obj.lines:
            calculate_new_position_3d(line.start, 0.5)
            calculate_new_position_3d(line.end, 0.5)

        clock.tick(1)
        pygame.display.flip()
