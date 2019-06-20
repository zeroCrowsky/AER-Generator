import multiprocessing as mp
import threading as th
import shutil as sh
import random as rdm
import os
import sys


def flat_coordinates(coordinates, limits_max, precision=3):
    n = len(coordinates)
    mult = 1
    index = 0
    for i in range(n):
        c = coordinates[n-1-i]
        l = limits_max[n-1-i]
        r = round(c * mult, precision)
        index = round(index + r, precision)
        mult = round(mult * l, precision)

    return index


def create_sequence_equitable_rdm(sequence, nseq, add_item, create_item, create_all_params):
    all_params = create_all_params()
    for i in range(nseq):
        rdm.shuffle(all_params)
        for param in all_params:
            item = create_item(param)
            add_item(sequence, item)

    return sequence


def create_sequence_absolute_rdm(sequence, nseq, add_item, create_item, create_all_params):
    all_params = create_all_params()
    n = len(all_params)
    for i in range(nseq):
        for j in range(n):
            idx = rdm.randint(0, n-1)
            item = create_item(all_params[idx])
            add_item(sequence, item)

    return sequence


def create_sequence_consecutive(sequence, nseq, add_item, create_item, create_all_params):
    all_params = create_all_params()
    for i in range(nseq):
        for param in all_params:
            item = create_item(param)
            add_item(sequence, item)
    return sequence


def mfloat(x, rnd=5):
    return round(float(x), rnd)


def parse_unit(chars):
    return eval(chars.replace(' ', '*', 1))


def str_dict(dict):
    result = ''
    for k, v in dict.items():
        result += k + ' ' + str(v) + '\n'
    return result


def mapfloat(x, xmin, xmax, ymin, ymax):
    x = min(max(x, xmin), xmax)
    return ymin + (x - xmin) * ((ymax - ymin) / (xmax - xmin))


def rmforce(filename):
    if os.path.isfile(filename):
        os.remove(filename)

    sh.rmtree(filename, ignore_errors=True)
    return


def ls(path, filter_elm=lambda _: True):
    from os import listdir
    from os.path import isfile, join
    return [f for f in listdir(path) if filter_elm(f)]


def lsfile(path, filter_name=lambda _: True):
    from os import listdir
    from os.path import isfile, join
    return [f for f in listdir(path) if isfile(join(path, f)) and filter_name(f)]


def log(*args, display=True, **kwargs):
    if display:
        print(*args, **kwargs)


def save(chars, file=sys.stdout):
    if type(file) is str:
        with open(file, 'w') as f:
            f.write(chars)
    else:
        file.write(chars)


def load(file=sys.stdin):
    text = ''
    if type(file) is str:
        with open(file, 'r') as f:
            text = f.read()
    else:
        text = file.read()
    return text


def run_in_thread(fn):
    def run(*k, **kw):
        t = th.Thread(target=fn, args=k, kwargs=kw)
        t.start()
    return run


def run_in_process(fn):
    def run(*k, **kw):
        p = mp.Process(target=fn, args=k, kwargs=kw)
        p.start()
    return run
