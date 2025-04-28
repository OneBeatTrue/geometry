import matplotlib.pyplot as plt
from random import uniform

import numpy as np

from affine import Affine
from stack import Stack

eps = 8


class Point(object):
    def __init__(self, x, y):
        self.x = round(x, eps)
        self.y = round(y, eps)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

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

    def get_distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


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


class Segment(object):
    def __init__(self, p1, p2):
        self.p1 = min(p1, p2)
        self.p2 = max(p1, p2)

    def __eq__(self, other):
        return self.p1 == other.p1 and self.p2 == other.p2 or self.p1 == other.p2 and self.p2 == other.p1

    def __lt__(self, other):
        return (self.p1.x, self.p1.y, self.p2.x, self.p2.y) < (other.p1.x, other.p1.y, other.p2.x, other.p2.y)

    def draw(self, color='black'):
        plt.plot([self.p1.x, self.p2.x], [self.p1.y, self.p2.y], color=color, zorder=1)

    def to_str(self):
        return self.p1.to_str() + " " + self.p2.to_str()

    def get_line(self):
        a = self.p2.y - self.p1.y
        b = self.p1.x - self.p2.x
        c = self.p2.x * self.p1.y - self.p2.y * self.p1.x
        return a, b, c

    def get_vect(self):
        a = self.p1.x - self.p2.x
        b = self.p1.y - self.p2.y
        return a, b

    def get_length(self):
        return self.p1.get_distance(self.p2)

    def contain(self, point):
        a, b, c = self.get_line()
        return (min(self.p1.x, self.p2.x) <= point.x <= max(self.p1.x, self.p2.x) and
                min(self.p1.y, self.p2.y) <= point.y <= max(self.p1.y, self.p2.y) and
                abs(round(a * point.x + b * point.y + c, eps)) <= 10 ** -(eps - 1))

    def intersect_a(self, other):
        a1, b1, c1 = self.get_line()
        a2, b2, c2 = other.get_line()
        if round(a1 * b2 - b1 * a2, eps) != 0:
            intersection_point = Point(
                    (b1 * c2 - c1 * b2) / (a1 * b2 - b1 * a2),
                    (c1 * a2 - a1 * c2) / (a1 * b2 - b1 * a2)
                )
            if self.contain(intersection_point) and other.contain(intersection_point):
                return intersection_point
        return None

    def intersect_b(self, other):
        s = Vector(self.p1, self.p2)
        r1 = Vector(s.p1, other.p1)
        r2 = Vector(s.p1, other.p2)
        ps1 = s.pseudoscalar(r1) * s.pseudoscalar(r2)

        s = Vector(other.p1, other.p2)
        r1 = Vector(s.p1, self.p1)
        r2 = Vector(s.p1, self.p2)
        ps2 = s.pseudoscalar(r1) * s.pseudoscalar(r2)

        if ps1 <= 0 and ps2 <= 0:
            return self.intersect_a(other)

    def intersect(self, other):
        return self.intersect_b(other)

    def intersect_vertical(self, x):
        if self.p1.x == self.p2.x:
            return self.p1.y
        t = (x - self.p1.x) / (self.p2.x - self.p1.x)
        return Point(x, self.p1.y + t * (self.p2.y - self.p1.y)).y


class HorizontalRightRay(object):
    def __init__(self, point):
        self.point = point

    def intersect(self, segment):
        if segment.contain(self.point):
            return self.point
        return Segment(self.point, Point(max(segment.p1.x, segment.p2.x, self.point.x) + 1, self.point.y)).intersect(segment)


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

    def draw(self, color='black'):
        x = 100
        if self.b != 0:
            Segment(Point(x, - (self.a * x + self.c) / self.b), Point(-x, - (self.a * x + self.c) / self.b)).draw(color=color)
        else:
            Segment(Point(-self.c / self.a, x), Point(-self.c / self.a, -x)).draw(color=color)


