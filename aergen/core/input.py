from aergen.core.direction import EntityDirection
from aergen.core.texture   import EntityTexture
from aergen.core.path      import EntityDirectionItemPath
from aergen.core.path      import EntityPath

from enum       import Enum
from matplotlib import cm

import math
import sys
import matplotlib.pyplot as plt
import numpy             as np
import copy              as cpy
import bisect            as bs

################ Procedure ###################
def get_elms_withtimes(times, data, start=None, end=None, retrange=False):
    begin  = 0          if start == None else bs.bisect_left(times, start)
    finish = len(times) if end == None   else bs.bisect_right(times, end)

    if retrange:
        return begin, finish
    return times[begin:finish], data[begin:finish]

def get_labels_withtimes(labels, start=None, end=None, retrange=False):
    begin = finish = 0
    tm = labels[0].time * 1000

    for l in labels:
        if tm < start:
            begin += 1
        if tm < end:
            finish += 1
        tm += l.time * 1000 # Milisecond

    if begin == finish: finish += 1

    if retrange:
        return begin, finish
    return labels[begin:finish]


def get_spikesrange_withlabels(labels, times, start, end):
    spks_labels = []
    ms = 1000
    tj, j = start, 0

    nlabels = len(labels)
    for l in labels:
        if l.direction != EntityDirection.JUMP:
            break
        tj = round(tj + round(l.time*ms, 5), 5)
        j += 1
        spks_labels.append(None)

    if j >= nlabels:
        return spks_labels

    # import ipdb; ipdb.set_trace()
    i = a = b = start # [a, b[
    tj = round(tj + round(labels[j].time*ms, 5), 5)
    for i in range(start, end):
        lj = labels[j]
        if lj.direction == EntityDirection.JUMP:
            j += 1
            tj = round(tj + round(labels[j].time*ms, 5), 5)
            spks_labels.append(None)
            continue

        ti = times[i]
        b = i
        if ti > tj:
            spks_labels.append((a, b))
            j += 1
            tj = round(tj + round(labels[j].time*ms, 5), 5)
            a = b = i

    spks_labels.append((a, b+1))

    for jj in range(j+1, nlabels): spks_labels.append(None)

    return spks_labels

