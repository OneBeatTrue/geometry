from itertools import combinations
import matplotlib.pyplot as plt
from random import uniform

eps = 8


class Point(object):
    def __init__(self, x, y):
        self.x = round(x, eps)
        self.y = round(y, eps)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @staticmethod
    def get_random(x_min, x_max, y_min, y_max):
        x = round(uniform(x_min, x_max), eps)
        y = round(uniform(y_min, y_max), eps)
        return Point(x, y)

    def draw(self, color='black'):
        plt.scatter(self.x, self.y, color=color, zorder=2)

    def to_str(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def highlight(self):
        plt.scatter(self.x, self.y, color='#66ff00', zorder=3)

    def lowlight(self):
        plt.scatter(self.x, self.y, color='red', zorder=3)


class Segment(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __eq__(self, other):
        return self.p1 == other.p1 and self.p2 == other.p2 or self.p1 == other.p2 and self.p2 == other.p1

    def draw(self, color='black'):
        plt.plot([self.p1.x, self.p2.x], [self.p1.y, self.p2.y], color=color, zorder=1)

    def to_str(self):
        return self.p1.to_str() + " " + self.p2.to_str()


class Vector(object):
    def __init__(self, p1, p2):
        self.x = p1.x - p2.x
        self.y = p1.y - p2.y
        self.p1 = p1
        self.p2 = p2

    def reverse(self):
        self.x, self.y, self.p1, self.p2 = -self.x, -self.y, self.p2, self.p1

    def pseudoscalar(self, other):
        return self.x * other.y - self.y * other.x

    def abs(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def sin(self, other):
        if self.abs() * other.abs() == 0:
            return None
        return self.pseudoscalar(other) / (self.abs() * other.abs())

    def cos(self, other):
        if self.abs() * other.abs() == 0:
            return None
        return (self.x * other.x + self.y * other.y) / (self.abs() * other.abs())

    def get_angle_info(self, other):
        return (self.pseudoscalar(other) < 0, self.cos(other) if self.pseudoscalar(other) < 0 else -self.cos(other))


class Line:
    # ax + by + c = 0
    def __init__(self, p1, p2):
        self.a = p2.y - p1.y
        self.b = p1.x - p2.x
        self.c = p2.x * p1.y - p2.y * p1.x

    def __call__(self, p):
        return self.a * p.x + self.b * p.y + self.c

    def intersection(self, other):
        return Point(
            (self.b * other.c - self.c * other.b) / (self.a * other.b - self.b * other.a),
            (self.c * other.a - self.a * other.c) / (self.a * other.b - self.b * other.a)
        )


class Polygon(object):
    def __init__(self, points):
        self.points = points
        self.kernel = Point(sum([point.x for point in points]) / len(points), sum([point.y for point in points]) / len(points))

    @staticmethod
    def get_coverage(points):
        coverage = [min(points, key=lambda p: (p.y, -p.x))]
        current_vector = Vector(coverage[0], Point(coverage[0].x, coverage[0].y - 1))
        while True:
            max_angle_vect = None
            for point in filter(lambda p: p != current_vector.p1 and p != current_vector.p2, points):
                vect = Vector(current_vector.p1, point)
                if max_angle_vect is None or current_vector.get_angle_info(vect) < current_vector.get_angle_info(max_angle_vect):
                    max_angle_vect = vect

            if max_angle_vect.p2 == coverage[0]:
                break

            max_angle_vect.reverse()
            current_vector = max_angle_vect
            coverage.append(max_angle_vect.p1)

        return Polygon(coverage)

    def draw(self, color="black"):
        for first_point, second_point in zip(self.points, self.points[1:] + [self.points[0]]):
            Segment(first_point, second_point).draw(color)

    def fill(self, color="black"):
        x, y = zip(*[(p.x, p.y) for p in self.points])
        plt.fill(x, y, color=color)

    def draw_kernel(self):
        plt.scatter(self.kernel.x, self.kernel.y, color='blue', zorder=2)
        for point in self.points:
            Segment(self.kernel, point).draw()

    def is_inside(self, point):
        q_vect = Vector(self.kernel, point)
        for first_point, second_point in zip(self.points, self.points[1:] + [self.points[0]]):
            first_vect = Vector(self.kernel, first_point)
            second_vect = Vector(self.kernel, second_point)
            if q_vect.pseudoscalar(first_vect) * q_vect.pseudoscalar(second_vect) <= 0:
                new_vect = Vector(first_point, second_point)
                first_vect = Vector(first_point, self.kernel)
                second_vect = Vector(first_point, point)
                if new_vect.pseudoscalar(first_vect) * new_vect.pseudoscalar(second_vect) < 0:
                    return False
        return True

    def intersect(self, other):
        intersection = self.points

        # Проходим по всем ребрам второго прямоугольника
        for p, q in zip(other.points, other.points[1:] + other.points[:1]):
            if len(intersection) <= 2:
                break

            line = Line(p, q)

            # Любая точка p с line(p) <= 0 находится внутри или на границе
            # Любая точка p с line(p) > 0  находится снаружи

            # Проходим по всем ребрам пересечения
            new_intersection = []
            line_values = [line(t) for t in intersection]
            for s, t, s_value, t_value in zip(
                    intersection, intersection[1:] + intersection[:1],
                    line_values, line_values[1:] + line_values[:1]):
                if s_value <= 0:
                    new_intersection.append(s)
                if s_value * t_value < 0:
                    intersection_point = line.intersection(Line(s, t))
                    new_intersection.append(intersection_point)

            intersection = new_intersection

        return Polygon(intersection)


size = 20
range_x, range_y = size, size
x_min, x_max, y_min, y_max = -range_x / 2, range_x / 2, -range_y / 2, range_y / 2

n = 16
points = [Point.get_random(x_min, x_max, y_min, y_max) for _ in range(n)]

first_points = points[:n // 2]
first_polygon = Polygon.get_coverage(first_points)
first_polygon.fill("#ff808a")
first_polygon.draw("red")
for point in first_points:
    point.draw("#8b0000")

second_points = points[n // 2:]
second_polygon = Polygon.get_coverage(second_points)
second_polygon.fill("#a6caf0")
second_polygon.draw("blue")
for point in second_points:
    point.draw("#00406b")

intersection = first_polygon.intersect(second_polygon)
intersection.fill("#876c99")
intersection.draw("purple")
for point in points:
    if intersection.is_inside(point):
        point.draw("#462036")


plt.axis('equal')
plt.grid(True)
plt.show()