class Polygon(object):

    def __init__(self, points):
        self.points = points

    def draw(self, color="black"):
        for first_point, second_point in zip(self.points, self.points[1:] + [self.points[0]]):
            Segment(first_point, second_point).draw(color)

    def draw_points(self, color="black"):
        for point in self.points:
            point.draw(color=color)

    def intersect(self, other):
        intersection = self.points
        name = 1
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
                self.draw("grey")
                other.draw("grey")
                Polygon(intersection).draw("purple")
                line.draw("black")

                s.draw("black")
                Polygon(new_intersection).draw_points("green")

                plt.axis('equal')
                plt.xlim(-20, 20)
                plt.ylim(-20, 20)
                plt.grid(True, alpha=0.2)
                plt.savefig("png/" + str(name) + ".png")
                plt.clf()
                name += 1

                if s_value <= 0:
                    new_intersection.append(s)
                    first_point_color = "green"
                else:
                    first_point_color = "red"

                self.draw("grey")
                other.draw("grey")
                Polygon(intersection).draw("purple")
                line.draw("black")

                s.draw(first_point_color)
                Polygon(new_intersection).draw_points("green")

                plt.axis('equal')
                plt.xlim(-20, 20)
                plt.ylim(-20, 20)
                plt.grid(True, alpha=0.2)
                plt.savefig("png/" + str(name) + ".png")
                plt.clf()
                name += 1

                self.draw("grey")
                other.draw("grey")
                Polygon(intersection).draw("purple")
                line.draw("black")

                Segment(s, t).draw("black")
                s.draw(first_point_color)
                t.draw("black")
                Polygon(new_intersection).draw_points("green")

                plt.axis('equal')
                plt.xlim(-20, 20)
                plt.ylim(-20, 20)
                plt.grid(True, alpha=0.2)
                plt.savefig("png/" + str(name) + ".png")
                plt.clf()
                name += 1


                if s_value * t_value < 0:
                    intersection_point = line.intersection(Line(s, t))
                    new_intersection.append(intersection_point)
                    self.draw("grey")
                    other.draw("grey")
                    Polygon(intersection).draw("purple")
                    line.draw("black")

                    Segment(s, t).draw("black")
                    s.draw(first_point_color)
                    t.draw("black")
                    Polygon(new_intersection).draw_points("green")

                    plt.axis('equal')
                    plt.xlim(-20, 20)
                    plt.ylim(-20, 20)
                    plt.grid(True, alpha=0.2)
                    plt.savefig("png/" + str(name) + ".png")
                    plt.clf()
                    name += 1
                else:
                    self.draw("grey")
                    other.draw("grey")
                    Polygon(intersection).draw("purple")
                    line.draw("black")

                    Segment(s, t).draw("black")
                    s.draw(first_point_color)
                    t.draw("red")
                    Polygon(new_intersection).draw_points("green")

                    plt.axis('equal')
                    plt.xlim(-20, 20)
                    plt.ylim(-20, 20)
                    plt.grid(True, alpha=0.2)
                    plt.savefig("png/" + str(name) + ".png")
                    plt.clf()
                    name += 1

            self.draw("grey")
            other.draw("grey")
            Polygon(intersection).draw("purple")
            line.draw("black")
            Polygon(new_intersection).draw("green")

            plt.axis('equal')
            plt.xlim(-20, 20)
            plt.ylim(-20, 20)
            plt.grid(True, alpha=0.2)
            plt.savefig("png/" + str(name) + ".png")
            plt.clf()
            name += 1
            intersection = new_intersection

        self.draw("grey")
        other.draw("grey")
        Polygon(intersection).draw("green")

        plt.axis('equal')
        plt.xlim(-20, 20)
        plt.ylim(-20, 20)
        plt.grid(True, alpha=0.2)
        plt.savefig("png/" + str(name) + ".png")
        plt.clf()
        name += 1
        return Polygon(intersection)

arr = [
    [-5, 5, 1],
    [-5, -15, 1],
    [25, -15, 1],
    [25, 5, 1]
]
first = Polygon([Point(i[0], i[1]) for i in arr])
affine = Affine()
arr = affine.Ta([5, -5], affine.Ro(np.pi * 3 / 2 - np.pi / 4 - np.pi / 7, arr))
second = Polygon([Point(i[0], i[1]) for i in arr])
second.intersect(first)
#plt.show()


# def plot_voronoi_diagram(diagram, edges):
#     fig, ax = plt.subplots(figsize=(8,8))
#     pts = np.array([[cell.point.x, cell.point.y] for cell in diagram.cells])
#     ax.scatter(pts[:,0], pts[:,1], color='blue', zorder=5)
#     for cell in diagram.cells:
#         poly = [[point.x, point.y] for point in cell.polygon.cells]
#         if len(poly) > 0:
#             poly = np.array(poly)
#             ax.plot(np.append(poly[:,0], poly[0,0]), np.append(poly[:,1], poly[0,1]), 'k-', lw=1)
#             ax.fill(poly[:,0], poly[:,1], alpha=0.2)
#     edges = np.array([[point.x, point.y] for point in edges.cells])
#     ax.plot(np.append(edges[:,0], edges[0,0]), np.append(edges[:,1], edges[0,1]), 'r--', lw=1)
#     ax.set_xlim(np.min(edges[:,0]), np.max(edges[:,0]))
#     ax.set_ylim(np.min(edges[:,1]), np.max(edges[:,1]))
#     plt.show()