import attr
import typing
from drone import Drone
from field import Field
import cv2
import numpy as np
from math import pi, sin, cos, hypot


@attr.s(auto_attribs=True)
class HiveMind:
    drones: typing.List[Drone]

    def tick(self, field: Field):
        for drone in self.drones:
            drone.tick(field)
        points = np.array([[np.array(point, dtype=int)] for point in field if field[point] > 0.01])
        if len(points) == 0:
            return
        (x, y), radius = cv2.minEnclosingCircle(points)
        points = []
        for i in range(len(self.drones)):
            point = (
                x + radius * cos(i * 2 * pi / len(self.drones)),
                y + radius * sin(i * 2 * pi / len(self.drones))
            )
            for r in range(int(radius), 1, -1):
                point = (
                    x + r * cos(i * 2 * pi / len(self.drones)),
                    y + r * sin(i * 2 * pi / len(self.drones))
                )
                try:
                    if field[int(point[0]), int(point[1])] > 0.05:
                        break
                except IndexError:
                    continue
            points.append(point)

        for drone in self.drones:
            drone.destination = None
        for point in points:
            drone = min(
                filter(lambda c_drone: c_drone.destination is None, self.drones),
                key=lambda c_drone: hypot(drone.x - point[0], drone.y - point[1])
            )
            drone.destination = point
