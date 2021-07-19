import pygame as pg
import random
import math
import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (150, 150, 150)

boids = []
grouping = []

FPS = 60

class Boid():
    def __init__(self, center):
        self.size = 5
        self.vision = 100
        self.center = center
        self.velocity = 90 / FPS

        self.cohesionX = 1
        self.separationX = 1
        self.alignmentX = 1

        self.rel_polar = (self.velocity, math.radians(90))
        self.rel_card = (random.randrange(-1 * screen.width, screen.width), random.randrange(-1 * screen.height, screen.height))
        self.dest_card = (500, 500)

        self.boxindex = None

        self.highlight = False

        # print(f"Start Dest: {math.degrees(screen.cartesian_to_polar((self.dest_card[0] - self.center[0], self.dest_card[1] - self.center[1]))[1])}, Start MyDegree: {math.degrees(self.rel_polar[1])}")

        # The vertices to draw for the boid
        self.points = []
        self.neighbors = []

        self.color = WHITE

        boids.append(self)

    def group_boid(self):
        # Place the boid in a particular box depending on it's center location
        x = self.center[0] // screen.columnsize
        y = self.center[1] // screen.rowsize

        # If statements ensures that
        if x < 0:
            x = 0
        if y < 0:
            y = 0

        if x > int(screen.width/screen.columnsize) - 1:
            x = int(screen.width/screen.columnsize) - 1
        if y > int(screen.height/screen.rowsize) - 1:
            y = int(screen.height/screen.rowsize) - 1

        # To get the index for grid to array, use index = y * # of columns + x
        index = int(y * int(screen.width/screen.columnsize) + x)

        # Initializes the box index of boid
        if self.boxindex == None:
            self.boxindex = index
            grouping[self.boxindex].append(self)

        # Reconfigures box index of boid
        if self.boxindex != index:
            grouping[self.boxindex].remove(self)
            self.boxindex = index
            grouping[self.boxindex].append(self)

    def compute_points(self):
        vertex_a = screen.polar_to_cartesian(self.center, (self.size, self.rel_polar[1]))
        distance = math.sqrt(self.size**2 + self.size**2)
        vertex_b = screen.polar_to_cartesian(self.center, (distance, math.radians(math.degrees(self.rel_polar[1]) + 135)))
        vertex_c = screen.polar_to_cartesian(self.center, (distance, math.radians(math.degrees(self.rel_polar[1]) - 135)))

        self.points = [vertex_a, vertex_b, self.center, vertex_c]

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
        self.group_boid()
        self.update_rel_polar()
        self.go_to_dest()
        # self.update_vector()
        self.get_neighbors()

        # self.alignment()
        self.cohesion()
        self.separation()

        screen.move_boid(self)
        self.compute_points()

    def destroy(self):
        boid.points = []
        boid.center = ()

    def get_distance(self, other):
        thisx = self.center[0]
        thisy = self.center[1]
        otherx = other.center[0]
        othery = other.center[1]

        # print(self.center, other.center)
        #
        # print(math.sqrt((thisx - otherx)**2 + (thisy - othery)**2))
        return math.sqrt((thisx - otherx)**2 + (thisy - othery)**2)

    def get_neighbors(self):
        visionrange = self.vision

        proportion = int(screen.width/screen.columnsize)

        x = self.boxindex % proportion
        y = self.boxindex // proportion

        checkboids = []
        if x > 0 and y > 0 and x < proportion - 1 and y < proportion - 1:
            # print(x, y, ((y - 1) * screen.rowsize) + (x - 1))
            checkboids += grouping[(y - 1) * proportion + (x - 1)]  # Top-left
            checkboids += grouping[(y - 1) * proportion + x]  # Top-center
            checkboids += grouping[(y - 1) * proportion + (x + 1)]  # Top-right
            checkboids += grouping[y * proportion + (x - 1)]  # Left-center
            checkboids += grouping[y * proportion + x]  # Center
            checkboids += grouping[y * proportion + (x + 1)]  # Right-center
            checkboids += grouping[(y + 1) * proportion + (x - 1)]  # Bottom-left
            checkboids += grouping[(y + 1) * proportion + x]  # Bottom-center
            checkboids += grouping[(y + 1) * proportion + (x + 1)]  # Bottom-right
        if x < 1:
            checkboids += grouping[y * proportion + x]  # Center
            checkboids += grouping[y * proportion + (x + 1)]  # Right-center
            if y < 1:
                checkboids += grouping[(y + 1) * proportion + x]  # Bottom-center
                checkboids += grouping[(y + 1) * proportion + (x + 1)]  # Bottom-right
            elif y >= proportion - 1:
                checkboids += grouping[(y - 1) * proportion + x]  # Top-center
                checkboids += grouping[(y - 1) * proportion + (x + 1)]  # Top-right
            else:
                checkboids += grouping[(y + 1) * proportion + x]  # Bottom-center
                checkboids += grouping[(y + 1) * proportion + (x + 1)]  # Bottom-right
                checkboids += grouping[(y - 1) * proportion + x]  # Top-center
                checkboids += grouping[(y - 1) * proportion + (x + 1)]  # Top-right

        if x >= proportion - 1:
            checkboids += grouping[y * proportion + x]  # Center
            checkboids += grouping[y * proportion + (x - 1)]  # Left-center
            if y < 1:
                checkboids += grouping[(y + 1) * proportion + x]  # Bottom-center
                checkboids += grouping[(y + 1) * proportion + (x - 1)]  # Bottom-left
            elif y >= proportion - 1:
                checkboids += grouping[(y - 1) * proportion + x]  # Top-center
                checkboids += grouping[(y - 1) * proportion + (x - 1)]  # Top-left
            else:
                checkboids += grouping[(y + 1) * proportion + x]  # Bottom-center
                checkboids += grouping[(y + 1) * proportion + (x - 1)]  # Bottom-left
                checkboids += grouping[(y - 1) * proportion + x]  # Top-center
                checkboids += grouping[(y - 1) * proportion + (x - 1)]  # Top-left

        if y < 1:
            checkboids += grouping[y * proportion + x]  # Center
            checkboids += grouping[(y + 1) * proportion + x]  # Bottom-center
            if x < 1:
                checkboids += grouping[y * proportion + (x + 1)]  # Right-center
                checkboids += grouping[(y + 1) * proportion + (x + 1)]  # Bottom-right
            elif x >= proportion - 1:
                checkboids += grouping[y * proportion + (x - 1)]  # Left-center
                checkboids += grouping[(y + 1) * proportion + (x - 1)]  # Bottom-left
            else:
                checkboids += grouping[y * proportion + (x + 1)]  # Right-center
                checkboids += grouping[(y + 1) * proportion + (x + 1)]  # Bottom-right
                checkboids += grouping[y * proportion + (x - 1)]  # Left-center
                checkboids += grouping[(y + 1) * proportion + (x - 1)]  # Bottom-left

        if y >= proportion - 1:
            checkboids += grouping[y * proportion + x]  # Center
            checkboids += grouping[(y - 1) * proportion + x]  # Top-center
            if x < 1:
                checkboids += grouping[y * proportion + (x + 1)]  # Right-center
                checkboids += grouping[(y - 1) * proportion + (x + 1)]  # Top-right
            elif x >= proportion - 1:
                checkboids += grouping[y * proportion + (x - 1)]  # Left-center
                checkboids += grouping[(y - 1) * proportion + (x - 1)]  # Top-left
            else:
                checkboids += grouping[y * proportion + (x + 1)]  # Right-center
                checkboids += grouping[(y - 1) * proportion + (x + 1)]  # Top-right
                checkboids += grouping[y * proportion + (x - 1)]  # Left-center
                checkboids += grouping[(y - 1) * proportion + (x - 1)]  # Top-left

        for boid in checkboids:
            screen.draw_grouping(self, boid)
            if boid != self and self.get_distance(boid) <= visionrange and boid not in self.neighbors:
                self.neighbors.append(boid)
                boid.neighbors.append(self)
                # boid.color = RED
                # self.color = RED
                # screen.draw_boid(self)
            elif self.get_distance(boid) > visionrange and boid in self.neighbors:
                self.neighbors.remove(boid)
                boid.neighbors.remove(self)
                # boid.color = WHITE
                # self.color = WHITE

        for boid in self.neighbors:
            screen.draw_neighbor(self, boid)

    def alignment(self):
        degree = 0
        count = 0
        for boid in self.neighbors:
            degree += math.degrees(boid.rel_polar[1])
            count += 1

        if count > 0:
            degreeavg = degree / count

            self.rel_polar = (self.velocity, math.radians(degreeavg))


    def cohesion(self):
        # self.dest_card = self.center
        totalx, totaly = 0, 0
        count = 0
        for boid in self.neighbors:
            x = boid.center[0]
            y = boid.center[1]
            totalx, totaly = totalx + x, totaly + y
            count += 1

        if count > 0:
            avgx, avgy = totalx / count, totaly / count

            self.dest_card = (avgx * self.cohesionX, avgy * self.cohesionX)

    def separation(self):
        self.dest_card = self.center
        if self.neighbors:
            for boid in self.neighbors:
                x = (self.center[0] - boid.center[0]) / self.get_distance(boid)
                y = (self.center[1] - boid.center[1]) / self.get_distance(boid)
                self.dest_card = (self.dest_card[0] + x * self.separationX, self.dest_card[1] + y * self.separationX)

    def go_to_dest(self):
        left = screen.polar_to_cartesian(self.center, (self.velocity, math.radians(math.degrees(self.rel_polar[1]) - 1)))
        right = screen.polar_to_cartesian(self.center, (self.velocity, math.radians(math.degrees(self.rel_polar[1]) + 1)))

        distanceleft = math.sqrt((left[0] - self.dest_card[0])**2 + (left[1] - self.dest_card[1])**2)
        distanceright = math.sqrt((right[0] - self.dest_card[0]) ** 2 + (right[1] - self.dest_card[1]) ** 2)

        polar = screen.cartesian_to_polar(self.dest_card)
        strength = 3000/polar[0]
        # print(polar[0], strength)

        # if polar[1] > 700 and polar[1] < 800:
        #     strength = 90

        if distanceleft > distanceright:
            self.rel_polar = (self.velocity, math.radians(math.degrees(self.rel_polar[1]) + strength))
        else:
            self.rel_polar = (self.velocity, math.radians(math.degrees(self.rel_polar[1]) - strength))

