import sys
sys.path.append("../../../../../..")

import unittest
import numpy as np
from src.main.service.analysisservice.qcsmell.cg import CG

class TestCG(unittest.TestCase):
    matrix = np.array(
        [
            ['None', '1', '2', '3'],
            ['qb-0', 'unitary(ndarray)', '', 'cx()'],
            ['qb-1', '', 'unitary(ndarray)', 'cx()']
        ]
    )

    def test_1_init(self):
        cg = CG()
        oracle = ["use of Customized Gates", "CG", 0]
        self.assertEqual(cg.name, oracle[0])
        self.assertEqual(cg.acronym, oracle[1])
        self.assertEqual(cg.value, oracle[2])

    def test_2_get_result(self):
        cg = CG()
        oracle = 2
        result = cg.get_result(self.matrix)
        self.assertEqual(result, oracle)















