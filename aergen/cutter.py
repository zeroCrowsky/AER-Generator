import sys, os; sys.path.insert(0, os.getcwd())

from impulsion.input.entity.input import EntityInput

import optparse as op

def parse_args():
    parser = op.OptionParser()
    parser.add_option('-f', '--filename', dest='filename', default='')
    parser.add_option('-s', '--start', dest='start', type='int', default=None)
    parser.add_option('-e', '--end', dest='end',type='int', default=None)
    parser.add_option('-o', '--output', dest='output',
                      help='''Specify file where you want to write, by default, it's stdout''', default=sys.stdout)
    parser.add_option('-a', '--animation', dest='animation', action="store_true", default=False)
    return parser.parse_args()

def launch(options):
    i1 = EntityInput.fromfile(options.filename)
    s, e = options.start, options.end
    i1.cut(s, e)
    for i in range(len(i1.times)):
        i1.times[i] -= s
    i1.save(options.output)
    if options.animation:
        i1.run_animation()

if __name__ == '__main__':
    options, _ = parse_args()

    launch(options)
