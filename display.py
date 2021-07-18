import pygame as pg
import random
import math
import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

boids = []

FPS = 60

class Boid():
    def __init__(self, center):
        self.size = 20
        self.center = center
        self.velocity = 180 / FPS

        self.rel_polar = (self.velocity, math.radians(90))
        self.rel_card = (random.randrange(-1 * screen.width, screen.width), random.randrange(-1 * screen.height, screen.height))
        self.dest_card = (500, 500)

        # print(f"Start Dest: {math.degrees(screen.cartesian_to_polar((self.dest_card[0] - self.center[0], self.dest_card[1] - self.center[1]))[1])}, Start MyDegree: {math.degrees(self.rel_polar[1])}")

        self.vertex_a = None
        self.vertex_b = None
        self.vertex_c = None
        self.points = []
        self.compute_points()
        # print(self.points)

        self.color = WHITE
        self.neighbors = []

        boids.append(self)

    def compute_points(self):
        self.vertex_a = screen.polar_to_cartesian(self.center, (self.size, self.rel_polar[1]))
        distance = math.sqrt(self.size**2 + self.size**2)
        self.vertex_b = screen.polar_to_cartesian(self.center, (distance, math.radians(math.degrees(self.rel_polar[1]) + 135)))
        self.vertex_c = screen.polar_to_cartesian(self.center, (distance, math.radians(math.degrees(self.rel_polar[1]) - 135)))

        self.points = [self.vertex_a, self.vertex_b, self.center, self.vertex_c]

    def update_rel_polar(self):
        if math.degrees(self.rel_polar[1]) > 360:
            self.rel_polar = (self.velocity, math.radians(math.degrees(self.rel_polar[1]) % 360))

    def update_Points(self):
        self.points = [self.vertex_a, self.vertex_b, self.center, self.vertex_c]

    def update_vector(self):
        distance = math.sqrt((self.center[0] - self.rel_card[0])**2 + (self.center[1] - self.rel_card[1])**2)
        strength = 1/distance
        self.center = (self.center[0] + (strength * self.rel_card[0]), self.center[1] + (strength * self.rel_card[1]))

    def update_Boid(self):
        self.update_rel_polar()
        self.go_to_dest()
        # self.update_vector()
        self.get_neighbors()
        # self.separation()
        screen.move_boid(self)
        self.compute_points()
        # self.compute_points()
        # self.update_Points()

    def destroy(self):
        boid.points = []
        boid.center = ()

    def get_distance(self, other):
        thisx = self.center[0]
        thisy = self.center[1]
        otherx = other.center[0]
        othery = other.center[1]

        return math.sqrt((thisx - otherx)**2 + (thisy - othery)**2)

    def get_neighbors(self):
        visionrange = 100
        for boid in boids:
            if self.get_distance(boid) <= visionrange and boid not in self.neighbors:
                self.neighbors.append(boid)
                boid.neighbors.append(self)
                boid.color = RED
                self.color = RED
                # screen.draw_boid(self)
            elif self.get_distance(boid) > visionrange and boid in self.neighbors:
                self.neighbors.remove(boid)
                boid.neighbors.remove(self)
                boid.color = WHITE
                self.color = WHITE

    def separation(self):
        destination = (0, 0)
        if self.neighbors:
            for boid in self.neighbors:
                x = self.center[0] - boid.center[0]
                y = self.center[1] - boid.center[1]
                destvector = screen.cartesian_to_polar((x, y))

        if destination != (0, 0):
            # print(destination)
            self.dest_card = screen.cartesian_to_polar(destination)
            # strength = 1/polar_dest[0]
            # print(polar_dest[1] * strength)
            # self.rel_polar = (self.rel_polar[0], self.rel_polar[1] + polar_dest[1] * strength)
            # self.rel_polar = (polar_dest[0], self.rel_polar[1] + (polar_dest[1]/polar_dest[0]))

    def go_to_dest(self):
        reldest = (self.dest_card[0] - self.center[0], -(self.dest_card[1] - self.center[1]))
        destdegree = math.degrees(screen.cartesian_to_polar(reldest)[1])
        # if destdegree > 360:
        #     print(destdegree)
        #     print("This shouldn't happen")
        #     quit()
        mydegree = math.degrees(self.rel_polar[1])
        # opposite = (mydegree + 180) % 360

        # print(f"Dest Degree: {destdegree}, My Degree: {mydegree}")

        left = screen.polar_to_cartesian(self.center, (self.velocity, math.radians(math.degrees(self.rel_polar[1]) - 1)))
        right = screen.polar_to_cartesian(self.center, (self.velocity, math.radians(math.degrees(self.rel_polar[1]) + 1)))

        distanceleft = math.sqrt((left[0] - self.dest_card[0])**2 + (left[1] - self.dest_card[1])**2)
        distanceright = math.sqrt((right[0] - self.dest_card[0]) ** 2 + (right[1] - self.dest_card[1]) ** 2)

        if distanceleft > distanceright:
            self.rel_polar = (self.velocity, math.radians(math.degrees(self.rel_polar[1]) + 1))
        else:
            self.rel_polar = (self.velocity, math.radians(math.degrees(self.rel_polar[1]) - 1))

