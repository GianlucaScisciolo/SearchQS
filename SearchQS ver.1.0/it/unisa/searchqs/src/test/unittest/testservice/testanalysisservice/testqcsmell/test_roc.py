import sys
sys.path.append("../../../../../..")

import unittest
import numpy as np
from src.main.service.analysisservice.qcsmell.roc import ROC

class TestROC(unittest.TestCase):
    def setUp(self):
        self.matrix = np.array(
            [
                ['None', '1',   '2',    '3',    '4'], 
                ['qb-0', 'h()', 'cx()', 'cx()', ''], 
                ['qb-1', '',    '',     '',     ''], 
                ['qb-2', '',    'cx()', 'cx()', 'h()']
            ]
        )

    def test_init(self):
        roc = ROC()
        oracle = ["Repeated set of Operations on Circuit", "ROC", 0]
        self.assertEqual(roc.name, oracle[0])
        self.assertEqual(roc.acronym, oracle[1])
        self.assertEqual(roc.value, oracle[2])

    def test_get_result(self):
        roc = ROC()
        oracle = 1
        result = roc.get_result(self.matrix)
        self.assertEqual(result, oracle)









