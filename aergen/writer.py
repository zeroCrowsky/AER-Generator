import sys, os; sys.path.insert(0, os.getcwd())

import sys
import optparse as op


def parse_args():
    parser = op.OptionParser()
    parser.add_option('-f', '--factory', dest='factory',
                      help='''Specify file where you want to load for create input.
                      Compatible with python file''', default='')
    parser.add_option('-p', '--params', dest='params',
                      help='''Specify file where you want to load for create input.
                      Compatible with python file''', default='')
    parser.add_option('-o', '--output', dest='output',
                      help='''Specify file where you want to write, by default, it's stdout''', default=sys.stdout)
    parser.add_option('-a', '--animation', dest='animation', action="store_true", default=False)
    return parser.parse_args()


# TODO REFACTOR FACTORY
if __name__ == '__main__':
    from aergen.core.alias   import *
    from aergen.core.input   import *
    from aergen.core.texture import *

    options, _ = parse_args()
    exec(open(options.factory).read())
    exec(open(options.params).read())

    ef = input_factory(**params)
    i1 = ef.create()
    i1.save(options.output)
    if options.animation:
        i1.run_animation(dim=(600,600), time_acquisition=0)
