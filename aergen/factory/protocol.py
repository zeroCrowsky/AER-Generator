# def create_input_equitable_rdm(nseq, *args):
#     return iu.create_sequence_equitable_rdm(
#         sequence=EntityPath()
#         nseq=nseq,
#         add_item=lambda s, i: s.append(i)
#         create_item=lambda d: EntityDirectionItemPath(d, time, vel, acc, env)
#         create_all_params=get_directions
#     )
#
# def create_input_absolute_rdm(nseq, *args):
#     return iu.create_sequence_absolute_rdm(
#         sequence=EntityPath()
#         nseq=nseq,
#         add_item=lambda s, i: s.append(i)
#         create_item=lambda d: EntityDirectionItemPath(d, time, vel, acc, env)
#         create_all_params=get_directions
#     )
#
# def create_input_consecutive(nseq, *args):
#     return iu.create_sequence_equitable_rdm(
#         sequence=EntityPath()
#         nseq=nseq,
#         add_item=lambda s, i: s.append(i)
#         create_item=lambda d: EntityDirectionItemPath(d, time, vel, acc, env)
#         create_all_params=get_directions
#     )

from impulsion.input.entity.input   import EntityInput
from impulsion.input.entity.texture import EntityTexture
from impulsion.input.entity.alias   import EP, EI, E, W, N, S, J

def create_all_directions_sequence(shapes, positions, input_params, shape_id=0):
       tp = input_params['time_pres']
       smp = input_params['sample']; vel = input_params['vel']
       dim = input_params['dim']; ist = input_params['is_tor']
       outside = input_params['outside']
       
       textures = create_all_directions_textures(shapes, positions, shape_id)

       directions = [EntityInput(textures[0], EP([EI(N, tp)]), dim, smp, vel, is_tor=ist, outside=outside),
                     EntityInput(textures[1], EP([EI(S, tp)]), dim, smp, vel, is_tor=ist, outside=outside),
                     EntityInput(textures[2], EP([EI(E, tp)]), dim, smp, vel, is_tor=ist, outside=outside),
                     EntityInput(textures[3], EP([EI(W, tp)]), dim, smp, vel, is_tor=ist, outside=outside)]
       return directions

def create_all_directions_textures(shapes, positions, shape_id):
    npos = len(positions)
    for _ in range(npos-1, 4):
        positions.append((0,0))
    
    p = positions
    return [EntityTexture(p[i][0], p[i][1], shapes, shape_id=shape_id) for i in range(4)]


class ProtocolInputSequenceFactory(object):
    def __init__(self, factory_params, input_params, input_test_params, shapes, shape_id=0, input_test=None):

        self.positions = factory_params['positions']

        self.input_params      = input_params
        self.input_test_params = input_test_params

        self.npres = input_params['npres']

        self.shapes   = shapes
        self.shape_id = shape_id

        self.time_pres_msec      = round(self.input_params['time_pres'] * 1000, 6)
        self.time_pres_msec_test = round(self.input_test_params['time_pres'] * 1000, 6)
        self.time_jump_msec_test = round(self.input_test_params['time_jump'] * 1000, 6)

        self.jump = EI(J, self.input_test_params['time_jump'])

        self.input_test = input_test
        if self.input_test is not None:
            self.lgth_msec_test = self.input_test.length * 1000
        else: 
            self.lgth_msec_test = None

        self._last_directions      = None
        self._data_input           = None
        self._orig                 = 0
        self._all_input_directions = None

        self.merge_sequence_input = self.merge_sequence_input_train

        self.reset_input()

    def reset_input(self):
        self._data_input = EntityInput.empty(self.input_params['dim'])
        self._orig       = 0

    def create_input(self):
        res = EntityInput.cpy_params(self._last_directions)
        res.indices = self._data_input.indices
        res.times   = self._data_input.times
        res.path    = self._data_input.path

        return res

    def create_input_test_sequence(self, initializer_strategy_input_sequence):
        self.merge_sequence_input = self.merge_sequence_input_test
        self.npres = self.input_test_params['npres']
        
        self._all_input_directions = create_all_directions_sequence(self.shapes, self.positions,
                                                                    self.input_test_params, shape_id=self.shape_id)

        self._orig = self.time_jump_msec_test 
        
        self._data_input.path.append(self.jump)   

        initializer_strategy_input_sequence(self)

        return self.create_input()


    def create_input_sequence(self, initializer_strategy_input_sequence):
        self.merge_sequence_input = self.merge_sequence_input_train
        self.npres = self.input_params['npres']
        
        self.lgth_msec_test = self.input_test.length * 1000
        
        self._all_input_directions = create_all_directions_sequence(self.shapes, self.positions,
                                                                    self.input_params, shape_id=self.shape_id)
        
        initializer_strategy_input_sequence(self)

        return self.create_input()


    def merge_sequence_input_fct(self, sequence, time_pres_msec):
        self._data_input.merge(sequence, orig=self._orig)
        self._orig = round(self._orig + time_pres_msec, 6)

    def merge_sequence_input_test(self, sequence):
        # Warning : length update via input.set_path
        time_step = self.time_pres_msec_test + self.time_jump_msec_test
        self.merge_sequence_input_fct(sequence, time_step)
        self._data_input.path.append(self.jump)



    def merge_sequence_input_train(self, sequence):
        self.merge_sequence_input_fct(sequence, self.time_pres_msec)
        self.merge_sequence_input_fct(self.input_test, self.lgth_msec_test)

        # self.__data_input.merge(sequence, orig=self.__orig)
        # self.__orig = round(self.__orig + self.time_pres_msec, 6)
        # self.__data_input.merge(self.input_test, orig=self.__orig)
        # self.__orig = round(self.__orig + self.time_pres_msec_test, 6)


    def initializer_rdm_relative_input_sequence(self):
        import random as rdm
        all_ds = self._all_input_directions; npres = self.npres

        for _ in range(npres):
            rdm.shuffle(all_ds)
            for d in all_ds:
                self.merge_sequence_input(d)

        self.__last_directions = all_ds[-1]


    def initializer_rdm_absolute_input_sequence(self):
        import random as rdm
        all_ds = self._all_input_directions; npres = self.npres
        nds = len(all_ds); idx = 0
        for _ in range(npres):
            for _ in range(nds):
                idx = rdm.randint(0, nds-1)
                self.merge_sequence_input(all_ds[idx])

        self._last_directions = all_ds[idx]


    def initializer_consecutive_input_sequence(self):
        all_ds = self._all_input_directions; npres = self.npres
        for _ in range(npres):
            for d in all_ds:
                self.merge_sequence_input(d)

        self._last_directions = all_ds[-1]
