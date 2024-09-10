import sys
sys.path.append("../../../../../..")

import unittest
from unittest.mock import patch, Mock, MagicMock
import numpy as np
from src.main.service.analysisservice.qcsmell.lc import LC


class TestLC(unittest.TestCase):
    matrix = np.array(
        [
            ['None', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29'], 
            ['qb-0', 'measure()', 'barrier()', 'h()', '', '', '', '', '', '', 'barrier()', 'cx()', '', '', '', 'barrier()', 'h()', '', '', '', '', '', '', 'barrier()', 'measure()', '', '', '', '', ''], 
            ['qb-1', '', 'barrier()', '', 'h()', '', '', '', '', '', 'barrier()', '', '', '', '', 'barrier()', '', 'h()', '', '', '', '', '', 'barrier()', '', 'measure()', '', '', '', ''], 
            ['qb-2', '', 'barrier()', '', '', 'h()', '', '', '', '', 'barrier()', 'measure()', 'cx()', '', '', 'barrier()', '', '', 'h()', '', '', '', '', 'barrier()', '', '', 'measure()', '', '', ''], 
            ['qb-3', '', 'barrier()', '', '', '', 'h()', '', '', '', 'barrier()', '', '', '', '', 'barrier()', '', '', '', 'h()', '', '', '', 'barrier()', '', '', '', 'measure()', '', ''], 
            ['qb-4', '', 'barrier()', '', '', 'measure()', '', 'h()', '', '', 'barrier()', '', '', 'cx()', '', 'barrier()', '', '', '', '', 'h()', '', '', 'barrier()', '', '', '', '', 'measure()', ''], 
            ['qb-5', '', 'barrier()', '', '', '', '', '', 'h()', '', 'barrier()', '', '', '', 'cx()', 'barrier()', '', '', '', '', '', 'h()', '', 'barrier()', '', '', '', '', '', 'measure()'], 
            ['qb-6', 'x()', 'barrier()', '', '', '', '', '', '', 'h()', 'barrier()', 'cx()', 'cx()', 'cx()', 'cx()', 'barrier()', '', '', '', '', '', '', 'h()', 'barrier()', '', '', '', '', '', ''], 
            ['cb-0', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], 
            ['cb-1', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], 
            ['cb-2', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], 
            ['cb-3', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], 
            ['cb-4', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], 
            ['cb-5', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
        ]
    )

    def test_1_init(self):
        lc = LC()
        oracle = ["Long Circuit", "LC", 0]
        self.assertEqual(lc.name, oracle[0])
        self.assertEqual(lc.acronym, oracle[1])
        self.assertEqual(lc.value, oracle[2])

    def test_2_get_result(self):
        lc = LC()
        oracle = 21
        result = lc.get_result(self.matrix)
        self.assertEqual(result, oracle)









