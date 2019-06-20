from impulsion.utils import rmforce

import os

class EntityMultipleFactory(object):

    PRES_PATH_GEN = {'cons'   : CC,
                     'rdm_abs': CA,
                     'rdm_eq' : CE}

    def __init__(self, path_dest, path_shapes, name_shapes, name_pres,
      dim, vel, is_tor, sample, time_pres, npres, repr_shapes=None, prefix='', inject=None):
        self.path_dest = path_dest; self.path_shapes = path_shapes
        self.name_shapes = name_shapes; self.name_pres = name_pres
        self.dim = dim; self.vel = vel; self.is_tor = is_tor; self.sample = sample
        self.time_pres = time_pres; self.npres = npres
        self.repr_shapes = name_shapes if repr_shapes is None else repr_shapes
        self.prefix = prefix
        self.inject = inject

        rmforce(self.path_dest)
        os.makedirs(self.path_dest)

        # if inject is None:
        #     self.inject = lambda : CC(1, 0.005).inject(0.005, lambda : [EI(J, 0.003)])
        return

    def create(self):
        inputs = []

        sep = '_'
        extension = '.in'
        pref = '' if self.prefix == '' else self.prefix + sep
        for i in range(len(self.name_shapes)):
            ns = self.name_shapes[i]
            rs = self.repr_shapes[i]
            shape = Shape.fromfile(self.path_shapes + ns)
            texture = EntityTexture(0, 0, shape)

            for j in range(len(self.name_pres)):
                np = self.name_pres[j]
                filename = pref + rs + sep + np + extension
                path = self.PRES_PATH_GEN[np](self.npres, self.time_pres)
                if self.inject is not None:
                    path = path.inject(self.time_pres, self.inject)

                inpt = EntityInput(texture, path, self.dim, self.sample, self.vel,
                    is_tor=self.is_tor)

                inpt.save(self.path_dest + filename)
                inputs.append(inpt)

        return inputs
