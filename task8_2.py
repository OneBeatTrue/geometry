from  task6_1_2 import *
from shapes import Point


size = 20
range_x, range_y = size, size
x_min, x_max, y_min, y_max = -range_x / 2, range_x / 2, -range_y / 2, range_y / 2

n = 10
points = [Point.get_random(x_min, x_max, y_min, y_max) for _ in range(n)]
multiplier = 100

edges = Polygon([
    Point(multiplier * x_min, multiplier * y_min),
    Point(multiplier * x_max, multiplier * y_min),
    Point(multiplier * x_max, multiplier * y_max),
    Point(multiplier * x_min, multiplier * y_max),
])
diagram = build_voronoi_diagram(points, edges)

plt.figure(figsize=(10, 10))


visual_multiplier = 1.5
plt.xlim(visual_multiplier * x_min, visual_multiplier * x_max)
plt.ylim(visual_multiplier * y_min, visual_multiplier * y_max)
plt.show()