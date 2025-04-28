import matplotlib.pyplot as plt
from random import uniform
from stack import Stack

eps = 8


class Point(object):
    def __init__(self, x, y):
        self.x = round(x, eps)
        self.y = round(y, eps)

    def __eq__(self, other):
        return abs(self.x - other.x) <= 10 ** -(eps - 1) and abs(self.y - other.y) <= 10 ** -(eps - 1)

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

    def midpoint(self, other):
        return Point((self.x + other.x) / 2, (self.y + other.y) / 2)


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

    def mid_perpendicular(self):
        mid = self.p1.midpoint(self.p2)
        a, b, c = self.get_line()
        return Line.instance(-b, a, - a * mid.y + b * mid.x)
        # a = self.p2.x - self.p1.x
        # b = self.p2.y - self.p1.y
        # c = a * mid.x + b * mid.y
        # return Line.instance(a, b, c)

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

    @staticmethod
    def instance(a, b, c):
        line = Line(Point(0, 0), Point(0, 0))
        line.a = a
        line.b = b
        line.c = c
        return line

    def intersection(self, other):
        return Point(
            (self.b * other.c - self.c * other.b) / (self.a * other.b - self.b * other.a),
            (self.c * other.a - self.a * other.c) / (self.a * other.b - self.b * other.a)
        )

    def inverted(self):
        return Line.instance(-self.a, -self.b, -self.c)


class Polygon(object):

    def __init__(self, points):
        self.points = points
        self.kernel = 0
        if len(points) != 0:
            self.kernel = Point(sum([point.x for point in points]) / len(points), sum([point.y for point in points]) / len(points))

    def __copy__(self):
        return Polygon(self.points.copy())

    def draw(self, color="black"):
        if len(self.points) == 0:
            return
        for first_point, second_point in zip(self.points, self.points[1:] + [self.points[0]]):
            Segment(first_point, second_point).draw(color)

    def fill(self, color="black"):
        if len(self.points) == 0:
            return
        x, y = zip(*[(p.x, p.y) for p in self.points])
        plt.fill(x, y, color=color)


    def draw_kernel(self):
        plt.scatter(self.kernel.x, self.kernel.y, color='blue', zorder=2)
        for point in self.points:
            Segment(self.kernel, point).draw()

    def is_inside_by_angle_method(self, point):
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

    def is_inside_by_ray_method(self, point):
        q_ray = HorizontalRightRay(point)
        intersections = []
        segments = []
        all_segments = []
        for first_point, second_point in zip(self.points, self.points[1:] + self.points[0:1]):
            segment = Segment(first_point, second_point)
            all_segments.append(segment)
            if segment.contain(point):
                return True
            intersection = q_ray.intersect(segment)
            if intersection is not None:
                intersections.append(intersection)
                segments.append(segment)

        if len(intersections) < 2:
            return len(intersections) % 2 == 1

        pairs = [tuple([intersection, segment]) for intersection, segment in zip(intersections, segments)]
        cycle_check = len(pairs) != 2 and (pairs[0][0] == pairs[-1][0] or (Segment(pairs[0][0], pairs[-1][0]) in all_segments))
        # циклическая проверка нужна в случае если обход сторон разорвал последовательные точки пересечения
        count = not cycle_check
        # в случае если не требуется циклическая проверка посследнюю точку положим сразу
        for i in range(len(pairs) - (not cycle_check)):
            first_point, first_segment, second_point, second_segment = pairs[i][0], pairs[i][1], pairs[(i + 1) % len(pairs)][0], pairs[(i + 1) % len(pairs)][1]
            if ((first_point != first_segment.p1 and first_point != first_segment.p2) or # если пересечение произошло не в вершине
                (max(first_segment.p1.y, first_segment.p2.y) == max(second_segment.p1.y, second_segment.p2.y) or # проверка на то лежат ли отрезки по разные стороны от луча
                 min(first_segment.p1.y, first_segment.p2.y) == min(second_segment.p1.y, second_segment.p2.y))):
                count += 1
        return count % 2 == 1

    def is_inside(self, point):
        return self.is_inside_by_ray_method(point)

    @staticmethod
    def get_coverage_jarvis(points):
        coverage = [min(points, key=lambda p: (p.y, p.x))]
        current_vector = Vector(coverage[0], Point(coverage[0].x, coverage[0].y - 1))
        while True:
            max_angle_vect = None
            for point in filter(lambda p: p != current_vector.p1 and p != current_vector.p2, points):
                vect = Vector(current_vector.p1, point)
                if max_angle_vect is None or current_vector.get_angle_info(vect) < current_vector.get_angle_info(
                        max_angle_vect):
                    max_angle_vect = vect

            if max_angle_vect.p2 == coverage[0]:
                break

            max_angle_vect.reverse()
            current_vector = max_angle_vect
            coverage.append(max_angle_vect.p1)

        return Polygon(coverage)

    @staticmethod
    def get_coverage_graham(points):
        start_point = min(points, key=lambda p: (p.y, p.x))
        current_vector = Vector(start_point, Point(start_point.x, start_point.y - 1))
        sorted_points = sorted(filter(lambda p: p != start_point, points),
                               key=lambda p: (
                                   *current_vector.get_angle_info(Vector(start_point, p)), start_point.get_distance(p)))
        queue = Stack(start_point)
        queue.push(sorted_points[0])
        for point in sorted_points[1:]:
            while Vector(queue.top(), queue.next_to_top()).pseudoscalar(Vector(queue.top(), point)) > 0:
                queue.pop()
            queue.push(point)
        return Polygon(queue.to_list())

    @staticmethod
    def get_coverage(points):
        return Polygon.get_coverage_graham(points)

    def get_perimeter(self):
        return sum([Segment(first_point, second_point).get_length() for first_point, second_point in
                    zip(self.points, self.points[1:] + [self.points[0]])])

    def get_triangle_area(self, first_point, second_point):
        a = Segment(first_point, second_point).get_length()
        b = Segment(self.kernel, first_point).get_length()
        c = Segment(self.kernel, second_point).get_length()
        p = (a + b + c) / 2
        return (p * (p - a) * (p - b) * (p - c)) ** 0.5

    def get_area(self):
        return sum([self.get_triangle_area(first_point, second_point) for first_point, second_point in
                    zip(self.points, self.points[1:] + [self.points[0]])])

    def is_intersect_line(self, line):
        line_values = [line(t) for t in self.points]
        for s, t, s_value, t_value in zip(
                self.points, self.points[1:] + self.points[:1],
                line_values, line_values[1:] + line_values[:1]):
            if s_value == 0 or s_value * t_value < 0:
                return True
        return False

    def clip(self, line):
        # Любая точка p с line(p) <= 0 находится внутри или на границе
        # Любая точка p с line(p) > 0  находится снаружи

        new_points = []
        line_values = [line(t) for t in self.points]
        # Проходим по всем ребрам многоугольника
        for s, t, s_value, t_value in zip(
                self.points, self.points[1:] + self.points[:1],
                line_values, line_values[1:] + line_values[:1]):
            if s_value <= 0:
                new_points.append(s)
            if s_value * t_value < 0:
                intersection_point = line.intersection(Line(s, t))
                new_points.append(intersection_point)

        return Polygon(new_points)

    def intersect(self, other):
        intersection = self
        # Проходим по всем ребрам второго прямоугольника и обрезаем по каждой з них
        for p, q in zip(other.points, other.points[1:] + other.points[:1]):
            if len(intersection.points) <= 2:
                break
            intersection = intersection.clip(Line(p, q))

        return intersection