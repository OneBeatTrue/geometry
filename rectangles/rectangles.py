import pygame
import sys
import asyncio
from math import pi, cos, sin


class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, v):
        if not isinstance(v, Vertex):
            return NotImplemented
        return Vertex(self.x + v.x, self.y + v.y)

    def __sub__(self, v):
        if not isinstance(v, Vertex):
            return NotImplemented
        return Vertex(self.x - v.x, self.y - v.y)

    def __call__(self):
        return [self.x, self.y]

    def rotate(self, angle, v):
        if not isinstance(v, Vertex):
            return NotImplemented
        angle = pi * angle / 180
        return Vertex(v.x + (self.x - v.x) * cos(angle) - (self.y - v.y) * sin(angle),
                      v.y + (self.x - v.x) * sin(angle) + (self.y - v.y) * cos(angle))


class Line:
    # ax + by + c = 0
    def __init__(self, v1, v2):
        self.a = v2.y - v1.y
        self.b = v1.x - v2.x
        self.c = v2.x * v1.y - v2.y * v1.x

    def __call__(self, p):
        return self.a * p.x + self.b * p.y + self.c

    def intersection(self, other):
        if not isinstance(other, Line):
            return NotImplemented
            return Vertex(
                (self.b * other.c - self.c * other.b) / (self.a * other.b - self.b * other.a),
                (self.c * other.a - self.a * other.c) / (self.a * other.b - self.b * other.a)
            )


def get_rectangle_vertices(cx, cy, width, height):
    return (
        Vertex(cx, cy) + Vertex(- width / 2, - height / 2),
        Vertex(cx, cy) + Vertex(+ width / 2, - height / 2),
        Vertex(cx, cy) + Vertex(+ width / 2, + height / 2),
        Vertex(cx, cy) + Vertex(- width / 2, + height / 2)
    )

def get_triangle_vertices(cx, cy, a, b, c):
    return (
        Vertex(cx, cy - a),
            Vertex(cx, cy - b).rotate(120, Vertex(cx, cy)),
        Vertex(cx, cy - c).rotate(240, Vertex(cx, cy))
    )

def get_area(poly):
    for v in poly:
        if not isinstance(v, Vertex):
            return NotImplemented
    if len(poly) <= 2:
        return 0
    return sum(p.x * q.y - p.y * q.x for p, q in zip(poly, poly[1:] + poly[:1])) / 2

def intersect(poly1, poly2):
    intersection = poly1

    # Проходим по всем ребрам второго прямоугольника
    for p, q in zip(poly2, poly2[1:] + poly2[:1]):
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

    return intersection

pygame.init()

# Размеры окна
width, height = 800, 600

# Цвета
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
purple = (128, 0, 128)
white = (255, 255, 255)

# Создание окна
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Modeling")

# Инициализация шрифта
pygame.font.init()
my_font = pygame.font.SysFont('Times New Roman', 30)

# Открытие файла для записи
# file = open('output.txt', 'w')

async def main():
    # Описание системы
    # plate_a, plate_b, plate_c = 0.1, 0.2, 0.3
    # dielectric_a, dielectric_b, dielectric_c = 0.4, 0.015, 0.05
    plate_width, plate_height = 0.150, 0.200
    dielectric_width, dielectric_height = 0.150, 0.200
    eps = 4.3
    eps0 = 8.8541878128
    d = 0.2
    h = 0.05
    angle_speed = pi

    center_x, center_y = width // 2, height // 2
    rotation_angle = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Очистка экрана
        screen.fill(black)

        # Преобразуем параметры в точки
        # plate = get_triangle_vertices(center_x, center_y, plate_a * 1000, plate_b * 1000, plate_c * 1000)
        # dielectric = tuple([i.rotate(rotation_angle, Vertex(center_x, center_y)) for i in
        #                     get_triangle_vertices(center_x, center_y, dielectric_a * 1000, dielectric_b * 1000, dielectric_c * 1000)])
        plate = get_rectangle_vertices(center_x, center_y, plate_width * 1000, plate_height * 1000)
        dielectric = tuple([i.rotate(rotation_angle, Vertex(center_x, center_y)) for i in
                            get_rectangle_vertices(center_x, center_y, dielectric_width * 1000, dielectric_height * 1000)])

        # Расчет области пересечения
        intersection = intersect(plate, dielectric)

        # Расчет площадей обкладок, и площади области пересечения
        intersection_area = get_area(intersection) / 1000 ** 2
        plate_area = get_area(plate) / 1000 ** 2

        # Расчет емкости конденсатора
        capacity = intersection_area * (eps * eps0 / (eps * (d - h) + h) - eps0 / d) + eps0 * plate_area / d

        # Вращение
        rotation_angle = (rotation_angle + 1) % 360

        # Отрисовка
        pygame.draw.polygon(screen, blue, [i() for i in plate])
        pygame.draw.polygon(screen, red, [i() for i in dielectric])
        pygame.draw.polygon(screen, purple, [i() for i in intersection])
        screen.blit(my_font.render('Intersection area = {:f} m²'.format(intersection_area), True, white), (20, 20))
        screen.blit(my_font.render('Capacity = {:f} pF'.format(capacity), True, white), (20, 60))

        # Запись значения в файл
        # file.write(str(capacity) + '\n')

        # Обновление экрана
        pygame.display.flip()

        # Задержка для управления скоростью вращения
        pygame.time.Clock().tick(angle_speed * 180 / pi)
        await asyncio.sleep(0)

asyncio.run(main())