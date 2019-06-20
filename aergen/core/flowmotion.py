from aergen.core.direction import EntityDirection
from aergen.core.texture   import Texture
from aergen.core.path      import EntityDirectionItemPath
from aergen.core.path      import EntityPath
from aergen.core.input     import EntityInput

from enum import Enum

import math
import sys
import matplotlib.pyplot as plt
import numpy             as np
import copy              as cpy
import bisect            as bs
import sortedcontainers  as sc


class PixelPositionRandomGenerator(object):
    def __init__(self, dim_texture, random_int_fct):
        self.width_texture  = dim_texture[0]
        self.height_texture = dim_texture[1]        
        self.random_int_fct = random_int_fct

    def compute(self):
        x = self.random_int_fct(self.width_texture)
        y = self.random_int_fct(self.height_texture)
        return x, y


class PixelTimeRandomGenerator(object):
    def __init__(self, tmin, tmax, random_int_fct):
        self.tmin = tmin
        self.tmax = tmax
        self.random_int_fct = random_int_fct

    def compute(self):
        return self.random_int_fct(self.tmin, self.tmax)


class FlowMotionTexture(Texture):
    def __init__(self, x, y, dim_texture, npixel_per_tick, gen_pos, gen_time):
        Texture.__init__(self, x, y)
        self.set_npixel_per_tick(npixel_per_tick)
        self.gen_pos  = gen_pos
        self.gen_time = gen_time
        self.width_texture  = dim_texture[0]
        self.height_texture = dim_texture[1]

        self.texture_matrix = [[0] * self.width_texture for _ in range(self.height_texture)]
        self.texture_pixels = sc.SortedList([], key=lambda x: -x[2])

        self.clk_npixel = 0
        self.npixel = 0

        self.init_texture()

        return

    def set_npixel_per_tick(self, npixel_per_tick):
        self._npixel_per_tick = npixel_per_tick
        if isinstance(npixel_per_tick, int):
            self.npixel_per_tick = npixel_per_tick
            return
        
        a, b, _ = npixel_per_tick

        self.npixel_per_tick = np.random.randint(a, b)
        return 

    def update_npixel_per_tick(self):
        if isinstance(self._npixel_per_tick, int):
            return

        a, b, clk_npixel = self._npixel_per_tick

        if self.clk_npixel > clk_npixel:
            self.npixel_per_tick = np.random.randint(a, b)
            self.clk_npixel = 0
            return
        
        self.clk_npixel += 1
        return

    def init_texture(self):
        self.new_pixels(self.npixel_per_tick)

    def new_pixels(self, npixel):
        '''
        npixel (int) : number of new pixel (the parameter is not checked)
        '''
        cpt_pixel = 0
        while cpt_pixel < npixel:
            x, y = self.gen_pos.compute()

            if self.texture_matrix[y][x] > 0:
                continue

            self.texture_matrix[y][x] = self.gen_time.compute() 
            self.texture_pixels.add((x,y,self.texture_matrix[y][x]))
            cpt_pixel += 1

    def del_pixels(self, npixel):
        for _ in range(npixel):
            x, y, _ = self.texture_pixels.pop()
            self.texture_matrix[y][x] = 0
        return
        
    
    def update(self):
        pass


    def move(self, dir, mvt, time, no_move=True):
        if no_move and mvt == 0:
            return False

        pos = self.position + dir.direction * mvt
        return self.env.put(self, pos, time)


class FlowMotionInput():
    def __init__(self, texture, path, dim, sample, vel, length=None,
                 is_tor=False, outside=False, builded=True):
        self.texture = texture
        self.vel = vel

        self.sample = sample
        self.width  = dim[0]
        self.height = dim[1]

        self.is_tor = is_tor
        self.outside = outside

        if not isinstance(path, EntityPath):
            path = EntityPath(path=path, env=self)

        self.__path = path

        self.indices = []
        self.times = []
        # self.pathra nge = []

        self.length = length

        self.shape_id = texture.shape_id

        texture.env = self

        if builded:
            self.build()
        return


    def put(self, texture, pos, time):
        def put_elm(elm, is_texture=False):
            if self.is_tor:
                elm[0] = elm[0] % self.width  # x
                elm[1] = elm[1] % self.height  # y

            elif elm[0] >= self.width or elm[0] < 0 or \
                    elm[1] >= self.height or elm[1] < 0:
                return False

            if not is_texture:
                self.put_spike(elm[0], elm[1], time)
            return True
        pos_e = np.copy(pos)
        status = put_elm(pos_e, is_texture=True)
        if status or self.outside:
            texture.position = pos_e

        status = True
        for yi in range(len(texture.shape)):
            for xi in range(len(texture.shape[yi])):
                if texture.shape[yi][xi]:
                    pixel = pos + np.array([xi, yi])
                    status = status and put_elm(pixel)

        return status

    def build(self):
        self.indices = []
        self.times   = []

        mvf = self.vel / self.sample
        mvi = math.floor(mvf)
        epsilon = mvf - mvi
        acc = 0
        ts = 0  # Microseconds
        delta = round(1/self.sample * 1000, 5)

        for ei in self.path:
            n = int(ei.time * self.sample)

            if ei.direction == EntityDirection.JUMP:
                ts = round(ts + n, 5)
                continue

            for _ in range(n):
                mvt = mvi
                if acc > 1:
                    acc -= math.floor(acc)
                    mvt += 1

                self.texture.move(ei.direction, mvt, ts)

                ts = round(ts + delta, 5)
                acc += epsilon  # MOUAIS
        return



