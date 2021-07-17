import pygame as pg
import random
import math
import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

boids = []

FPS = 60

class Boid():
    def __init__(self, center):
        self.center = center
        self.vertex_a = (center[0], center[1] - 15)
        self.vertex_b = (center[0] - 15, center[1] + 15)
        self.vertex_c = (center[0] + 15, center[1] + 15)
        self.points = [self.vertex_a, self.vertex_b, self.center, self.vertex_c]
        boids.append(self)
        self.velocity = 61/FPS

    def update_Points(self):
        self.points = [self.vertex_a, self.vertex_b, self.center, self.vertex_c]

    def update_physics(self):


        self.update_Points()

class Canvas():
    def __init__(self):
        self.width, self.height = (1000, 1000)
        self.WIN = pg.display.set_mode((self.width, self.height))
        pg.display.flip()

    def draw_boid(self, boid):
        pg.draw.polygon(self.WIN, WHITE, boid.points)

    def cartesian_to_polar(self, boid):
        polar_points = []
        # print(f"Boid points: {boid.points}, Center: {boid.center}")

        xc = boid.center[0]
        yc = boid.center[1]

        for point in boid.points:
            xp = point[0]
            yp = point[1]

            x = xp - xc
            y = yp - yc

            distance = math.sqrt((xc - xp)** 2 + (yc - yp)** 2)

            if x == 0:
                if y < 0:
                    # 270 degrees
                    angle = math.radians(270)
                else:
                    angle = math.radians(90)
            else:
                angle = math.atan(y/x) # in radians
                # If point is on the II or III quadrant, add pi
                if y < 0 and x < 0 or y > 0 and x < 0:
                    angle += math.radians(180)
                # If point is on the IV quadrant, add 2 * pi
                if y < 0 and x < 0:
                    angle += 2 * (math.radians(180))

            polar_points.append((distance, angle))

        return polar_points

    def rotate_boid(self, boid, degree): # degree is in degrees
        polar_points = self.cartesian_to_polar(boid)
        center = boid.center

        degree = math.radians(degree)

        cartesian_points = []

        for polar_point in polar_points:
            y = center[1] + (polar_point[0] * math.sin(polar_point[1] + degree))
            x = center[0] + (polar_point[0] * math.cos(polar_point[1] + degree))

            cartesian_points.append((x, y))

        boid.vertex_a = cartesian_points[0]
        boid.vertex_b = cartesian_points[1]
        boid.vertex_c = cartesian_points[3]
        boid.update_Points()

        screen.draw_boid(boid)

    def get_vector(self, boid):
        center = boid.points[2]
        tip = boid.points[0]

        xc = center[0]
        yc = center[1]
        xt = tip[0]
        yt = tip[1]
        x = xt - xc
        y = yt - yc

        distance = boid.velocity

        if x == 0:
            if y < 0:
                # 270 degrees
                angle = math.radians(270)
            else:
                angle = math.radians(90)
        else:
            angle = math.atan(y / x)  # in radians
            # If point is on the II or III quadrant, add pi
            if y < 0 and x < 0 or y > 0 and x < 0:
                angle += math.radians(180)
            # If point is on the IV quadrant, add 2 * pi
            if y < 0 and x < 0:
                angle += 2 * (math.radians(180))

        return (distance, angle)

    def move_boid(self, boid, velocity): # degree is in degrees
        vector = self.get_vector(boid)

        cartesian_points = []

        for point in boid.points:
            y = point[1] + vector[0] * math.sin(vector[1])
            x = point[0] + vector[0] * math.cos(vector[1])

            cartesian_points.append((x, y))

        boid.vertex_a = cartesian_points[0]
        boid.vertex_b = cartesian_points[1]
        boid.vertex_c = cartesian_points[3]
        boid.center = cartesian_points[2]
        boid.update_Points()

        screen.draw_boid(boid)

    # work on this, terrible integration
    def check_edge(self, boid):
        if boid.center[0] < 0 or boid.center[1] < 0 or boid.center[0] > self.width or boid.center[1] > self.height:
            print(boid.center)
            vector = self.get_vector(boid)

            self.rotate_boid(boid, abs(math.radians(360) - vector[1]))
            # print(vector)
            #
            # cartesian_points = []
            #
            # for point in boid.points:
            #     y = point[1] + vector[0] * math.sin(vector[1] + math.radians(180))
            #     x = point[0] + vector[0] * math.cos(vector[1] + math.radians(180))
            #
            #     cartesian_points.append((x, y))
            #
            # boid.vertex_a = cartesian_points[0]
            # boid.vertex_b = cartesian_points[1]
            # boid.vertex_c = cartesian_points[3]
            # boid.center = cartesian_points[2]
            # boid.update_Points()
            #
            # screen.draw_boid(boid)




running = True
screen = Canvas()

for x in range(100):
    center = (random.randrange(0, 1000), random.randrange(0, 1000))
    boid = Boid(center)
    # pg.draw.circle(screen.WIN, RED, (500, 500), 15)
    # screen.draw_boid(boid)
    screen.rotate_boid(boid, random.randrange(179, 180))

# screen.WIN.fill(BLACK)
# for x in boids:
#     screen.draw_boid(x)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.WIN.fill(BLACK)

    for boid in boids:
        screen.move_boid(boid, boid.velocity)
        screen.check_edge(boid)
        # boid.update_physics()
        screen.rotate_boid(boid, random.randrange(-2, 3))
        screen.draw_boid(boid)

    pg.display.update()
    time.sleep(1/FPS)
