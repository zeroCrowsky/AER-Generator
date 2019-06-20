# shape = Shape.fromfile('impulsion/data/inputs/shapes/shape_5x5_square_id2.txt')
# texture = EntityTexture(0, 0, shape)
#
# path = CC(10, 0.2)
#
# # Params public
# input_params = {'texture' : texture,
#                 'dim' : (5, 5),
#                 'vel' : 480,
#                 'is_tor' : True,
#                 'sample': 1000,
#                 'path' : path}

root_path = ''
data_path = root_path + 'data/'
inputs_data_path  = data_path + 'inputs/'

inject = lambda : CC(1, 0.01).inject(0.01, lambda : [EI(J, 0.005)])

name_shapes = ['shape_5x5_diag5.txt',
               'shape_5x5_square9.txt',
               'shape_5x5_vline5.txt']

repr_shapes = ['diag', 'square', 'vline']

name_pres = ['cons', 'rdm_abs', 'rdm_eq']



input_params = {'path_dest' : inputs_data_path,
                'path_shapes' : inputs_data_path + 'shapes/',
                'name_shapes' : name_shapes,
                'repr_shapes' : repr_shapes,
                'name_pres' : name_pres,
                'time_pres' : 0.2,
                'npres' : 10,
                'dim': (5, 5),
                'vel' : 480,
                'sample' : 1000,
                'is_tor' : True,
                'prefix' : 'input1',
                'inject' : inject}

input_factory = EntityMultipleFactory




# factory_params = {'nseq' : 10,
#                   'dim'  : (5, 5),
#                   'direction_time_sec' : 0.2,
#                   'shape': Shape.fromfile('impulsion/data/inputs/shapes/shape_5x5_square_id2.txt'),
#                   'middle': False}
# initializer = 'EntityFactory.initializer_rdm_relative_seqinput'
