from aergen.core.direction import EntityDirection

from aergen.config import Configuration

import aergen.utils as iu

import numpy  as np
import copy   as cp
import random as rdm
import json 


def get_property_env(env, env_property, property):
    (None if env is None else env_property) if property is None else property


def get_method(method):
    if isinstance(method, str):
        return eval(method)
    return method

def str_ei_handcraft(ei):
    sep = ei._sep
    d_str = ei.direction.name
    t_str = str(ei.time)
    pos_str = '' if ei.pos       is None else sep + 'pos:'      + str(ei.pos[0]) + ',' + str(ei.pos[1])
    s_str   = '' if ei._shape_id is None else sep + 'shape_id:' + str(ei.shape_id)
    v_str   = '' if ei._vel      is None else sep + 'vel:'      + str(ei._vel)
    a_str   = '' if ei._acc      is None else sep + 'acc:'      + str(ei._acc)
    return d_str + sep + t_str + pos_str + s_str + v_str + a_str

def str_ei_json(ei): 
    result = {
        "direction": ei.direction.name,
        "time"     : ei.time,
        "vel"      : ei._vel,
        "acc"      : ei._acc,
        "shape_id" : ei._shape_id
    }
    return json.dumps(result)


def set_shape_id(ei, v): ei._shape_id = np.fromstring(v, sep=',') 
def set_pos(ei, v):      ei._pos = int(v)
def set_vel(ei, v):      ei._vel = eval(v)
def set_acc(ei, v):      ei._acc = eval(v)

dict_ei_setter = {
    'shape_id': set_shape_id,
    'pos':      set_pos,
    'vel':      set_vel,
    'acc':      set_acc 
}

def parse_ei_handcraft(ei, s):
    sep = ei._sep
    data = s.split(sep)
    n    = len(data)
    ei._direction  = EntityDirection[data[0]]
    ei.time        = eval(data[1])
    
    for i in range(2, n):
        name, value = data[i].split(':')
        setter = dict_ei_setter[name]
        setter(ei, value)            
    
    return ei

def init_from_dict(ei, dct):
    ei.time       = dct["time"] 
    ei._direction = EntityDirection[dct["direction"]]
    ei._vel       = dct["vel"]      
    ei._acc       = dct["acc"]      
    ei._shape_id  = dct["shape_id"]

    return ei

def from_dict(dct):
    return init_from_dict(EntityDirectionItemPath.empty(), dct)

def parse_ei_json(ei, s):
    dct = json.loads(s) 
    return init_from_dict(ei, dct)

str_method   = Configuration.EntityDirectionItemPath.str_method
parse_method = Configuration.EntityDirectionItemPath.parse_method


class EntityDirectionItemPath(object):
    @staticmethod
    def empty():
        return EntityDirectionItemPath(None, None)

    def __init__(self, direction, time, pos=None, shape_id=None, vel=None, acc=None, env=None,
            str_method=str_method, 
            parse_method=parse_method):
        self.time = time; self.env = env
        self.direction = direction

        self.pos = pos
        self._shape_id = shape_id; self._vel = vel; self._acc = acc

        self._sep = ' '

        self.str_method   = get_method(str_method)
        self.parse_method = get_method(parse_method)

        return

    def __repr__(self):
        return str(self)

    def __eq__(self, ei):
        if not isinstance(ei, type(self)):
            return False
        return self.direction == ei.direction and self.time == ei.time

    def __str__(self):
        return self.str_method(self)
    
    def parse(self, s):
        self.parse_method(self, s)

    @property
    def direction(self): return self._direction

    @direction.setter
    def direction(self, direction):
        self._direction = EntityDirection[direction] if isinstance(direction, str) else direction

    @property
    def shape_id(self): return get_property_env(self.env, self.env.shape_id, self._shape_id)

    @shape_id.setter
    def shape_id(self, shape_id):
        self._shape_id = shape_id

    @property
    def vel(self): return get_property_env(self.env, self.env.vel, self._vel)

    @vel.setter
    def vel(self, vel): self._vel = vel

    @property
    def acc(self): return get_property_env(self.env, self.env.acc, self._acc)

    @acc.setter
    def acc(self, acc): self._acc = acc



