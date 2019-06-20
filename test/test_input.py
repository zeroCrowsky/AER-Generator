from unittest import TestCase

from aergen.alias import *

import aergen.input as ei

class EntityInputTest(TestCase):
    def test_get_labels_withtimes(self):
        path = CC(2, 0.2)

        lbl_expected = [EI(S, 0.2)]
        lbl_res = ei.get_labels_withtimes(path, 340, 341)
        self.assertEqual(lbl_expected, lbl_res)

        lbl_expected = [EI(E, 0.2)]
        lbl_res = ei.get_labels_withtimes(path, 440, 441)
        self.assertEqual(lbl_expected, lbl_res)

        lbl_expected = [EI(N, 0.2)]
        lbl_res = ei.get_labels_withtimes(path, 0, 20)
        self.assertEqual(lbl_expected, lbl_res)

        lbl_expected = [EI(N, 0.2)]
        lbl_res = ei.get_labels_withtimes(path, 0, 200)
        self.assertEqual(lbl_expected, lbl_res)

        lbl_expected = [EI(E, 0.2)]
        lbl_res = ei.get_labels_withtimes(path, 401, 600)
        self.assertEqual(lbl_expected, lbl_res)

        lbl_expected = [EI(S, 0.2), EI(E, 0.2), EI(W, 0.2)]
        lbl_res = ei.get_labels_withtimes(path, 201, 900)
        self.assertEqual(lbl_expected, lbl_res)

        path = [EI(N, 0.2),
                EI(N, 0.005), EI(J, 0.003), EI(S, 0.005), EI(J, 0.003),
                EI(E, 0.005), EI(J, 0.003), EI(W, 0.005), EI(J, 0.003)]

        lbl_expected = [EI(N, 0.005), EI(J, 0.003), EI(S, 0.005), EI(J, 0.003),
                        EI(E, 0.005), EI(J, 0.003), EI(W, 0.005), EI(J, 0.003)]

        lbl_res = ei.get_labels_withtimes(path, 201, 232)

        #self.assertEqual(lbl_expected, lbl_res)

    def test_get_elms_withtimes(self):
        times = [1, 1, 3, 3, 3, 6, 7, 7]
        data  = [0, 0, 1, 1, 1, 2, 3, 3]

        elms_expected = 2, 5
        elms_res = ei.get_elms_withtimes(times, data, 3, 3, retrange=True)
        self.assertEqual(elms_expected, elms_res)

        elms_expected = 0, 5
        elms_res = ei.get_elms_withtimes(times, data, 0, 3, retrange=True)
        self.assertEqual(elms_expected, elms_res)

        elms_expected = 0, 5
        elms_res = ei.get_elms_withtimes(times, data, 0, 5, retrange=True)
        self.assertEqual(elms_expected, elms_res)

        elms_expected = 0, 2
        elms_res = ei.get_elms_withtimes(times, data, 0, 2, retrange=True)
        self.assertEqual(elms_expected, elms_res)

        elms_expected = 0, 2
        elms_res = ei.get_elms_withtimes(times, data, 0, 2.5, retrange=True)
        self.assertEqual(elms_expected, elms_res)

        elms_expected = 5, 8
        elms_res = ei.get_elms_withtimes(times, data, 6, 7, retrange=True)
        self.assertEqual(elms_expected, elms_res)


        times = [1, 1, 3, 3, 3, 6, 7, 7]

        print()
        elms_res = ei.get_elms_withtimes(times, data, 3.3, 3.4, retrange=True)

        print(elms_res)


    def test_get_spikes_withlabels(self):
        path = [EI(N,0.002),EI(S,0.003),EI(E,0.001),EI(W,0.002)]
        times = [1,1,1,2,2,3,4,5,6,6,7,8]
        start, end = 0, len(times)
        labels_spks_expected = [(0,5),(5,8),(8,10),(10,12)]
        labels_spks_res = ei.get_spikesrange_withlabels(path, times, start, end)
        self.assertEqual(labels_spks_expected, labels_spks_res)

        times = [1,1,1,2,2,3,4,5,6,6,7]
        start, end = 0, len(times)
        labels_spks_expected = [(0,5),(5,8),(8,10),(10,11)]
        labels_spks_res = ei.get_spikesrange_withlabels(path, times, start, end)
        self.assertEqual(labels_spks_expected, labels_spks_res)

        path = [EI(N,0.002),EI(J,0.002),EI(S,0.003),EI(E,0.001),EI(W,0.002),EI(J,0.002)]
        times = [1,1,1,2,2,5,6,7,8,8,9,10]
        start, end = 0, len(times)
        labels_spks_expected = [(0,5),None,(5,8),(8,10),(10,12),None]
        labels_spks_res = ei.get_spikesrange_withlabels(path, times, start, end)
        self.assertEqual(labels_spks_expected, labels_spks_res)