class Canvas():
    def __init__(self):
        self.width, self.height = (1000, 1000)
        self.WIN = pg.display.set_mode((self.width, self.height))
        self.columnsize, self.rowsize = 100, 100
        pg.display.flip()

    def draw_grid(self):
        for x in range(self.columnsize, self.width + 1, self.columnsize):
            pg.draw.line(self.WIN, GREY, (x, 0), (x, self.height))
        for y in range(self.rowsize, self.height + 1, self.rowsize):
            pg.draw.line(self.WIN, GREY, (0, y), (self.width, y))

    def draw_boid(self, boid):
        pg.draw.polygon(self.WIN, boid.color, boid.points)

    def draw_neighbor(self, boid, other):
        if boid.highlight:
            pg.draw.line(self.WIN, RED, boid.center, other.center, 5)

    def draw_grouping(self, boid, other):
        if boid.highlight:
            pg.draw.line(self.WIN, GREEN, boid.center, other.center)
            rect = pg.Rect((int(boid.center[0]//100) - 1) * 100, (int(boid.center[1]//100) -1) * 100, 300, 300)
            pg.draw.rect(self.WIN, GREEN, rect, 3)

    def draw_vector(self, boid):
        if boid.highlight:
            pg.draw.circle(self.WIN, RED, boid.center, boid.vision, width=1)
            pg.draw.line(self.WIN, GREEN, boid.center, boid.dest_card, 1)

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

test = [(500, 500), (450, 500), (500, 450)]

# Initialize empty grouping array
# number of grid boxes
for x in range(100):
    grouping.append([])

print(len(grouping), "grouping")

lastboid = None

for x in range(100):
    # center = x
    center = (random.randrange(0, 1000), random.randrange(0, 1000))
    # center = (500, 500)
    boid = Boid(center)
    # pg.draw.circle(screen.WIN, RED, (500, 500), 15)
    # screen.draw_boid(boid)
    screen.rotate_boid(boid, random.randrange(0, 360))
    lastboid = boid

lastboid.color = RED
lastboid.highlight = True

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
        screen.draw_grid()
        screen.draw_vector(boid)

    pg.display.update()
    time.sleep(1/FPS)
