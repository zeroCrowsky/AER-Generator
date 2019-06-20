from unittest import TestCase

from aergen.path  import EntityPath
from aergen.alias import *


class EntityPathTest(TestCase):
    def test_inject(self):
        path = CC(1, 0.2)
        path_expected = \
            [EI(N, 0.07), EI(N, 0.07), EI(N, 0.06),
             EI(S, 0.01), EI(S, 0.07), EI(S, 0.07), EI(S, 0.05),
             EI(E, 0.02), EI(E, 0.07), EI(E, 0.07), EI(E, 0.04),
             EI(W, 0.03), EI(W, 0.07), EI(W, 0.07), EI(W, 0.03)]

        path_result = path.inject(0.07, lambda : [])
        self.assertEqual(path_expected, path_result)

        path = CC(1, 0.2)
        path_expected = \
            [EI(N, 0.1), EI(N, 0.1),
             EI(S, 0.1), EI(S, 0.1),
             EI(E, 0.1), EI(E, 0.1),
             EI(W, 0.1), EI(W, 0.1)]
        path_result = path.inject(0.1, lambda : [])
        self.assertEqual(path_expected, path_result)

        path = CC(1, 0.2)
        path_expected = \
            [EI(N, 0.2), EI(ST, 0.1),
             EI(S, 0.2), EI(ST, 0.1),
             EI(E, 0.2), EI(ST, 0.1),
             EI(W, 0.2), EI(ST, 0.1)]
        path_result = path.inject(0.2, lambda : [EI(ST, 0.1)])
        self.assertEqual(path_expected, path_result)

        path = CC(4, 0.2)
        path_expected = \
            [EI(N, 0.2), EI(S, 0.2), EI(E, 0.2), EI(W, 0.2), EI(ST, 0.1),
             EI(N, 0.2), EI(S, 0.2), EI(E, 0.2), EI(W, 0.2), EI(ST, 0.1),
             EI(N, 0.2), EI(S, 0.2), EI(E, 0.2), EI(W, 0.2), EI(ST, 0.1),
             EI(N, 0.2), EI(S, 0.2), EI(E, 0.2), EI(W, 0.2), EI(ST, 0.1)]
        path_result = path.inject(0.8, lambda : [EI(ST, 0.1)])
        self.assertEqual(path_expected, path_result)


    def test_itempath_tojson(self):
        item = EI(N, 0.2, str_method='str_ei_json', parse_method='parse_ei_json')
    
        item_str = str(item)
        

        import ipdb; ipdb.set_trace()