class EntityPath(list):
    def __init__(self, *args, path=None, env=None, metadata=None):
        list.__init__(self, *args)
        self.metadata = [] if metadata is None else metadata
        self.env = env
        if path is not None:
            self.extend(path)

    def __str__(self):
        npath = len(self)
        s = ''
        s += str(npath) + ' '.join(list(map(lambda x: str(x), self.metadata))) + '\n'

        for e in self:
            s += str(e) + '\n'

        return s

    def parse_header(self, line):
        npath, *metadata = line.split(' ')

        self.metadata = metadata

        return int(npath)

    def parse(self, data, start=None, end=None, parse_header=True, npath=None):
        if isinstance(data, str):
            data = data.split('\n')

        start = 0           if start is None else start
        if parse_header:
            npath = self.parse_header(data[start])
            start += 1
        end   = npath+start if end   is None else end

        for i in range(start, end):
            ei = EntityDirectionItemPath.empty()
            ei.parse(data[i])
            self.append(ei)
        return self

    @property
    def times(self)
        ts = []
        t = 0
        for e in self:
            ts.append(t)
            t += e.time
        return ts

    @property
    def length(self):
        lgth = 0
        for p in self:
            lgth += round(p.time, 6)
        return round(lgth, 6)


    def inject(self, dt, builder, endvalue=True, epsilon=0.00001, dec=5):
        path = []
        lgth = self.length

        n = round(lgth / dt, 5)
        if n - int(n) == 0:
            endvalue = False
        n = int(n)

        m = len(self)
        i = j = lt = 0
        ti = dt; tj = round(self[j].time, dec)
        #import ipdb; ipdb.set_trace()
        while i < n:
            diff = round(ti - tj, dec)
            ed = cp.copy(self[j])

            if ti < tj:
                ed.time = round(ti - lt, dec)
                path.append(ed); path.extend(builder())

                lt = round(lt + ed.time, dec); i += 1
                ti = round(ti + dt, dec)
            else: # ti >= tj
                # Cas ti > tj
                ed.time = round(tj - lt, dec)
                path.append(ed)
                lt = round(lt + ed.time, dec); j += 1

                if j < m: # Fix end equal case
                    tj = round(tj + round(self[j].time, dec), dec)
                # Cas ti == tj
                if abs(diff) < epsilon: # ti == tj
                    path.extend(builder())
                    ti = round(ti + dt, dec); i += 1
            continue

        if endvalue:
            ed = cp.copy(self[j])
            ed.time = round(lgth - lt, dec)
            path.append(ed); path.extend(builder())

        return EntityPath(path=path, env=self.env)

    @staticmethod
    def create_path_equitable_rdm(nseq, *args, kwargs={}):
        return iu.create_sequence_equitable_rdm(
            sequence=EntityPath(),
            nseq=nseq,
            add_item=(lambda s, i: s.append(i)),
            create_item=(lambda d: EntityDirectionItemPath(d, *args, **kwargs)),
            create_all_params=EntityDirection.directions
        )

    @staticmethod
    def create_path_absolute_rdm(nseq, *args, kwargs={}):
        return iu.create_sequence_absolute_rdm(
            sequence=EntityPath(),
            nseq=nseq,
            add_item=(lambda s, i: s.append(i)),
            create_item=(lambda d: EntityDirectionItemPath(d, *args, **kwargs)),
            create_all_params=EntityDirection.directions
        )

    @staticmethod
    def create_path_consecutive(nseq, *args, directions=EntityDirection.directions, kwargs={}):
        return iu.create_sequence_consecutive(
            sequence=EntityPath(),
            nseq=nseq,
            add_item=(lambda s, i: s.append(i)),
            create_item=(lambda d: EntityDirectionItemPath(d, *args, **kwargs)),
            create_all_params=directions
        )

    @staticmethod
    def create_path_withstr(chars):
        pass
