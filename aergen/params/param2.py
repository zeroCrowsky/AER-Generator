root_path  = ''
data_path  = root_path + 'data/'
shape_path = data_path + 'shapes/'

shapes = shape_path + 'shape_5x5_diag5.txt'

factory_params = {'positions'     : [(0,-5), (0,5), (-5,0), (5,0)],
                  'pres_strategy' : ProtocolInputSequenceFactory.initializer_consecutive_input_sequence}

input_params = {'time_pres' : 0.3,
                'npres'     : 2,
                'dim'       : (5,5),
                'vel'       : 480,
                'sample'    : 1000,
                'is_tor'    : False,
                'outside'   : True}

input_test_params = {'time_pres' : 0.03, 
                     'time_jump' : 0.005,
                     'npres'     : 1,
                     'path'      : lambda: EP([EI(J, 0.005)] + CC(1, 0.03).inject(0.03, lambda: [EI(J, 0.005)]))}

params = {'factory_params'    : factory_params,
          'input_params'      : input_params,
          'input_test_params' : input_test_params,
          'shapes'            : shapes}

input_factory = ProtocolInputSequenceFactory

