import attr
import numpy as np
from field import Field
from drone import Drone
from hivemind import HiveMind
import settings
from typing import List


@attr.s(auto_attribs=True)
class Model:
    field: Field
    hivemind: HiveMind
    field_log: List[np.array] = []
    drones_log: List[np.array] = []

    @classmethod
    def default(cls, field_width=settings.DEFAULT_FIELD_SIZE, field_height=settings.DEFAULT_FIELD_SIZE,
                fire_focus_strength=settings.DEFAULT_FIRE_FOCUS,
                propagation=settings.PROPAGATION, deviation=0.25, drone_number=20):
        field = Field.from_focus((field_width, field_height), fire_focus_strength, propagation)
        drones = [Drone.random(field, deviation) for _ in range(drone_number)]
        return cls(field=field, hivemind=HiveMind(drones=drones))

    def tick(self, tick_drones=True):
        self.field_log.append(self.field.field)
        self.drones_log.append([(drone.x, drone.y) for drone in self.hivemind.drones])
        if tick_drones:
            self.hivemind.tick(self.field)
        self.field.tick()

    @property
    def drones(self):
        return self.hivemind.drones
