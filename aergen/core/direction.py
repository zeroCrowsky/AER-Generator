from enum import Enum

import numpy as np

class EntityDirection(Enum):
    NORTH = (0, np.array([0,1]))
    SOUTH = (1, np.array([0,-1]))
    EAST  = (2, np.array([1,0]))
    WEST  = (3, np.array([-1,0]))

    STATIC = (4, np.array([0,0]))
    JUMP   = (5, None) # np.array = position

    def __eq__(self, d):
        if not isinstance(d, type(self)):
            return False
        return self.flag == d.flag

    @property
    def flag(self):
        return self.value[0]

    @property
    def direction(self):
        return self.value[1]

    @staticmethod
    def directions():
        return [EntityDirection.NORTH, EntityDirection.SOUTH, EntityDirection.EAST, EntityDirection.WEST]