class Canvas():
    def __init__(self):
        self.width, self.height = (1000, 1000)
        self.WIN = pg.display.set_mode((self.width, self.height))
        pg.display.flip()

    def draw_boid(self, boid):
        pg.draw.polygon(self.WIN, boid.color, boid.points)

    def draw_vector(self, boid):
        pg.draw.line(self.WIN, GREEN, boid.center, boid.dest_card)

    def polar_to_cartesian(self, pos, polar):
        d, r = polar
        xc, yc = pos

        x = xc + (d * math.cos(r))
        y = yc - (d * math.sin(r))

        # print(x, y)
        return (x, y)

    def cartesian_to_polar(self, pos):
        x, y = pos

        distance = math.sqrt(x**2 + y**2)

        if x == 0 or y == 0:
            if x == 0:
                if y < 0:
                    # 270 degrees
                    angle = math.radians(270)
                else:
                    # 90 degrees
                    angle = math.radians(90)
            else:
                if x < 0:
                    # 180 degrees
                    angle = math.radians(180)
                else:
                    # 0 degrees
                    angle = math.radians(0)
        else:
            angle = math.atan(y/x) # in radians
            # If point is on the II or III quadrant, add pi
            if y < 0 and x < 0 or y > 0 and x < 0:
                angle += math.radians(180)
            # If point is on the IV quadrant, add 2 * pi
            if y < 0 and x > 0:
                angle += 2 * (math.radians(180))
        # print(f"Polar: {distance, angle}")
        return (distance, angle)

    # def cartesian_to_polar(self, boid):
    #     polar_points = []
    #     # print(f"Boid points: {boid.points}, Center: {boid.center}")
    #
    #     xc = boid.center[0]
    #     yc = boid.center[1]
    #
    #     for point in boid.points:
    #         xp = point[0]
    #         yp = point[1]
    #
    #         x = xp - xc
    #         y = yp - yc
    #
    #         distance = math.sqrt((xc - xp)** 2 + (yc - yp)** 2)
    #
    #         if x == 0:
    #             if y < 0:
    #                 # 270 degrees
    #                 angle = math.radians(270)
    #             else:
    #                 angle = math.radians(90)
    #         else:
    #             angle = math.atan(y/x) # in radians
    #             # If point is on the II or III quadrant, add pi
    #             if y < 0 and x < 0 or y > 0 and x < 0:
    #                 angle += math.radians(180)
    #             # If point is on the IV quadrant, add 2 * pi
    #             if y < 0 and x < 0:
    #                 angle += 2 * (math.radians(180))
    #
    #         polar_points.append((distance, angle))
    #
    #     return polar_points

    def rotate_boid(self, boid, degree):
        polar = math.radians(degree)
        # print(boid.rel_polar)
        boid.rel_polar = (boid.rel_polar[0], boid.rel_polar[1] + polar)
        boid.update_Boid()

    # def rotate_boid(self, boid, degree): # degree is in degrees
    #     polar_points = self.cartesian_to_polar(boid)
    #     center = boid.center
    #
    #     degree = math.radians(degree)
    #
    #     cartesian_points = []
    #
    #     for polar_point in polar_points:
    #         y = center[1] + (polar_point[0] * math.sin(polar_point[1] + degree))
    #         x = center[0] + (polar_point[0] * math.cos(polar_point[1] + degree))
    #
    #         cartesian_points.append((x, y))
    #
    #     boid.vertex_a = cartesian_points[0]
    #     boid.vertex_b = cartesian_points[1]
    #     boid.vertex_c = cartesian_points[3]
    #     boid.update_Points()
    #
    #     screen.draw_boid(boid)

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

    def move_boid(self, boid):
        vector = self.polar_to_cartesian(boid.center, boid.rel_polar)
        boid.center = vector

    # def move_boid(self, boid, velocity): # degree is in degrees
    #     vector = self.get_vector(boid)
    #
    #     cartesian_points = []
    #
    #     for point in boid.points:
    #         y = point[1] + vector[0] * math.sin(vector[1])
    #         x = point[0] + vector[0] * math.cos(vector[1])
    #
    #         cartesian_points.append((x, y))
    #
    #     boid.vertex_a = cartesian_points[0]
    #     boid.vertex_b = cartesian_points[1]
    #     boid.vertex_c = cartesian_points[3]
    #     boid.center = cartesian_points[2]
    #     boid.update_Points()
    #
    #     screen.draw_boid(boid)

    # work on this, terrible integration
    def check_edge(self, boid):
        threshold = 50
        if boid.center[0] + threshold < 0:
            points = []
            for point in boid.points:
                x = point[0] + screen.width + threshold
                y = point[1]
                points.append((x, y))
            boid.vertex_a = points[0]
            boid.vertex_b = points[1]
            boid.vertex_c = points[3]
            boid.center = points[2]
            boid.update_Points()
        if boid.center[1] + threshold < 0:
            points = []
            for point in boid.points:
                y = point[1] + screen.height + threshold
                x = point[0]
                points.append((x, y))
            boid.vertex_a = points[0]
            boid.vertex_b = points[1]
            boid.vertex_c = points[3]
            boid.center = points[2]
            boid.update_Points()
        if boid.center[0] - threshold > screen.width:
            points = []
            for point in boid.points:
                x = point[0] - screen.width - threshold
                y = point[1]
                points.append((x, y))
            boid.vertex_a = points[0]
            boid.vertex_b = points[1]
            boid.vertex_c = points[3]
            boid.center = points[2]
            boid.update_Points()
        if boid.center[1] - threshold > screen.height:
            points = []
            for point in boid.points:
                y = point[1] - screen.height - threshold
                x = point[0]
                points.append((x, y))
            boid.vertex_a = points[0]
            boid.vertex_b = points[1]
            boid.vertex_c = points[3]
            boid.center = points[2]
            boid.update_Points()

