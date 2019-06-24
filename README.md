# AER Generator

- Veïs OUDJAIL
- Jean MARTINET

## How to use?
- First	follow the INSTALL.md instructions

- In the project, there is a _Makefile_, there are several rules, some concerning the launching of unit tests, others concerning the launching of executables:

   - `winput`: This rule allows to execute a program that generates an AER sequence in text file, via a configuration file (see corresponding section). In Makefile, there are parameters to set the default paths to simplify the command line, if you wish, you can modify these parameters. Here is a simple command to generate one sequence, `-a` is an option to activate if you want to display the sequence when it is generated.

   ```
   make winput PARAMS=param2.py OUTPUT=test.txt ARGS=-a
   ``` 
   - `run_test`: This rule runs all unit tests

## 

## Configuration file
Here is a minimal example, the file format is `python`. This file is located at `aergen/params/param2.py`
```python
root_path  = ''
data_path  = root_path + 'data/'
shape_path = data_path + 'shapes/'

shapes = shape_path + 'shape_5x5_diag5.txt'

factory_params = {'positions'     : [(0,-5), (0,5), (-5,0), (5,0)],
                  'pres_strategy' : ProtocolInputSequenceFactory.initializer_consecutive_input_sequence}

input_params = {'time_pres' : 0.3,   # The times direction motion
                'npres'     : 2,     # The number of sequence repetitions
                'dim'       : (5,5), # Window dimension
                'vel'       : 480,   # Texture speed in pixel/sec
                'sample'    : 1000,  # Window update rate in Hz 
                'is_tor'    : False, # Toric environment 
                'outside'   : True}  # Compute texture motion outside the window

# Test sequence parameter
input_test_params = {'time_pres' : 0.03, 
                     'time_jump' : 0.005,
                     'npres'     : 1,
                     'path'      : lambda: EP([EI(J, 0.005)] + CC(1, 0.03).inject(0.03, lambda: [EI(J, 0.005)]))}

params = {'factory_params'    : factory_params,
          'input_params'      : input_params,
          'input_test_params' : input_test_params,
          'shapes'            : shapes}

input_factory = ProtocolInputSequenceFactory
```

In this file, `factory_param['positions']` key represents the initial texture positions for each motion direction. 
In input_test_params, `path` key represent motions direction sequence.

## AER File
In this example, here is the text format of a sequence:
```
480 1000 5 5 3.56 0 1
-138 0 0 1
5 5
00001
00010
00100
01000
10000
#
80
NORTH 0.3
JUMP 0.005
NORTH 0.03
...
JUMP 0.005
600
4 11.0
8 11.0
12 11.0
...
0 3544.00
```
First line corresponding to global attribute (each attribute separate by space):
- (_velocity_: 480 pixel/sec, _sample_: 1000 Hz, _width-window_: 5 px,  _height-window_: 5 px, _length-sequence_: 3.56 sec, _toric-window_: False, _update-outside_: True)

Second line corresponding texture attribute:
- (_texture-position-x_: -138, _texture-position-y_: 0, _texture-shape-id_: 0, _texture-shape-number_:1)

The following lines up to the __#__ marker correspond to the shapes that the texture can take. The shapes number is known (_texture-shape-number_).

The next line correponds to the number of motions direction sequence

Each next line corresponds to an action in the sequence, an action is represented by a type and a duration.
- an action maybe a direction (__NORTH__, __SOUTH__, __EST__, __WEST__). There exists a particular action: __JUMP__, for a certain period of time, the pattern doesn't move.

After a specific number of lines, the last part of the file encodes the AER events.

The first line corresponds to the number of events.
Each next line corresponds to an event, an event is represented by the flat spatial coordinate and the timestamp. The flat spatial coordinate (_indice_) is compute by this relation :

    indice = y . width + x 

## Main objects and methods

[TODO]
```python
path = EP([]) # EP is a constructor, it's an alias for EntityPath
path1 = EP([EI(N, 0.3)]) # EI is an element, N represent North direction and 0.3 is times direction motion in second. 
path2 = EP([EI(J, 0.3)]) # J represent JUMP, for a certain period of time, the pattern doesn't move. 
path = path1 + path2 # Append path
texture = Texture()
ei = EntityInput()
``` 
- N, S, W, E, J : NORTH, SOUTH, WEST, EST, JUMP

### Note
One way to see the different uses of the library is to look at the different unit tests.
