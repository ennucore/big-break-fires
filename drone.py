import attr
from math import hypot, atan2
import settings
from field import Field
from random import uniform, choice
import typing


def choose_nearest_from_neighborhood(x0, y0, x, y):
    dx, dy = x - x0, y - y0
    delta = [
        (1, 0),
        (1, 1),
        (0, 1),
        (-1, 1),
        (-1, 0),
        (-1, -1),
        (0, -1),
        (1, -1)
    ][int(atan2(dy, dx) / 0.7853981633974483)]
    return x0 + delta[0], y0 + delta[1]


@attr.s(auto_attribs=True)
class Drone:
    x: float
    y: float
    speed: float = settings.DEFAULT_SPEED
    quenching_speed: float = settings.DEFAULT_QUENCHING_SPEED
    quenching_radius: float = settings.DEFAULT_QUENCHING_RADIUS
    destination: typing.Optional[typing.Tuple[float, float]] = None

    @classmethod
    def random(cls, field: Field, max_deviation=0.25):
        def deviation():
            return uniform(1 - max_deviation, 1 + max_deviation)

        return cls(
            x=uniform(0, field.width),
            y=uniform(0, field.height),
            speed=settings.DEFAULT_SPEED * deviation(),
            quenching_speed=settings.DEFAULT_QUENCHING_SPEED * deviation(),
            quenching_radius=settings.DEFAULT_QUENCHING_RADIUS * deviation()
        )

    def tick(self, field: Field):
        for i in range(
                max(0, int(self.x - 2 - self.quenching_radius)),
                min(field.width, int(self.x + 2 + self.quenching_radius))):
            for j in range(
                    max(0, int(self.y - 2 - self.quenching_radius)),
                    min(field.height, int(self.y + 2 + self.quenching_radius))):
                if hypot(self.x - i, self.y - i) < self.quenching_radius:
                    field[i, j] = field[i, j] - self.quenching_speed

        if self.destination:
            dx, dy = self.destination[0] - self.x, self.destination[1] - self.y
            self.x, self.y = self.x + self.speed * dx / hypot(dx, dy), self.y + self.speed * dy / hypot(dx, dy)
