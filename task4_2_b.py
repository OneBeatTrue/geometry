import matplotlib.pyplot as plt
from shapes import Point, Polygon

# cells = [
#     Point(2, 0),
#     Point(6, 0),
#     Point(8, 1),
#     Point(7, 5),
#     Point(1, 6),
#     Point(0, 3),
#     Point(1, 1),
# ]
#
#
# points_to_check = [
#     Point(6, 3),
#     Point(8, 5),
# Point(1, 5),
# ]

# cells = [
#     Point(1, 1),
#     Point(2, 2),
#     Point(4, 0),
#     Point(4, 1),
#     Point(5, 1),
#     Point(6, 0),
#     Point(6, 4),
#     Point(4, 6),
#     # Point(3.7, 4),
#     # Point(3.5, 4),
#     # Point(3, 4),
#     # Point(5, 4),
#     Point(2, 4),
#     Point(0, 6),
# ]
#
#
# points_to_check = [
#     Point(1.5, 4),
#     Point(3.5, 5),
#     Point(4, 1),
# ]

points = [
    Point(1, 1),
    Point(2, 2),
    Point(4, 0),
    Point(6, 4),
    Point(4, 6),
    Point(2, 4),
    Point(0, 6),
]


points_to_check = [
    Point(1.5, 4.2),
    Point(3.5, 5),
    Point(4.5, 1),
]

polygon = Polygon(points)
polygon.draw()
for point in points_to_check:
    if polygon.is_inside_by_ray_method(point):
        point.highlight()
    else:
        point.lowlight()

plt.axis('equal')
plt.grid(True)
plt.show()