def check_mouse(mouse):
    mx, my = mouse
    threshold = 200
    for boid in boids:
        if int(math.sqrt((boid.center[0] - mx)** 2 + (boid.center[1] - my)** 2)) <= threshold:
            boid.color = GREEN
        if int(math.sqrt((boid.center[0] - mx) ** 2 + (boid.center[1] - my) ** 2)) > threshold:
            # boid.color = WHITE
            pass

running = True
screen = Canvas()

for x in range(10):
    center = (random.randrange(0, 1000), random.randrange(0, 1000))
    # center = (500, 500)
    boid = Boid(center)
    # pg.draw.circle(screen.WIN, RED, (500, 500), 15)
    # screen.draw_boid(boid)
    screen.rotate_boid(boid, random.randrange(0, 360))

screen.WIN.fill(BLACK)
# for x in boids:
#     screen.draw_boid(x)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # mouse = pg.mouse.get_pos()
    # check_mouse(mouse)

    if pg.mouse.get_pressed()[0]:
        # print("clicked")
        mousepos = pg.mouse.get_pos()
        for boid in boids:
            boid.dest_card = mousepos

    screen.WIN.fill(BLACK)

    for boid in boids:
        screen.check_edge(boid)
        boid.update_Boid()
        # boid.rel_polar = (boid.rel_polar[0], boid.rel_polar[1] + math.radians(random.randrange(-2, 3)))
        # screen.rotate_boid(boid, random.randrange(-2, 3))
        # boid.compute_points()
        screen.draw_boid(boid)
        screen.draw_vector(boid)

    pg.display.update()
    time.sleep(1/FPS)
