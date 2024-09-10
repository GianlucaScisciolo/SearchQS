import sys
sys.path.append("../../../../..")

import unittest
from src.main.service.analysisservice.transpilation import Transpilation

class TestTranspilation(unittest.TestCase):
    t = Transpilation()
    
    def test_1_list_gates(self):
        oracle = {
            'original': ['u1', 'u2', 'u3', 'rz', 'sx', 'x', 'cx', 'id'],
            'simple': ['cx', 'u3'],
            'ibm_perth': ['cx', 'id', 'rz', 'sx', 'x'],
            'ibm_sherbroke': ['ecr', 'id', 'rz', 'sx', 'x'],
            'rpcx': ['cx', 'rx', 'ry', 'rz', 'p']
        }
        self.assertEqual(self.t.LIST_GATES, oracle)

    def test_2_list_names_transpilation(self):
        oracle = ['original', 'simple', 'ibm_perth', 'ibm_sherbroke', 'rpcx']
        self.assertEqual(self.t.LIST_NAMES_TRANSPILATION, oracle)












