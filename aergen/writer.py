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
    from impulsion.input.entity.alias   import *
    from impulsion.input.entity.input   import *
    from impulsion.input.entity.texture import *

    options, _ = parse_args()

    exec(open(options.factory).read())
    exec(open(options.params).read())

    ef = input_factory(**input_params)
    i1 = ef.create()
    # i1.save(options.output)
    # if options.animation:
    #     i1.run_animation()
