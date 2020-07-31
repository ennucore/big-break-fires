import numpy as np
import attr
import settings
import cv2
from random import uniform
from typing import Optional, List
from itertools import chain


def get_fire_color(rate):
    return 0, 5 * rate, 255 * rate


@attr.s(auto_attribs=True)
class Field:
    field: np.array
    propagation: float
    contour: Optional[np.array] = None
    deviation: float = 0.2

    @classmethod
    def from_focus(cls, shape, fire=settings.DEFAULT_FIRE_FOCUS, propagation=settings.PROPAGATION):
        field = np.zeros(shape)
        field[shape[0] // 2][shape[1] // 2] = fire
        return cls(field=field, propagation=propagation)

    @property
    def height(self):
        return len(self.field)

    @property
    def width(self):
        return len(self.field[0])

    @property
    def cnt(self):
        if self.contour is not None:
            return self.contour
        else:
            contours, _ = cv2.findContours(
                self.get_image(True),
                cv2.RETR_CCOMP,
                cv2.CHAIN_APPROX_SIMPLE)
            self.contour = max(contours, key=cv2.contourArea) if contours else None
            return self.contour

    def get_grad_in_point(self, i, j):
        return (self[i + 1, j] - self[i - 1, j]) ** 2 + (self[i, j + 1] - self[i, j - 1]) ** 2

    def tick(self):
        new_field = self.field.copy()
        for i in range(self.field.shape[0]):
            for j in range(self.field.shape[1]):
                neighborhood = [(i2, j2) for i2, j2 in self.neighborhood_iter(i, j) if (i2, j2) != (i, j)]
                neighborhood_average = sum(
                    self.field[i2, j2]
                    for i2, j2 in neighborhood
                ) / len(neighborhood)
                new_field[i, j] = min(
                    1,
                    (self.field[i, j] +
                     max((neighborhood_average - self.field[i, j]) * self.propagation * uniform(1 - self.deviation,
                                                                                                1 + self.deviation),
                         0)) * uniform(1 - self.deviation, 1 + self.deviation)
                )
                if new_field[i, j] < 0.008:
                    new_field[i, j] = 0
                if self.field[i, j] == 1 and neighborhood_average == 1 and uniform(0, 1) > 0.8:
                    new_field[i, j] = 0
        self.field = new_field
        self.contour = None

    def get_image(self, bool_img=False):
        mat = []
        for i in range(self.width):
            row = []
            for j in range(self.height):
                row.append(get_fire_color(self[i, j]) if not bool_img else int(bool(self[i, j])))
            mat.append(row)
        mat = np.array(mat)
        return mat

    def __setitem__(self, key, value):
        self.field.__setitem__(key, value)

    def __getitem__(self, item):
        return self.field.__getitem__(item)

    def __iter__(self):
        for i in range(self.field.shape[0]):
            for j in range(self.field.shape[1]):
                yield i, j

    def neighborhood_iter(self, x0, y0):
        for x in range(round(x0 - 1), round(x0 + 2)):
            for y in range(round(y0 - 1), round(y0 + 2)):
                if 0 <= x < self.width and 0 <= y < self.height:
                    yield x, y

    def score(self):
        return sum(chain(*self.field))
