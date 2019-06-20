from itertools import islice

import bisect as bs


left = bs.bisect_left


def right(xs, x): return bs.bisect_right(xs, x) - 1


def find(xs, x, bisect=left):
    'Locate the leftmost value exactly equal to x'
    i = bisect(xs, x)
    if i != len(xs) and xs[i] == x:
        return i
    raise IndexError


def find_left(xs, x):
    'Locate the leftmost value exactly equal to x'
    return find(xs, x, bisect=left)


def find_right(xs, x):
    'Locate the rightmost value exactly equal to x'
    return find(xs, x, bisect=right)


def find_range(xs, x):
    'Locate the range value exactly equal to x'
    i1 = find_left(xs, x)
    i2 = find_right(xs, x) + 1
    return i1, i2


def find_lt(xs, x):
    'Find rightmost value less than x'
    i = bs.bisect_left(xs, x)
    if i:
        return i-1
    raise IndexError


def find_le(xs, x):
    'Find rightmost value less than or equal to x'
    i = bs.bisect_right(xs, x)
    if i:
        return i-1
    raise IndexError


def find_gt(xs, x):
    'Find leftmost value greater than x'
    i = bs.bisect_right(xs, x)
    if i != len(xs):
        return i
    raise IndexError


def find_ge(xs, x):
    'Find leftmost item greater than or equal to x'
    i = bs.bisect_left(xs, x)
    if i != len(xs):
        return i
    raise IndexError


class SublistView(object):
    def __init__(self, base=[], start=0, end=None):
        self._base = base
        self._start = start
        self._end = len(self._base) if self._end is None else end

    def __len__(self): return self._end - self._start

    def __getitem__(self, index):
        self._check_end_range(index)
        return self._base[index + self._start]

    def __setitem__(self, index, value):
        self._check_end_range(index, 'list assignment index out of range')
        self._base[index + self._start] = value

    def __delitem__(self, index):
        self._check_end_range(index, 'list assignment index out of range')
        del self._base[index + self._start]

    def __iter__(self):
        return islice(self._base, self._start, self._end)

    def __str__(self):
        return str(self._base[self._start:self._end])

    def __repr__(self):
        return repr(self._base[self._start:self._end])

    def get_sublist(self, start=0, end=None):
        return SublistView(base=self._base, start=start, end=end)

    def _check_end_range(self, index, msg='list index out of range'):
        if self._end is not None and index >= self._end - self._start:
            raise IndexError(msg)


class SublistViewSequenceFactory(object):
    def __init__(self, base):
        self.base = base

    def create(self, start, end):
        return SublistView(self.base, start, end)


class RangeViewSequenceFactory(object):
    def __init__(self):
        return

    def create(self, start, end):
        return range(start, end)


rangeview_factory = RangeViewSequenceFactory()
'''
Temporal sequence view : sequence times : [ [
'''


class TemporalSequenceView(object):
    def __init__(self, data, times, sequence_factory=rangeview_factory):
        self.data = data
        self.times = times

        self.time_cur = 0
        self.time_idx = 0
        self.sequence_factory = sequence_factory

        return

    def __len__(self):
        return len(self.times)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.sequence(key.start, key.stop)

        start, end = find_range(self.times, key)
        return self.sequence_factory.create(start, end)

    def __setitem__(self, key, value):
        pass

    def __iter__(self):
        pass

    def sequence(self, tstart=0, tend=None):
        start = 0 if tstart == 0 else find_ge(self.times, tstart)
        end = len(self.data) - 1 if tend is None else find_lt(self.times, tend)

        return self.sequence_factory.create(start, end)

    def next(self, tduration):
        self.time_cur = round(self.time_cur + tduration, 5)
        # Compute idx
        start = self.time_idx
        end = find_lt(self.times, self.time_cur)

        self.time_idx = end

        return self.sequence_factory.create(start, end)

# def sequence(temporal, tstart=0, tend=None, sequence_factory=rangeview_factory):
#     temporal_sequence_factory = temporal.sequence_factory
#     temporal.sequence_factory = sequence_factory
#     result = temporal_sequence_factory.sequence(tstart, tend)
#     temporal.sequence_factory = temporal_sequence_factory

#     return result


class SyncTemporalSequenceView(object):
    def __init__(self, *temporals, sequence_factory=rangeview_factory):
        self.temporals = temporals

        self.time_cur = 0
        self.time_idx = [0] * len(temporals)

        self.sequence_factory = sequence_factory

        self.rangeview_factory = RangeViewSequenceFactory()

        return

    def sequence(self, tstart=0, tend=None):
        n = len(self.temporals)
        results = [None] * n
        for i in range(n):
            temporal = self.temporals[i]
            temporal_sequence_factory = temporal.sequence_factory
            temporal.sequence_factory = self.rangeview_factory
            results[i] = temporal.sequence(tstart, tend)
            temporal.sequence_factory = temporal_sequence_factory

        return results

    def next(self, tduration):
        n = len(self.temporals)
        results = [None] * n
        self.time_cur = round(self.time_cur + tduration, 5)

        for i in range(n):
            temporal = self.temporals[i]
            temporal_sequence_factory = temporal.sequence_factory
            temporal.sequence_factory = self.rangeview_factory
            results[i] = temporal.next(tduration)
            temporal.sequence_factory = temporal_sequence_factory

        return results


# class ObjectFactory(object):
#     def __init__(self, ctor, *args, **kwargs):
#         self.ctor   = ctor
#         self.args   = args
#         self.kwargs = kwargs

#     def create(self):
#         return self.ctor(*self.args, **self.kwargs)
