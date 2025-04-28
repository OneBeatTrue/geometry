import matplotlib.pyplot as plt
from task6_1_2 import build_voronoi_diagram
from shapes import Point, Polygon



size = 20
range_x, range_y = size, size
x_min, x_max, y_min, y_max = -range_x / 2, range_x / 2, -range_y / 2, range_y / 2

n = 50
points = [Point.get_random(x_min, x_max, y_min, y_max) for _ in range(n)]
multiplier = 1

edges = Polygon([
    Point(multiplier * x_min, multiplier * y_min),
    Point(multiplier * x_max, multiplier * y_min),
    Point(multiplier * x_max, multiplier * y_max),
    Point(multiplier * x_min, multiplier * y_max),
])

visual_multiplier = 1
plt.figure(figsize=(10, 10))
plt.xlim(visual_multiplier * x_min, visual_multiplier * x_max)
plt.ylim(visual_multiplier * y_min, visual_multiplier * y_max)

for name in range(100):
    diagram = build_voronoi_diagram(points, edges)

    diagram.draw()
    plt.show()
    plt.savefig("d_____vpng/" + str(name + 1) + ".png")
    points = diagram.get_relaxed()