class EntityInput(object):
    @staticmethod
    def empty(dim=(0, 0)):
        return EntityInput(EntityTexture(0, 0), EntityPath(path=[]), dim, 0, 0, builded=False)

    @staticmethod
    def cpy_params(inp):
        dim = (inp.width, inp.height)
        return EntityInput(inp.texture, inp.path, dim, inp.sample, inp.vel,
                           is_tor=inp.is_tor, outside=inp.outside,
                           length=inp.length, builded=False)

    @staticmethod
    def fromfactoryfile(factoryfile, paramsfile):
        return None

    @staticmethod
    def frominfile(infile):
        ent = EntityInput.empty()
        ent.load(infile)
        return ent

    @staticmethod
    def fromfile(file):
        if file.endswith('in'):
            return EntityInput.frominfile(file)
        return EntityInput.frompyfile(file)

    @staticmethod
    def fromstr(s):
        ent = EntityInput.empty()
        ent.parse(s)
        return ent

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
        self.times   = []
        # self.pathrange = []

        self.length = length

        self.shape_id = texture.shape_id

        texture.env = self

        if builded:
            self.build()
        return

    @property
    def length(self):
        return self.__length

    @length.setter
    def length(self, length):
        if length is None:
            length = self.path.length
        self.__length = round(length, 6)


    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, path):
        self.__path = path
        self.length = None


    def __str__(self):
        n     = len(self.indices)

        sep = ' '
        s = str(self.vel) + sep + str(self.sample) + sep \
          + str(self.width) + sep + str(self.height) + sep + str(self.length) + sep \
          + str(int(self.is_tor)) + sep + str(int(self.outside)) + '\n' \
          + str(self.texture) + '#\n' \
          + str(self.path) + str(n) + '\n'

        for i in range(n):
            s += str(self.indices[i]) + ' ' + str(self.times[i]) + '\n'


        return s


    def parse(self, s):
        lines = s.split('\n')

        v, s, w, h, l, is_t, o = list(map(eval, lines[0].split(' ')))

        self.vel    = v;          self.sample  = s
        self.width  = w;          self.height  = h
        self.length = l
        self.is_tor = bool(is_t); self.outside = bool(o)

        ent_str = ''
        i = 1
        while lines[i] != '#':
            ent_str += lines[i] + '\n'
            i += 1

        self.texture = EntityTexture.fromstr(ent_str);   i += 1
        self.texture.env = self
        # Path parsing
        npath = self.path.parse_header(lines[i]); i += 1
        self.path.parse(lines, start=i, npath=npath, parse_header=False); i += npath
        # Body parsing
        n = int(lines[i]); i += 1
        for j in range(i, i+n):
            idx, t = lines[j].split(' ')
            self.indices.append(int(idx))
            self.times.append(float(t))

        return


    def load(self, filename):
        with open(filename, 'r') as file:
            s = file.read()
            self.parse(s)

    def save(self, file=sys.stdout):
        if type(file) is str:
            with open(file, 'w') as f:
                f.write(str(self))
        else:
            file.write(str(self))

    def find_direction(self, time):
        ts = 0
        for i in range(len(self.path)):
            ts += self.path[i][1]
            if ts >= time:
                return i
        return -1


    def put_spike(self, x, y, ts):
        """
            Ajoute un spike, màj les listes self.indices et self.times

            :param x: Adresse spatial en x, (0 >= x < self.width)
            :param y: Adresse spatial en y, (0 >= y < self.height)
            :param ts: Timestamp du spike (en ms)
            :return: None
        """
        idx = y*self.height + x
        self.indices.append(idx)
        self.times.append(ts)


    def put(self, texture, pos, time):
        def put_elm(elm, is_texture=False):
            if self.is_tor:
                elm[0] = elm[0] % self.width  # x
                elm[1] = elm[1] % self.height # y

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


    # TODO : Prise en compte des vitesses et acc dans le path
    def build(self):
        self.indices = []
        self.times   = []


        mvf = self.vel / self.sample
        mvi = math.floor(mvf)
        epsilon = mvf - mvi
        acc = 0
        ts  = 0 # Microseconds
        delta = round(1/self.sample * 1000, 5)

        for ei in self.path:
            n = int(ei.time * self.sample)

            if ei.direction == EntityDirection.JUMP:
                # if isinstance(attr, tuple):
                #     pos, time = attr
                #     self.put(self.texture, pos, time)
                ts = round(ts + n, 5)

                if ei.pos is not None:
                   self.put(self.texture, ei.pos, ts)
                
                continue

            for _ in range(n):
                mvt = mvi
                if acc > 1:
                    acc -= math.floor(acc)
                    mvt += 1

                self.texture.move(ei.direction, mvt, ts)

                ts   = round(ts + delta, 5)
                acc += epsilon # MOUAIS
        return

    def merge(self, ent_input, timesep=0, orig=None):
        if self.times:
            orig = self.times[-1] if orig is None else orig
        else:
            orig = 0 if orig is None else orig

        timesep += orig

        for i in range(len(ent_input.indices)):
            self.indices.append(ent_input.indices[i])
            self.times.append(ent_input.times[i] + timesep)

        self.path.extend(ent_input.path)

        self.length += ent_input.length
        return

    def concat(self, ent_input, timesep=0, orig=None):
        res = cpy.deepcopy(self)
        res.merge(ent_input, timesep, orig)
        return res

    def cut(self, start=None, end=None):
        if start is None and end is None:
            return

        self.times, self.indices = get_elms_withtimes(self.times, self.indices, start, end)

        self.path = get_labels_withtimes(self.path, start, end)
        return



    def run_animation(self, fps=60, xlim=None, ylim=None):
        plt.ion()
        fig = plt.figure(figsize=(6,6))
        plt.show()
        ax = fig.add_subplot(111)


        xlim = 0, self.width-1  if xlim is None else xlim
        ylim = 0, self.height-1 if ylim is None else ylim

        delta = 1/fps if fps != 0 else 0

        ids = np.array(self.indices)

        xs = ids  % self.width
        ys = ids // self.width

        # for i in range(len(self.times)):
        #     t = self.times[i]
        #     i = self.indices[i]
        #     x = xs[i]
        #     y = ys[i]
        #
        #     # print('t :', str(t), 'i :', str(i), 'pos :', str(x) + ',' + str(y))

        xs_ti = []
        ys_ti = []
        ti = self.times[0]
        for i in range(len(self.times)): # self.times doit être ordonnées
            if ti != self.times[i]:
                ax.clear()
                ax.scatter(xs_ti, ys_ti,
                           c="g", marker = 'o', cmap = cm.jet)

                ax.set_xlim(xlim)
                ax.set_ylim(ylim)
                plt.draw()
                plt.pause(delta)

                xs_ti = []
                ys_ti = []
                ti = self.times[i]

            xs_ti.append(xs[i])
            ys_ti.append(ys[i])
        return
