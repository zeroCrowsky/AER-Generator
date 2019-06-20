from unittest import TestCase

from aergen.texture import EntityTexture


texture_str_expected1 = \
'''0 0 0 1
2 1
11
'''

texture_str_expected2 = \
'''3 4 1 2
2 1
11
4 4
0000
0110
0110
0000
'''

shape1 = [[True, True]]

shape2 = [[False, False, False, False],
          [False, True, True, False],
          [False, True, True, False],
          [False, False, False, False]]

shapes = [shape1, shape2]

class EntityTextureTest(TestCase):


    def test_texture_str(self):
        texture = EntityTexture(0, 0, shape1)

        texture_str_result = str(texture)

        self.assertEqual(texture_str_expected1, texture_str_result)

        texture = EntityTexture(3, 4, shapes, shape_id=1)

        texture_str_result = str(texture)
        self.assertEqual(texture_str_expected2, texture_str_result)


    def test_texture_parse(self):
        texture_expected = EntityTexture(0, 0, shape1)
        texture_expected_str = str(texture_expected)

        texture_result = EntityTexture.fromstr(texture_expected_str)
        texture_result_str = str(texture_result)

        self.assertEqual(texture_expected_str, texture_result_str)

        texture_expected = EntityTexture(3, 4, shapes, shape_id=1)
        texture_expected_str = str(texture_expected)

        texture_result = EntityTexture.fromstr(texture_expected_str)
        texture_result_str = str(texture_result)

        self.assertEqual(texture_expected_str, texture_result_str)
