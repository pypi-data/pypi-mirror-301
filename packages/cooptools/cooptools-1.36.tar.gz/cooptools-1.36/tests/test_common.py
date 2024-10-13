import unittest
from cooptools.common import *

class Test_Common(unittest.TestCase):

    def test__flat_lst_of_lst(self):
        # arrange
        n_lsts = 5
        lst_length = 10
        l_o_l = [[x for x in range(lst_length)] for y in range(n_lsts)]

        # act
        flat = flattened_list_of_lists(l_o_l)

        #assert
        self.assertEqual(len(flat), n_lsts * lst_length)


    def test__flat_lst_of_lst__unique(self):
        # arrange
        l_o_l = [
            [0, 1, 2],
            [2, 3, 4],
            [4, 5, 6]
        ]

        # act
        flat = flattened_list_of_lists(l_o_l, unique=True)

        # assert
        self.assertEqual(flat, [0, 1, 2, 3, 4, 5, 6])

    def test__all_indxs_in_lst(self):
        # arrange
        lst = [0, 1, 3, 7, 3, 1, 3, 2]

        # act
        idxs = all_indxs_in_lst(lst, 3)

        # assert
        self.assertEqual(idxs, [2, 4, 6])

    def test__all_indxs_in_lst__none(self):
        # arrange
        lst = [0, 1, 3, 7, 3, 1, 3, 2]

        # act
        idxs = all_indxs_in_lst(lst, 10)

        # assert
        self.assertEqual(idxs, [])
