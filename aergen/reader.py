import sys, os; sys.path.insert(0, os.getcwd())

from impulsion.input.entity.input import EntityInput

from impulsion.input.entity.alias import *

import optparse as op

def parse_args():
    parser = op.OptionParser()
    parser.add_option('-f', '--filename', dest='filename', default='')
    parser.add_option('-t', '--fps', dest='fps', type='int', default=10)
    return parser.parse_args()

if __name__ == '__main__':
    options, _ = parse_args()
    print(options.fps)
    inp = EntityInput.fromfile(options.filename).run_animation(fps=options.fps)
